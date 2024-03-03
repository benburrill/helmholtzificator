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

## Usage
To start the interactive eigenfunction explorer, run:

```
$ python3 -m hemholtzificator FILE
```

Where FILE can be either a `.png` file (transparent pixels indicate
where to enforce boundary conditions of 0, no way to specify a
potential) or a `.npz` file (with up to two numpy arrays, boolean array
"mask" is False in the boundary region and float array "potential" is
$V(\vec{x})$ as described above).

The resolution of your input images/arrays should be low!  I recommend
below 100x100 px.
