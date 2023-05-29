import numpy
from sympy import sqrt

from .. import nsphere
from ..helpers import article, fsd, pm, untangle, z
from ._helpers import NBallScheme, volume_unit_ball

citation = article(
    authors=["A.H. Stroud"],
    title="Some Seventh Degree Integration Formulas for Symmetric Regions",
    journal="SIAM J. Numer. Anal.",
    volume="4",
    number="1",
    pages="37–44",
    url="https://doi.org/10.1137/0704004",
)


def _stroud_1967_7_ab(n, variant_a):
    if variant_a:
        assert 3 <= n <= 7
        t = 1
    else:
        # ERR Stroud mentions nothing of variant b being only valid up to dimension 6,
        # but that's the way it is.
        assert 3 <= n <= 6
        t = -1

    alpha = sqrt(6 * (n + 6) * (8 - n))

    r2 = (3 * (n + 6) * (8 - n) - t * (n - 2) * alpha) / ((n + 6) * (34 - 5 * n))
    s2 = (3 * n * (n + 6) - t * 2 * alpha) / ((n + 6) * (3 * n ** 2 + 6 * n - 16))
    t2 = (6 * (n + 6) + t * alpha) / (14 * (n + 6))

    B = (8 - n) / (n + 2) / (n + 4) / (n + 6) / r2 ** 3
    C = 1 / (n + 2) / (n + 4) / (n + 6) / s2 ** 3 / 2 ** n
    D = 1 / (n + 2) / (n + 4) / (n + 6) / t2 ** 3 / 2
    A = 1 - 2 * n * B - 2 ** n * C - 2 * n * (n - 1) * D

    r = sqrt(r2)
    s = sqrt(s2)
    t = sqrt(t2)

    data = [(A, z(n)), (B, fsd(n, (r, 1))), (C, pm(n, s)), (D, fsd(n, (t, 2)))]
    points, weights = untangle(data)

    weights *= volume_unit_ball(n)

    name = "Stroud 1967-7{}".format("a" if variant_a else "b")
    return NBallScheme(name, n, weights, points, 7, citation)


def stroud_1967_7_a(n):
    return _stroud_1967_7_ab(n, variant_a=True)


def stroud_1967_7_b(n):
    return _stroud_1967_7_ab(n, variant_a=False)


def stroud_1967_7_c(n):
    assert n >= 3

    alpha = sqrt(2 * (n + 2) * (n + 4))

    r1, r2 = [
        sqrt(((n + 2) * (n + 4) + i * 2 * alpha) / (n + 4) / (n + 6)) for i in [+1, -1]
    ]
    A1, A2 = [
        (2 * (n + 2) ** 2 + i * (n - 2) * alpha) / (4 * n * (n + 2) ** 2)
        for i in [+1, -1]
    ]

    s = nsphere.stroud_1967(n)

    points = numpy.concatenate([r1 * s.points, r2 * s.points])
    weights = numpy.concatenate([A1 * s.weights, A2 * s.weights])

    return NBallScheme("Stroud 1967-7 a", n, weights, points, 7, citation)
