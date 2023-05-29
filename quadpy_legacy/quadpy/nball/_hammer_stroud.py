from sympy import Rational as frac
from sympy import sqrt

from ..helpers import article, fsd, untangle, z
from ._helpers import NBallScheme, volume_unit_ball

citation = article(
    authors=["Preston C. Hammer", "Arthur H. Stroud"],
    title="Numerical Evaluation of Multiple Integrals II",
    journal="Math. Comp.",
    volume="12",
    year="1958",
    pages="272-280",
    url="https://doi.org/10.1090/S0025-5718-1958-0102176-6",
)


def hammer_stroud_11n(n, alpha):
    r = sqrt(frac(n + alpha, n + alpha + 2))
    data = [(frac(1, 2 * n), fsd(n, (r, 1)))]

    points, weights = untangle(data)
    weights *= volume_unit_ball(n)
    return NBallScheme("Hammer-Stroud 11n", n, weights, points, 3, citation)


def hammer_stroud_12n(n, alpha):
    r = sqrt(frac(3 * (n + alpha + 2), (n + 2) * (n + alpha + 4)))
    B1 = frac(
        (4 - n) * (n + 2) * (n + alpha) * (n + alpha + 4), 18 * n * (n + alpha + 2) ** 2
    )
    B2 = frac((n + 2) * (n + alpha) * (n + alpha + 4), 36 * n * (n + alpha + 2) ** 2)
    B0 = 1 - 2 * n * B1 - 2 * n * (n - 1) * B2

    data = [(B0, z(n)), (B1, fsd(n, (r, 1))), (B2, fsd(n, (r, 2)))]

    points, weights = untangle(data)
    weights *= volume_unit_ball(n)
    return NBallScheme("Hammer-Stroud 12n", n, weights, points, 5, citation)
