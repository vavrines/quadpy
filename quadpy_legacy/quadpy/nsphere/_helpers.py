import math

import numpy
from sympy import Rational, gamma, prod


class NSphereScheme:
    def __init__(self, name, dim, weights, points, degree, citation):
        self.name = name
        self.dim = dim
        self.degree = degree
        self.citation = citation

        if weights.dtype == numpy.float64:
            self.weights = weights
        else:
            assert weights.dtype in [numpy.dtype("O"), numpy.int64]
            self.weights = weights.astype(numpy.float64)
            self.weights_symbolic = weights

        if points.dtype == numpy.float64:
            self.points = points
        else:
            assert points.dtype in [numpy.dtype("O"), numpy.int64]
            self.points = points.astype(numpy.float64)
            self.points_symbolic = points
        return

    def integrate(self, f, center, radius, dot=numpy.dot):
        center = numpy.array(center)
        rr = numpy.multiply.outer(radius, self.points)
        rr = numpy.swapaxes(rr, 0, -2)
        ff = numpy.array(f((rr + center).T))
        return numpy.array(radius) ** (self.dim - 1) * dot(ff, self.weights)

    def integrate_discrete(self, data, radius, dot=numpy.dot):
        """Quadrature where `data` are pointwise values defined at self.points.
        """
        return numpy.array(radius) ** (self.dim - 1) * dot(data.T, self.weights)


def integrate_monomial_over_unit_nsphere(alpha, symbolic=False):
    """
    Gerald B. Folland,
    How to Integrate a Polynomial over a Sphere,
    The American Mathematical Monthly,
    Vol. 108, No. 5 (May, 2001), pp. 446-448,
    <https://doi.org/10.2307/2695802>.
    """
    if any(a % 2 == 1 for a in alpha):
        return 0

    if symbolic:
        return 2 * (
            prod([gamma(Rational(a + 1, 2)) for a in alpha])
            / gamma(sum([Rational(a + 1, 2) for a in alpha]))
        )

    # Use lgamma since other with ordinary gamma, numerator and denominator
    # might overflow.
    return 2 * math.exp(
        math.fsum([math.lgamma(0.5 * (a + 1)) for a in alpha])
        - math.lgamma(math.fsum([0.5 * (a + 1) for a in alpha]))
    )
