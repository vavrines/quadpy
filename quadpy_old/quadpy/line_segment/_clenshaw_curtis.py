import numpy

from ..helpers import article
from ._helpers import LineSegmentScheme

citation = article(
    authors=["J. Waldvogel"],
    title="Fast Construction of the Fejér and Clenshaw–Curtis Quadrature Rules",
    journal="BIT Numerical Mathematics",
    month="mar",
    year="2006",
    volume="46",
    number="1",
    pages="195–202",
    url="https://doi.org/10.1007/s10543-006-0045-4",
)


def clenshaw_curtis(n):
    degree = n

    points = -numpy.cos((numpy.pi * numpy.arange(n)) / (n - 1))

    if n == 2:
        weights = numpy.array([1.0, 1.0])
        return LineSegmentScheme("Clenshaw-Curtis", degree, weights, points)

    n -= 1
    N = numpy.arange(1, n, 2)
    length = len(N)
    m = n - length
    v0 = numpy.concatenate(
        [2.0 / N / (N - 2), numpy.array([1.0 / N[-1]]), numpy.zeros(m)]
    )
    v2 = -v0[:-1] - v0[:0:-1]
    g0 = -numpy.ones(n)
    g0[length] += n
    g0[m] += n
    g = g0 / (n ** 2 - 1 + (n % 2))

    w = numpy.fft.ihfft(v2 + g)
    assert max(w.imag) < 1.0e-15
    w = w.real

    if n % 2 == 1:
        weights = numpy.concatenate([w, w[::-1]])
    else:
        weights = numpy.concatenate([w, w[len(w) - 2 :: -1]])

    return LineSegmentScheme("Clenshaw-Curtis", degree, weights, points, citation)
