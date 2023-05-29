import numpy

from ..helpers import plot_disks_1d


class E1r2Scheme:
    def __init__(self, name, weights, points, degree, citation=None):
        self.name = name
        self.weights = weights
        self.points = points
        self.degree = degree
        self.citation = citation
        return

    def integrate(self, f, dot=numpy.dot):
        x = numpy.array([self.points.T])
        fx = numpy.asarray(f(x))
        return dot(fx, self.weights)

    def integrate_discrete(self, data, dot=numpy.dot):
        """Quadrature where `data` are pointwise values expected to be
        defined at self.points.
        """
        return dot(data.T, self.weights)


    def show(self, *args, **kwargs):
        import matplotlib.pyplot as plt

        self.plot(*args, **kwargs)
        plt.show()
        return

    def plot(self):
        import matplotlib.pyplot as plt

        plt.axis("equal")
        m = 1.1 * numpy.max(self.points)
        plt.plot([-m, +m], [0, 0], color="k")
        pts = numpy.column_stack([self.points, numpy.zeros(len(self.points))])
        plot_disks_1d(plt, pts, self.weights, total_area=1.0)
        return
