from sympy import Rational as frac
from sympy import sqrt

from ..helpers import article
from ._helpers import QuadrilateralScheme, concat, symm_r0, symm_s

citation = article(
    authors=["W. Burnside"],
    title="An approximate quadrature formula",
    journal="Messenger of Math.",
    volume="37",
    year="1908",
    pages="166-167",
)


def burnside():
    r = sqrt(frac(7, 15))
    s = sqrt(frac(7, 9))
    weights, points = concat(symm_r0([frac(10, 49), r]), symm_s([frac(9, 196), s]))
    weights *= 4
    return QuadrilateralScheme("Burnside", weights, points, 5, citation)
