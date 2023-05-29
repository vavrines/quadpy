from math import pi

import numpy

from .. import helpers


class BallScheme:
    def __init__(self, name, citation, degree, weights, points):
        self.name = name
        self.citation = citation
        self.degree = degree

        flt = numpy.vectorize(float)

        if weights.dtype == numpy.float64:
            self.weights = weights
        else:
            assert weights.dtype == numpy.dtype("O")
            self.weights = flt(weights)
            self.weights_symbolic = weights

        if points.dtype == numpy.float64:
            self.points = points
        else:
            assert points.dtype == numpy.dtype("O")
            self.points = flt(points)
            self.points_symbolic = points
        return

    def show(self, backend="vtk"):
        """Displays scheme for 3D ball quadrature.
        """
        helpers.backend_to_function[backend](
            self.points,
            self.weights,
            volume=4.0 / 3.0 * pi,
            edges=[],
            balls=[((0.0, 0.0, 0.0), 1.0)],
        )
        return

    def integrate(self, f, center, radius, dot=numpy.dot):
        center = numpy.asarray(center)
        rr = numpy.multiply.outer(radius, self.points)
        rr = numpy.swapaxes(rr, 0, -2)
        ff = numpy.asarray(f((rr + center).T))
        return numpy.asarray(radius) ** 3 * dot(ff, self.weights)

    def integrate_discrete(self, data, radius, dot=numpy.dot):
        """Quadrature where `data` are pointwise values expected to be
        defined at self.points.
        """
        return radius**3 * dot(data.T, self.weights)
