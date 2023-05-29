import numpy
from mpmath import mp
from sympy import Rational as frac
from sympy import sqrt

from ..helpers import article, fsd, pm, pm_array, pm_array0, untangle
from ._helpers import SphereScheme, cartesian_to_spherical_sympy

citation = article(
    authors=["A.D. McLaren"],
    title="Optimal Numerical Integration on a Sphere",
    journal="Mathematics of Computation",
    volume="17",
    number="84",
    month="oct",
    year="1963",
    pages="361-383",
    url="https://doi.org/10.1090/S0025-5718-1963-0159418-2",
)


def mclaren_01():
    degree = 3
    data = [(frac(1, 12), fsd(3, (sqrt(frac(1, 2)), 2)))]

    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)


def mclaren_02():
    degree = 5
    # Stroud doesn't mention u=1, but it's implied. (After all, this is integration on a
    # sphere.)
    u = 1

    r = frac(1, 2)
    s, t = [(sqrt(5) + pm_) / 4 for pm_ in [+1, -1]]

    data = [
        (frac(1, 30), fsd(3, (u, 1))),
        (frac(1, 30), pm_array([r, s, t])),
        (frac(1, 30), pm_array([t, r, s])),
        (frac(1, 30), pm_array([s, t, r])),
    ]

    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)


def mclaren_03():
    degree = 7

    # the positive roots of
    #  z^6 - z^4 + 0.2*z^2 - 1/105 = 0,
    # i.e., the square roots of the roots of
    #  z^3 - z^2 + 0.2*z^1 - 1/105 = 0,
    r2, s2, t2 = mp.polyroots([1, -1, frac(1, 5), -frac(1, 105)])
    r = sqrt(r2)
    s = sqrt(s2)
    t = sqrt(t2)

    u = numpy.array([+r, -r, +s, -s, +t, -t])
    v = numpy.array([+s, +t, +t, +r, +r, +s])
    w = numpy.array([+t, +s, +r, +t, +s, +r])

    data = [
        (frac(1, 24), numpy.column_stack([+u, +v, +w])),
        (frac(1, 24), numpy.column_stack([+u, -v, -w])),
        (frac(1, 24), numpy.column_stack([+u, +w, -v])),
        (frac(1, 24), numpy.column_stack([+u, -w, +v])),
    ]

    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)


def mclaren_04():
    degree = 8

    # the positive roots of
    #  z^6 - z^4 + 5/21 * z^2 - 5/441 = 0,
    # i.e., the square roots of the roots of
    #  z^3 - z^2 + 5/21 * z^1 - 5/441 = 0,
    r2, s2, t2 = mp.polyroots([1, -1, frac(5, 21), -frac(5, 441)])
    r = sqrt(r2)
    s = sqrt(s2)
    t = sqrt(t2)

    u = numpy.array([+r, -r, +s, -s, +t, -t])
    v = numpy.array([+s, +t, +t, +r, +r, +s])
    w = numpy.array([+t, +s, +r, +t, +s, +r])

    data = [
        (frac(16, 600), fsd(3, (1, 1))),
        (frac(21, 600), numpy.column_stack([+u, +v, +w])),
        (frac(21, 600), numpy.column_stack([+u, -v, -w])),
        (frac(21, 600), numpy.column_stack([+u, +w, -v])),
        (frac(21, 600), numpy.column_stack([+u, -w, +v])),
    ]
    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)


def mclaren_05():
    degree = 9

    r, s = [sqrt((5 + pm_ * sqrt(5)) / 10) for pm_ in [+1, -1]]
    u, v = [sqrt((3 - pm_ * sqrt(5)) / 6) for pm_ in [+1, -1]]
    t = sqrt(frac(1, 3))

    B1 = frac(25, 840)
    B2 = frac(27, 840)

    data = [
        (B1, pm_array0(3, [r, s], [0, 1])),
        (B1, pm_array0(3, [r, s], [1, 2])),
        (B1, pm_array0(3, [r, s], [2, 0])),
        #
        (B2, pm_array0(3, [u, v], [0, 1])),
        (B2, pm_array0(3, [u, v], [1, 2])),
        (B2, pm_array0(3, [u, v], [2, 0])),
        #
        (B2, pm(3, t)),
    ]
    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)


def mclaren_06():
    degree = 9

    r, s = [sqrt((5 + pm_ * sqrt(5)) / 10) for pm_ in [+1, -1]]
    t = 1
    u = frac(1, 2)
    v, w = [(sqrt(5) + pm_) / 4 for pm_ in [+1, -1]]

    B = frac(25, 1260)
    C = frac(32, 1260)

    data = [
        # ERR Stroud is missing +- at the first r.
        (B, pm_array0(3, [r, s], [0, 1])),
        (B, pm_array0(3, [r, s], [1, 2])),
        (B, pm_array0(3, [r, s], [2, 0])),
        #
        (C, fsd(3, (t, 1))),
        #
        (C, pm_array([u, v, w])),
        (C, pm_array([w, u, v])),
        (C, pm_array([v, w, u])),
    ]
    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)


