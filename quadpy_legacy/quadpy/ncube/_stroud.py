import numpy
from sympy import Rational as frac
from sympy import sqrt

from ..helpers import book, fsd, pm
from ._ewing import ewing as stroud_cn_3_5
from ._hammer_stroud import hammer_stroud_2n as stroud_cn_5_2
from ._helpers import NCubeScheme
from ._mustard_lyness_blatt import mustard_lyness_blatt as stroud_cn_5_5
from ._phillips import phillips as stroud_cn_7_1
from ._stroud_1957 import stroud_1957_2 as stroud_cn_2_1
from ._stroud_1957 import stroud_1957_3 as stroud_cn_3_1
from ._stroud_1966 import stroud_1966_a as stroud_cn_5_4
from ._stroud_1966 import stroud_1966_b as stroud_cn_5_6
from ._stroud_1966 import stroud_1966_c as stroud_cn_5_7
from ._stroud_1966 import stroud_1966_d as stroud_cn_5_8
from ._stroud_1968 import stroud_1968 as stroud_cn_5_3
from ._thacher import thacher as stroud_cn_2_2
from ._tyler import tyler as stroud_cn_3_3

_citation = book(
    authors=["Arthur Stroud"],
    title="Approximate Calculation of Multiple Integrals",
    publisher="Prentice Hall",
    year="1971",
)


def stroud_cn_1_1(n):
    # centroid scheme
    reference_volume = 2 ** n
    weights = numpy.array([reference_volume])
    points = numpy.full((1, n), 0)
    return NCubeScheme("Stroud Cn 1-1", n, weights, points, 1, _citation)


def stroud_cn_1_2(n):
    # product trapezoidal scheme
    weights = numpy.full(2 ** n, 1)
    points = pm(n, 1)
    return NCubeScheme("Stroud Cn 1-2", n, weights, points, 1, _citation)


def stroud_cn_3_2(n):
    reference_volume = 2 ** n

    weights = numpy.full(2 * n, frac(reference_volume, 2 * n))
    r = sqrt(frac(n, 3))
    points = fsd(n, (r, 1))
    return NCubeScheme("Stroud Cn 3-2", n, weights, points, 3, _citation)


def stroud_cn_3_4(n):
    reference_volume = 2 ** n
    weights = numpy.full(2 ** n, frac(reference_volume, 2 ** n))
    r = sqrt(3) / 3
    points = pm(n, r)
    return NCubeScheme("Stroud Cn 3-4", n, weights, points, 3, _citation)


def stroud_cn_3_6(n):
    lst = n * [[frac(1, 3), frac(4, 3), frac(1, 3)]]
    weights = numpy.product(numpy.array(numpy.meshgrid(*lst)).T.reshape(-1, n), axis=-1)
    lst = n * [[-1, 0, +1]]
    points = numpy.array(numpy.meshgrid(*lst)).T.reshape(-1, n)
    return NCubeScheme("Stroud Cn 3-6", n, weights, points, 3, _citation)


def stroud_cn_5_9(n):
    lst = n * [[frac(5, 9), frac(8, 9), frac(5, 9)]]
    weights = numpy.product(numpy.array(numpy.meshgrid(*lst)).T.reshape(-1, n), axis=-1)
    sqrt35 = sqrt(frac(3, 5))
    lst = n * [[-sqrt35, 0, sqrt35]]
    points = numpy.array(numpy.meshgrid(*lst)).T.reshape(-1, n)
    return NCubeScheme("Stroud Cn 5-9", n, weights, points, 5, _citation)


__all__ = [
    "stroud_cn_1_1",
    "stroud_cn_1_2",
    "stroud_cn_2_1",
    "stroud_cn_2_2",
    "stroud_cn_3_1",
    "stroud_cn_3_2",
    "stroud_cn_3_3",
    "stroud_cn_3_4",
    "stroud_cn_3_5",
    "stroud_cn_3_6",
    # TODO implement Cn 5-1
    # Cn 5-1 is not implemented because it's based on explicit values only given for
    # n=4,5,6.
    "stroud_cn_5_2",
    "stroud_cn_5_3",
    "stroud_cn_5_4",
    "stroud_cn_5_5",
    "stroud_cn_5_6",
    "stroud_cn_5_7",
    "stroud_cn_5_8",
    "stroud_cn_5_9",
    "stroud_cn_7_1",
]
