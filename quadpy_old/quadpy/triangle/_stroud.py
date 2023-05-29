import numpy

from ..helpers import book
from ..line_segment import gauss_legendre
from ._albrecht_collatz import albrecht_collatz as stroud_t2_3_1
from ._hammer_marlowe_stroud import hammer_marlowe_stroud_5 as stroud_t2_5_1
from ._helpers import TriangleScheme

citation = book(
    authors=["Arthur Stroud"],
    title="Approximate Calculation of Multiple Integrals",
    publisher="Prentice Hall",
    year="1971",
)


def stroud_t2_7_1():
    # conical product Gauss
    gl4 = gauss_legendre(4)
    r = (gl4.points + 1) / 2
    A = gl4.weights / 2

    # Generate Gauss formula for int_0^1 (1-s) * f(s) ds.
    # ```
    # k = numpy.arange(8)
    # moments = 1 / (k**2 + 3*k + 2)
    # alpha, beta = orthopy.line.chebyshev(moments)
    # s, B = orthopy.line.schemes.custom(alpha, beta, mode='numpy')
    # ```
    s = numpy.array(
        [
            5.710419611452533e-02,
            2.768430136381415e-01,
            5.835904323689318e-01,
            8.602401356562251e-01,
        ]
    )
    B = numpy.array(
        [
            1.355069134315012e-01,
            2.034645680102685e-01,
            1.298475476082247e-01,
            3.118097095000554e-02,
        ]
    )

    weights = numpy.array([2 * A[i] * B[j] for i in range(4) for j in range(4)])
    points = numpy.array(
        [
            [s[j], r[i] * (1 - s[j]), (1 - r[i]) * (1 - s[j])]
            for i in range(4)
            for j in range(4)
        ]
    )
    return TriangleScheme("Stroud 7-1", weights, points, 7, citation)


__all__ = ["stroud_t2_3_1", "stroud_t2_5_1", "stroud_t2_7_1"]