def mclaren_07():
    degree = 9

    r, s = [sqrt((3 - pm_ * sqrt(5)) / 6) for pm_ in [+1, -1]]
    t = sqrt(frac(1, 3))
    # ERR Stroud incorrectly gives sqrt(0.5)
    u = frac(1, 2)
    v, w = [(sqrt(5) + pm_) / 4 for pm_ in [+1, -1]]

    B = -frac(9, 140)
    C = frac(16, 210)

    data = [
        (B, pm_array0(3, [r, s], [0, 1])),
        (B, pm_array0(3, [r, s], [1, 2])),
        (B, pm_array0(3, [r, s], [2, 0])),
        #
        (B, pm(3, t)),
        #
        (C, fsd(3, (1, 1))),
        #
        (C, pm_array([u, v, w])),
        (C, pm_array([w, u, v])),
        (C, pm_array([v, w, u])),
    ]
    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)


def mclaren_08():
    degree = 11

    r = 1
    s = sqrt(frac(1, 2))
    t = sqrt(frac(1, 3))

    u = sqrt(frac(1, 11))
    v = sqrt(frac(9, 11))

    B1 = frac(9216, 725760)
    B2 = frac(16384, 725760)
    B3 = frac(15309, 725760)
    B4 = frac(14641, 725760)

    data = [
        (B1, fsd(3, (r, 1))),
        (B2, fsd(3, (s, 2))),
        (B3, pm(3, t)),
        (B4, fsd(3, (u, 2), (v, 1))),
    ]
    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)


def mclaren_09():
    degree = 11

    sqrt5 = sqrt(5)

    p, q = [sqrt((5 + pm_ * sqrt5) / 10) for pm_ in [+1, -1]]
    r, s = [sqrt((3 - pm_ * sqrt5) / 6) for pm_ in [+1, -1]]
    t = sqrt(frac(1, 3))

    u = frac(1, 2)
    v, w = [(sqrt(5) + pm_) / 4 for pm_ in [+1, -1]]

    B = frac(625, 27720)
    C = frac(243, 27720)
    D = frac(512, 27720)

    data = [
        (B, pm_array0(3, [p, q], [0, 1])),
        (B, pm_array0(3, [p, q], [1, 2])),
        (B, pm_array0(3, [p, q], [2, 0])),
        #
        (C, pm_array0(3, [r, s], [0, 1])),
        (C, pm_array0(3, [r, s], [1, 2])),
        (C, pm_array0(3, [r, s], [2, 0])),
        #
        (C, pm(3, t)),
        #
        (D, fsd(3, (1, 1))),
        #
        (D, pm_array([u, v, w])),
        (D, pm_array([w, u, v])),
        (D, pm_array([v, w, u])),
    ]
    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)


def mclaren_10():
    degree = 14

    r, s = [sqrt((5 - pm_ * sqrt(5)) / 10) for pm_ in [+1, -1]]
    B = frac(125, 10080)
    C = frac(143, 10080)

    # The roots of
    #
    # 2556125 y^6 - 5112250 y^5 + 3578575 y^4 - 1043900 y^3
    #     + 115115 y^2 - 3562 y + 9 =0
    #
    # in decreasing order.
    y = [
        0.8318603575087328951583062165711519728388,
        0.5607526046766541293084396308069013490725,
        0.4118893592345073860321480490176804941547,
        0.1479981814629634692260834719469411619893,
        0.04473134613410273910111648293922113227845,
        0.002768150983039381173906148718103889666260,
    ]
    z = numpy.sqrt(y)

    u = (
        numpy.array([z[3] - z[2], z[1] - z[4], z[5] - z[1], z[2] - z[5], z[4] - z[3]])
        / 2
        / s
    )
    v = (
        numpy.array([z[4] + z[5], z[5] + z[3], z[2] + z[4], z[3] + z[1], z[1] + z[2]])
        / 2
        / s
    )
    w = (
        numpy.array([z[0] + z[1], z[0] + z[2], z[0] + z[3], z[0] + z[4], z[0] + z[5]])
        / 2
        / s
    )

    data = [
        (B, pm_array0(3, [r, s], [0, 1])),
        (B, pm_array0(3, [r, s], [1, 2])),
        (B, pm_array0(3, [r, s], [2, 0])),
        #
        (C, numpy.column_stack([+u, +v, +w])),
        (C, numpy.column_stack([+u, -v, -w])),
        (C, numpy.column_stack([-u, -v, +w])),
        (C, numpy.column_stack([-u, +v, -w])),
        #
        (C, numpy.column_stack([+v, +w, +u])),
        (C, numpy.column_stack([+v, -w, -u])),
        (C, numpy.column_stack([-v, -w, +u])),
        (C, numpy.column_stack([-v, +w, -u])),
        #
        (C, numpy.column_stack([+w, +u, +v])),
        (C, numpy.column_stack([+w, -u, -v])),
        (C, numpy.column_stack([-w, -u, +v])),
        (C, numpy.column_stack([-w, +u, -v])),
    ]

    points, weights = untangle(data)
    azimuthal_polar = cartesian_to_spherical_sympy(points)
    return SphereScheme("McLaren 1", weights, points, azimuthal_polar, degree, citation)
