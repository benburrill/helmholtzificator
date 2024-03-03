import numpy as np
from .helmholtz import Helmholtz
from PIL import Image

def load(fname, width):
    if fname.endswith('.png'):
        mask = np.array(Image.open(fname).getchannel('A')) > 10
        return Helmholtz(mask, width=width)

    npz = np.load(fname)
    mask = npz.get('mask')
    potential = npz.get('potential')
    if mask is None:
        if potential is None:
            raise KeyError('Must have either mask or potential array')
        mask = np.ones_like(potential, dtype=bool)

    return Helmholtz(mask, potential, width)
