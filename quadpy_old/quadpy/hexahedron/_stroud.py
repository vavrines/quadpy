from sympy import Rational as frac
from sympy import sqrt

from ..helpers import book, untangle
from ..ncube import ewing
from ._albrecht_collatz import albrecht_collatz as stroud_c3_3_6
from ._hammer_stroud import hammer_stroud_2_3 as stroud_c3_5_2
from ._hammer_stroud import hammer_stroud_5_3a as stroud_c3_7_1a
from ._hammer_stroud import hammer_stroud_5_3b as stroud_c3_7_1b
from ._hammer_wymore import hammer_wymore as stroud_c3_7_2
from ._helpers import HexahedronScheme, pm_rrr
from ._mustard_lyness_blatt import mustard_lyness_blatt_1 as stroud_c3_3_4
from ._mustard_lyness_blatt import mustard_lyness_blatt_2 as stroud_c3_3_5
from ._mustard_lyness_blatt import mustard_lyness_blatt_3 as stroud_c3_3_7
from ._mustard_lyness_blatt import mustard_lyness_blatt_4 as stroud_c3_5_4
from ._mustard_lyness_blatt import mustard_lyness_blatt_5 as stroud_c3_5_5
from ._mustard_lyness_blatt import mustard_lyness_blatt_6 as stroud_c3_5_6
from ._mustard_lyness_blatt import mustard_lyness_blatt_7 as stroud_c3_5_7
from ._sadowsky import sadowsky as stroud_c3_5_8
from ._sarma_stroud import sarma_stroud as stroud_c3_7_3
from ._stroud_1967 import stroud_1967 as stroud_c3_5_1
from ._tyler import tyler_1 as stroud_c3_3_1
from ._tyler import tyler_2 as stroud_c3_5_3

_citation = book(
    authors=["Arthur Stroud"],
    title="Approximate Calculation of Multiple Integrals",
    publisher="Prentice Hall",
    year="1971",
)


def stroud_c3_3_2():
    # Product Gauss scheme
    data = [(frac(1, 8), pm_rrr(sqrt(frac(1, 3))))]
    points, weights = untangle(data)
    weights *= 8
    return HexahedronScheme("Stroud C3 3-2", weights, points, 3, _citation)


def stroud_c3_3_3():
    return ewing(3)


__all__ = [
    "stroud_c3_3_1",
    "stroud_c3_3_2",
    "stroud_c3_3_3",
    "stroud_c3_3_4",
    "stroud_c3_3_5",
    "stroud_c3_3_6",
    "stroud_c3_3_7",
    "stroud_c3_5_1",
    "stroud_c3_5_2",
    "stroud_c3_5_3",
    "stroud_c3_5_4",
    "stroud_c3_5_5",
    "stroud_c3_5_6",
    "stroud_c3_5_7",
    "stroud_c3_5_8",
    "stroud_c3_7_1a",
    "stroud_c3_7_1b",
    "stroud_c3_7_2",
    "stroud_c3_7_3",
]
