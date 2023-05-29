import numpy

from ._helpers import HexahedronScheme


def product(scheme1d):
    schemes = scheme1d if isinstance(scheme1d, list) else 3 * [scheme1d]

    wy, wz, wx = numpy.meshgrid(
        schemes[0].weights, schemes[1].weights, schemes[2].weights
    )
    weights = numpy.vstack([wx.flatten(), wy.flatten(), wz.flatten()]).T
    weights = numpy.prod(weights, axis=1)
    # the order, yeah...
    y, z, x = numpy.meshgrid(schemes[0].points, schemes[1].points, schemes[2].points)
    points = numpy.vstack([x.flatten(), y.flatten(), z.flatten()]).T

    degree = min([s.degree for s in schemes])
    return HexahedronScheme(
        "Product scheme ({})".format(scheme1d.name), weights, points, degree
    )
