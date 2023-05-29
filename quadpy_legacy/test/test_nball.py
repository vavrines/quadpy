import numpy
import pytest

import quadpy
from helpers import check_degree
from quadpy.nball._helpers import integrate_monomial_over_unit_nball


@pytest.mark.parametrize(
    "scheme",
    [quadpy.nball.dobrodeev_1970(n) for n in range(3, 9)]
    + [quadpy.nball.dobrodeev_1978(n) for n in range(2, 7)]
    + [quadpy.nball.stroud_sn_2_1(dim) for dim in range(2, 9)]
    + [quadpy.nball.stroud_sn_3_1(dim) for dim in range(2, 9)]
    + [quadpy.nball.stroud_sn_3_2(dim) for dim in range(2, 9)]
    + [quadpy.nball.stroud_sn_5_2(dim) for dim in range(2, 9)]
    + [quadpy.nball.stroud_sn_5_3(dim) for dim in range(2, 9)]
    + [quadpy.nball.stroud_sn_5_4(dim) for dim in range(2, 9)]
    + [quadpy.nball.stroud_sn_5_5(dim) for dim in range(2, 9)]
    + [quadpy.nball.stroud_sn_5_6(dim) for dim in range(2, 9)]
    + [quadpy.nball.stroud_sn_5_1a(dim) for dim in range(4, 8)]
    + [quadpy.nball.stroud_sn_5_1b(dim) for dim in range(4, 8)]
    + [quadpy.nball.stroud_sn_7_1a(dim) for dim in range(3, 8)]
    + [quadpy.nball.stroud_sn_7_1b(dim) for dim in range(3, 7)]
    + [quadpy.nball.stroud_sn_7_2(dim) for dim in range(3, 7)]
    + [quadpy.nball.stroud_sn_7_3a(dim) for dim in range(3, 7)]
    + [quadpy.nball.stroud_sn_7_3b(dim) for dim in range(3, 7)]
    + [quadpy.nball.stroud_sn_9_1a(dim) for dim in range(3, 7)]
    + [quadpy.nball.stroud_sn_9_1b(dim) for dim in range(4, 7)]
    + [quadpy.nball.stroud_sn_11_1a(dim) for dim in [3, 4]]
    + [quadpy.nball.stroud_sn_11_1b(dim) for dim in [4, 5]],
)
def test_scheme(scheme):
    assert scheme.points.dtype == numpy.float64, scheme.name
    assert scheme.weights.dtype == numpy.float64, scheme.name

    tol = 1.0e-14
    n = scheme.dim
    center = numpy.zeros(n)
    radius = 1
    degree = check_degree(
        lambda poly: scheme.integrate(poly, center, radius),
        integrate_monomial_over_unit_nball,
        n,
        scheme.degree + 1,
        tol=tol,
    )
    assert (
        degree >= scheme.degree
    ), "{} (dim={})  --  observed: {}, expected: {}".format(
        scheme.name, scheme.dim, degree, scheme.degree
    )
    return


if __name__ == "__main__":
    n_ = 3
    scheme_ = quadpy.nball.Stroud(n_, "Sn 2-1", symbolic=True)
    test_scheme(scheme_)
