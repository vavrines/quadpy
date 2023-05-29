import numpy
from sympy import Rational as frac
from sympy import gamma, pi, sqrt

from .. import nsphere
from ..helpers import article, fsd, pm, untangle
from ._helpers import Enr2Scheme

citation = article(
    authors=["A.H. Stroud"],
    title="Some Seventh Degree Integration Formulas for Symmetric Regions",
    journal="SIAM J. Numer. Anal.",
    volume="4",
    number="1",
    pages="37–44",
    url="https://doi.org/10.1137/0704004",
)


def _stroud_1967_7_2(n, variant_a=True):
    if variant_a:
        # the points/weights are complex-valued for n >= 9; one could permit that
        assert n in [2, 3, 4, 6, 7]
        p_m = +1
    else:
        assert n in [3, 4]
        p_m = -1

    sqrt38n = sqrt(3 * (8 - n))

    r2 = (3 * (8 - n) - p_m * (n - 2) * sqrt38n) / 2 / (5 - n)
    s2 = (3 * n - p_m * 2 * sqrt38n) / 2 / (3 * n - 8)
    t2 = (6 + p_m * sqrt38n) / 2
    B = (8 - n) / r2 ** 3 / 8
    C = 1 / s2 ** 3 / 2 ** (n + 3)
    D = 1 / t2 ** 3 / 16
    A = 1 - 2 * n * B - 2 ** n * C - 2 * n * (n - 1) * D

    r = sqrt(r2)
    s = sqrt(s2)
    t = sqrt(t2)

    data = [
        (A, numpy.full((1, n), 0)),
        (B, fsd(n, (r, 1))),
        (C, pm(n, s)),
        (D, fsd(n, (t, 2))),
    ]

    points, weights = untangle(data)
    weights *= sqrt(pi) ** n

    name = "Stroud 1967-7 2 (variant {})".format("a" if variant_a else "b")
    return Enr2Scheme(name, n, weights, points, 7, citation)


def stroud_1967_7_2a(n):
    return _stroud_1967_7_2(n, True)


def stroud_1967_7_2b(n):
    return _stroud_1967_7_2(n, False)


def stroud_1967_7_4(n):
    assert n >= 3

    sqrt2n2 = sqrt(2 * (n + 2))
    r1, r2 = [sqrt((n + 2 - p_m * sqrt2n2) / 2) for p_m in [+1, -1]]
    g = gamma(frac(n, 2))
    A1, A2 = [(n + 2 + p_m * sqrt2n2) / 4 / (n + 2) * g for p_m in [+1, -1]]

    s = nsphere.stroud_1967(n)

    points = numpy.concatenate([r1 * s.points, r2 * s.points])
    weights = numpy.concatenate([A1 * s.weights, A2 * s.weights])
    return Enr2Scheme("Stroud 1967-7 4", n, weights, points, 7, citation)
