import matplotlib.pyplot as plt
import numpy
import pytest
import sympy

import quadpy
from helpers import check_degree


def _integrate_exact(k, pyra):
    def f(x):
        return x[0] ** int(k[0]) * x[1] ** int(k[1]) * x[2] ** int(k[2])

    # map the reference hexahedron [-1,1]^3 to the pyramid
    xi = sympy.DeferredVector("xi")
    pxi = (
        +pyra[0] * (1 - xi[0]) * (1 - xi[1]) * (1 - xi[2]) / 8
        + pyra[1] * (1 + xi[0]) * (1 - xi[1]) * (1 - xi[2]) / 8
        + pyra[2] * (1 + xi[0]) * (1 + xi[1]) * (1 - xi[2]) / 8
        + pyra[3] * (1 - xi[0]) * (1 + xi[1]) * (1 - xi[2]) / 8
        + pyra[4] * (1 + xi[2]) / 2
    )

    pxi = [sympy.expand(pxi[0]), sympy.expand(pxi[1]), sympy.expand(pxi[2])]
    # determinant of the transformation matrix
    J = sympy.Matrix(
        [
            [
                sympy.diff(pxi[0], xi[0]),
                sympy.diff(pxi[0], xi[1]),
                sympy.diff(pxi[0], xi[2]),
            ],
            [
                sympy.diff(pxi[1], xi[0]),
                sympy.diff(pxi[1], xi[1]),
                sympy.diff(pxi[1], xi[2]),
            ],
            [
                sympy.diff(pxi[2], xi[0]),
                sympy.diff(pxi[2], xi[1]),
                sympy.diff(pxi[2], xi[2]),
            ],
        ]
    )
    det_J = sympy.det(J)
    # we cannot use abs(), see <https://github.com/sympy/sympy/issues/4212>.
    # abs_det_J = sympy.Piecewise((det_J, det_J >= 0), (-det_J, det_J < 0))
    # This is quite the leap of faith, but sympy will cowardly bail out
    # otherwise.
    abs_det_J = det_J

    exact = sympy.integrate(
        sympy.integrate(
            sympy.integrate(abs_det_J * f(pxi), (xi[2], -1, 1)), (xi[1], -1, +1)
        ),
        (xi[0], -1, +1),
    )

    return float(exact)


@pytest.mark.parametrize(
    "scheme",
    [
        quadpy.pyramid.felippa_1(),
        quadpy.pyramid.felippa_2(),
        quadpy.pyramid.felippa_3(),
        quadpy.pyramid.felippa_4(),
        quadpy.pyramid.felippa_5(),
        quadpy.pyramid.felippa_6(),
        quadpy.pyramid.felippa_7(),
        quadpy.pyramid.felippa_8(),
        quadpy.pyramid.felippa_9(),
    ],
)
def test_scheme(scheme):
    assert scheme.points.dtype in [numpy.float64, numpy.int64], scheme.name
    assert scheme.weights.dtype in [numpy.float64, numpy.int64], scheme.name

    # Test integration until we get to a polynomial degree `d` that can no longer be
    # integrated exactly. The scheme's degree is `d-1`.
    pyra = numpy.array(
        [[-1, -1, -1], [+1, -1, -1], [+1, +1, -1], [-1, +1, -1], [0, 0, 1]]
    )
    degree = check_degree(
        lambda poly: scheme.integrate(poly, pyra),
        lambda k: _integrate_exact(k, pyra),
        3,
        scheme.degree + 1,
    )
    assert degree == scheme.degree
    return


@pytest.mark.parametrize("scheme", [quadpy.pyramid.felippa_5()])
def test_show(scheme):
    scheme.show()
    plt.close()
    return


if __name__ == "__main__":
    scheme_ = quadpy.pyramid.Felippa(3)
    test_scheme(scheme_)
    # test_show(scheme_)
    # quadpy.pyramid.show(scheme_, backend='vtk')
