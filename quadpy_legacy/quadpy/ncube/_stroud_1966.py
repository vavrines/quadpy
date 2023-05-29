import numpy
from sympy import Rational as frac
from sympy import S, sqrt

from ..helpers import article, fsd, pm, untangle, z
from ._helpers import NCubeScheme, _fs11

_citation = article(
    authors=["A.H. Stroud"],
    title="Some Fifth Degree Integration Formulas for Symmetric Regions",
    journal="Mathematics of Computation",
    volume="20",
    number="93",
    month="jan",
    year="1966",
    pages="90-97",
    url="https://doi.org/10.1090/S0025-5718-1966-0191094-8",
)


def stroud_1966_a(n):
    r = sqrt(frac(5 * n + 4, 30))
    s = sqrt(frac(5 * n + 4, 15 * n - 12))
    data = [
        (frac(40, (5 * n + 4) ** 2), fsd(n, (r, 1))),
        (frac(5 * n - 4, (5 * n + 4)) ** 2 / 2 ** n, pm(n, s)),
    ]

    points, weights = untangle(data)
    weights *= 2 ** n
    return NCubeScheme("Stroud 1966a", n, weights, points, 5, _citation)


def stroud_1966_b(n):
    s = 1 / sqrt(3)
    data = [(frac(4, 5 * n + 4), z(n))]
    for k in range(1, n + 1):
        r = sqrt(frac(5 * k + 4, 15))
        arr = numpy.full((2 ** (n - k + 1), n), S(0))
        arr[:, k - 1 :] = pm(n - k + 1, 1)
        arr[:, k - 1] *= r
        arr[:, k:] *= s
        b = frac(5 * 2 ** (k - n + 1), (5 * k - 1) * (5 * k + 4))
        data.append((b, arr))

    points, weights = untangle(data)
    weights *= 2 ** n
    return NCubeScheme("Stroud 1966b", n, weights, points, 5, _citation)


def stroud_1966_c(n):
    r = sqrt((5 * n + 4 + 2 * (n - 1) * sqrt(5 * n + 4)) / (15 * n))
    s = sqrt((5 * n + 4 - 2 * sqrt(5 * n + 4)) / (15 * n))
    data = [(frac(4, 5 * n + 4), z(n)), (frac(5, (5 * n + 4) * 2 ** n), _fs11(n, r, s))]

    points, weights = untangle(data)
    weights *= 2 ** n
    return NCubeScheme("Stroud 1966c", n, weights, points, 5, _citation)


def stroud_1966_d(n):
    r = sqrt((5 * n - 2 * sqrt(5) + 2 * (n - 1) * sqrt(5 * n + 5)) / (15 * n))
    # This sqrt() is imaginary for negative for n=2.
    s = sqrt((5 * n - 2 * sqrt(5) - 2 * sqrt(5 * n + 5)) / (15 * n))
    t = sqrt((5 + 2 * sqrt(5)) / 15)
    w = frac(1, 2 ** n * (n + 1))
    data = [(w, _fs11(n, r, s)), (w, pm(n, t))]

    points, weights = untangle(data)
    weights *= 2 ** n
    return NCubeScheme("Stroud 1966d", n, weights, points, 5, _citation)
