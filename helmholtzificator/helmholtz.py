import numpy as np
import itertools as it


class Helmholtz:
    def __init__(self, mask, potential=None, width=1):
        self.width = width
        self.shape = mask.shape
        self.mask_idx = np.nonzero(mask)
        self.matrix = laplacian_2d(np.transpose(self.mask_idx), (self.shape[-1] - 1) ** 2)
        if potential is not None:
            self.matrix = self.matrix - np.diag(potential[self.mask_idx] * self.width**2)
            self.min_pot = np.min(potential)
        else:
            self.min_pot = 0

    def func(self, vector):
        """ Convert vectors into functions """
        grid = np.zeros(self.shape, dtype=float)
        grid[self.mask_idx] = vector
        return grid

    def eigenstats(self, eigenvector):
        """ Estimate eigenvalue and uncertainty given an approximate eigenvector """
        vscaled = self.matrix @ eigenvector
        eigenvalue = (eigenvector @ vscaled) / (eigenvector @ eigenvector)
        return (
            eigenvalue / self.width**2,
            np.std(vscaled / eigenvalue - eigenvector) / self.width**2
        )

    def max_eigenvector(self, **kwargs):
        """ Returns most dominant eigenvector """
        return iterate_until(self.matrix, **kwargs)

    def min_eigenvector(self, **kwargs):
        """ Returns eigenvector with eigenvalue farthest from max_eigenvector """
        return self.find_eigenvector(-self.min_pot, **kwargs)

        # max_vect = self.max_eigenvector(**{**kwargs, 'fail': 'ignore'})
        # vscaled = self.matrix @ max_vect
        # max_val = (max_vect @ vscaled) / (max_vect @ max_vect)
        # shifted = self.matrix - np.diag([max_val] * len(self.matrix))
        # return iterate_until(shifted, **kwargs)

    def find_eigenvector(self, eigenval=0, **kwargs):
        """ Finds an eigenvector close to the given target eigenvalue """
        shifted_inverse = np.linalg.inv(self.matrix - np.diag([eigenval * self.width**2] * len(self.matrix)))
        return iterate_until(shifted_inverse, **kwargs)


def laplacian_2d(vertices, h_inv_sq):
    lapl = np.diag(np.array(
        [-4 * h_inv_sq] * len(vertices),
        dtype=np.min_scalar_type(-4 * h_inv_sq)
    ))

    vmap = {tuple(vert): idx for idx, vert in enumerate(vertices)}
    for (i, j), idx in vmap.items():
        for neighbor in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            try:
                nidx = vmap[neighbor]
            except KeyError:
                continue
            lapl[idx][nidx] = lapl[nidx][idx] = h_inv_sq
    return lapl


def iterate(mat):
    v = np.random.randn(len(mat))
    while True:
        v = mat @ v
        v /= np.linalg.norm(v)
        yield v


def iterate_until(mat, *, thresh=1e-7, max_iter=5000, fail='error'):
    for i, (prev, cur) in zip(range(max_iter), it.pairwise(iterate(mat))):
        if abs(abs(cur@prev) - 1) < thresh:
            return cur

    msg = 'Failed to reach threshold, max iterations exceeded'
    if fail == 'error': raise ValueError(msg)
    elif fail != 'ignore': print(msg)
    return cur
