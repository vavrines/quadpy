import itertools

import numpy

from ..helpers import n_outer


class NCubeScheme:
    def __init__(self, name, dim, weights, points, degree, citation):
        self.name = name
        self.dim = dim
        self.degree = degree
        self.citation = citation

        if weights.dtype == numpy.float64:
            self.weights = weights
        else:
            assert weights.dtype in [numpy.dtype("O"), numpy.int64]
            self.weights = weights.astype(numpy.float64)
            self.weights_symbolic = weights

        if points.dtype == numpy.float64:
            self.points = points
        else:
            assert points.dtype in [numpy.dtype("O"), numpy.int64]
            self.points = points.astype(numpy.float64)
            self.points_symbolic = points
        return

    def integrate(self, f, ncube, dot=numpy.dot):
        x = transform(self.points.T, ncube).T
        detJ = get_detJ(self.points.T, ncube)
        return dot(f(x) * abs(detJ), self.weights)

    def integrate_discrete(self, data, dot=numpy.dot):
        """Quadrature where `data` are pointwise values defined at self.points.
        """
        detJ = get_detJ(self.points.T, ncube)
        return dot(data.T * abs(detJ), self.weights)


def transform(xi, cube):
    """Transform the points `xi` from the reference cube to `cube`.
    """
    # For d==2, the result used to be computed with
    #
    # out = (
    #     + outer(0.25*(1.0-xi[0])*(1.0-xi[1]), cube[0, 0])
    #     + outer(0.25*(1.0+xi[0])*(1.0-xi[1]), cube[1, 0])
    #     + outer(0.25*(1.0-xi[0])*(1.0+xi[1]), cube[0, 1])
    #     + outer(0.25*(1.0+xi[0])*(1.0+xi[1]), cube[1, 1])
    #     )
    #
    # This array of multiplications and additions is reminiscent of dot(), and
    # indeed tensordot() can handle the situation. We just need to compute the
    # `1+-xi` products and align them with `cube`.
    one_mp_xi = numpy.stack([0.5 * (1.0 - xi), 0.5 * (1.0 + xi)], axis=1)
    a = n_outer(one_mp_xi)

    # <https://stackoverflow.com/q/45372098/353337>
    d = xi.shape[0]
    return numpy.tensordot(a, cube, axes=(range(d), range(d)))


def get_detJ(xi, cube):
    """Get the determinant of the transformation matrix.
    """
    # For d==2, the result can be computed with
    # ```
    # J0 = (
    #     - numpy.multiply.outer(0.25*(1-xi[1]), quad[0, 0])
    #     + numpy.multiply.outer(0.25*(1-xi[1]), quad[1, 0])
    #     - numpy.multiply.outer(0.25*(1+xi[1]), quad[0, 1])
    #     + numpy.multiply.outer(0.25*(1+xi[1]), quad[1, 1])
    #     ).T
    # J1 = (
    #     - numpy.multiply.outer(0.25*(1-xi[0]), quad[0, 0])
    #     - numpy.multiply.outer(0.25*(1+xi[0]), quad[1, 0])
    #     + numpy.multiply.outer(0.25*(1-xi[0]), quad[0, 1])
    #     + numpy.multiply.outer(0.25*(1+xi[0]), quad[1, 1])
    #     ).T
    # out = J0[0]*J1[1] - J1[0]*J0[1]
    # ```
    # Like transform(), simplify here and form the determinant explicitly.
    d = xi.shape[0]

    one_mp_xi = numpy.stack([0.5 * (1.0 - xi), 0.5 * (1.0 + xi)], axis=1)

    # Build the Jacobi matrix row by row.
    J = []
    for k in range(d):
        a = one_mp_xi.copy()
        a[k, 0, :] = -0.5
        a[k, 1, :] = +0.5
        a0 = n_outer(a)
        J.append(numpy.tensordot(a0, cube, axes=(range(d), range(d))).T)

    # `det` needs the square at the end. Fortran...
    # For d==2 or d==3, we could avoid this copy and compute the determinant
    # with their elementary formulas, i.e.,
    #
    #     + J[0][0]*J[1][1] - J[1][0]*J[0][1];
    #
    #     + J0[0]*J1[1]*J2[2] + J1[0]*J2[1]*J0[2] + J2[0]*J0[1]*J1[2]
    #     - J0[2]*J1[1]*J2[0] - J1[2]*J2[1]*J0[0] - J2[2]*J0[1]*J1[0].
    #
    J = numpy.array(J)
    J = numpy.moveaxis(J, (0, 1), (-2, -1))
    out = numpy.linalg.det(J)
    return out


def integrate_monomial_over_ncube(ncube_limits, exp):
    return numpy.prod(
        [
            (a[1] ** (k + 1) - a[0] ** (k + 1)) / (k + 1)
            for a, k in zip(ncube_limits, exp)
        ]
    )


def ncube_points(*xyz):
    """Given the end points of an n-cube aligned with the coordinate axes, this returns
    the corner points of the cube in the correct data structure.
    """
    return numpy.moveaxis(numpy.array(numpy.meshgrid(*xyz, indexing="ij")), 0, -1)


def _fs11(n, r, s):
    """Get all permutations of [+-r, +-s, ..., +-s] of length n.
    len(out) == n * 2**n.
    """
    # <https://stackoverflow.com/a/45321972/353337>
    k1 = 1
    k2 = n - 1
    idx = itertools.combinations(range(k1 + k2), k1)
    vs = ((s if j not in i else r for j in range(k1 + k2)) for i in idx)
    return numpy.array(
        list(
            itertools.chain.from_iterable(
                itertools.product(*((+vij, -vij) for vij in vi)) for vi in vs
            )
        )
    )


def _s(n, a, b):
    """Get all permutations of [a, b, ..., b] of length n. len(out) == n.
    """
    out = numpy.full((n, n), b)
    numpy.fill_diagonal(out, a)
    return out


def _s2(n, a):
    """Get all permutations of [a, a, 0, 0, ..., 0] of length n.
    len(out) == (n-1)*n / 2.
    """
    return _s11(n, a, a)


def _s11(n, a, b):
    """Get all permutations of [a, b, 0, 0, ..., 0] of length n.
    len(out) == (n-1)*n.
    """
    s = [a, b] + (n - 2) * [0]
    # First permutations, then set can be really inefficient if items are
    # repeated. Check out <https://stackoverflow.com/q/6284396/353337> for
    # improvements.
    return numpy.array(list(set(itertools.permutations(s, n))))
