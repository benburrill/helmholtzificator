# Helmholtzificator
Explore eigenfunctions of the 2D Laplacian, subject to Dirichlet
boundary conditions.  In addition to the Helmholtz equation,
Hemholtzificator also supports similar eigenvalue problems of the form

$$
\nabla^2 f(\vec{x}) - V(\vec{x})f(\vec{x}) = \lambda f(\vec{x})
$$

This is the form of the time-independent Schrödinger equation with
potential $\propto V(\vec{x})$.

Helmholtzificator provides an interactive matplotlib user interface with
a slider to select eigenvalues.

## Examples

By drawing the silhouette of a cat face in an image editor and passing it as input to helmholtzificator, we can create some immortal, time-independent Schrödinger's cats:

![Cat face](https://github.com/benburrill/helmholtzificator/assets/8140726/096aa8e0-1211-4fd8-a6e0-025a11e90030)

Here's an eigenfunction for a quartic double-well potential:

![Double well](https://github.com/benburrill/helmholtzificator/assets/8140726/aa3a6ef3-8f43-437a-9e8a-e3f2de370b13)

## Usage
To start the interactive eigenfunction explorer, run:

```
$ python3 -m hemholtzificator FILE
```

Where FILE can be either a `.png` file (transparent pixels specify
boundary conditions of 0, no way to specify a potential) or a `.npz`
file (with up to two numpy arrays, boolean array "mask" is False in the
boundary region and float array "potential" is $V(\vec{x})$ as described
above).

In addition to the mask given by the input, the boundary condition of 0
is also enforced outside the bounds of the image/array.

All images are considered to have a pixel-centered width of 1, ie the
top left pixel has coordinates (0, 0) and the top right pixel has
coordinates (0, 1).

Uncertainties are estimated rather crudely, so take them with a grain of
salt.  They give some indication of how well the solution has converged, but
I typically see more variance in eigenvalues by pressing refresh a bunch of
times than can be explained by the uncertainties.

The resolution of your input images/arrays should be low!  I recommend
below 100x100 px.
