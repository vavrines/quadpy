import math

import numpy
import pytest

import orthopy
import quadpy
from helpers import check_degree_ortho


@pytest.mark.parametrize(
    "scheme",
    [quadpy.ncube.dobrodeev_1970(n) for n in range(5, 8)]
    + [quadpy.ncube.dobrodeev_1978(n) for n in range(2, 8)]
    + [quadpy.ncube.hammer_stroud_1n(n) for n in range(3, 7)]
    + [quadpy.ncube.hammer_stroud_2n(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_1_1(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_1_2(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_2_1(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_2_2(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_3_1(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_3_2(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_3_3(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_3_4(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_3_5(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_3_6(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_5_2(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_5_3(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_5_4(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_5_5(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_5_6(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_5_7(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_5_8(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_5_9(n) for n in range(3, 7)]
    + [quadpy.ncube.stroud_cn_7_1(n) for n in range(3, 7)],
)
def test_scheme(scheme, tol=1.0e-11):
    assert scheme.points.dtype in [numpy.float64, numpy.int64], scheme.name
    assert scheme.weights.dtype in [numpy.float64, numpy.int64], scheme.name

    n = scheme.dim
    ncube_limits = [[-1.0, 1.0]] * n
    ncube = quadpy.ncube.ncube_points(*ncube_limits)

    # degree = check_degree(
    #     lambda poly: scheme.integrate(poly, ncube),
    #     lambda exp: integrate_monomial_over_ncube(ncube_limits, exp),
    #     n,
    #     scheme.degree + 1,
    #     tol=tol,
    # )
    # assert degree >= scheme.degree, "observed: {}, expected: {}".format(
    #     degree, scheme.degree
    # )

    def eval_orthopolys(x):
        return numpy.concatenate(
            orthopy.ncube.tree(x, scheme.degree + 1, symbolic=False)
        )

    vals = scheme.integrate(eval_orthopolys, ncube)

    # Put vals back into the tree structure:
    # len(approximate[k]) == k+1
    approximate = [
        vals[
            numpy.prod(range(k, k + n))
            // math.factorial(n) : numpy.prod(range(k + 1, k + 1 + n))
            // math.factorial(n)
        ]
        for k in range(scheme.degree + 2)
    ]

    exact = [numpy.zeros(len(s)) for s in approximate]
    exact[0][0] = numpy.sqrt(2.0) ** n

    degree = check_degree_ortho(approximate, exact, abs_tol=tol)

    assert degree >= scheme.degree, "{} (dim: {}) -- Observed: {}, expected: {}".format(
        scheme.name, scheme.dim, degree, scheme.degree
    )
    return


if __name__ == "__main__":
    n_ = 4
    scheme_ = quadpy.ncube.Stroud(n_, "Cn 7-1")
    test_scheme(scheme_, 1.0e-14)
