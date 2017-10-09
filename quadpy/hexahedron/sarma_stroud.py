# -*- coding: utf-8 -*-
#
from .hammer_wymore import HammerWymore


class SarmaStroud(object):
    '''
    V.L.N. Sarma and A. H. Stroud,
    Eberlein Measure and Mechanical Quadrature Formulae. II. Numerical Results,
    Mathematics of Computation,
    Vol. 23, No. 108 (Oct., 1969), pp. 781-784,
    <https://dx.doi.org/10.2307/2004963>.
    '''
    def __init__(self):
        # Hammer-Wymore is a one-parameter family of schemes, and the
        # parameters lambda is chosen to minimize the standard deviation of
        # Sarma's error functional. The particular value of lambda is not
        # explicitly given in the article, but computed from the specified
        # values. Note that it is only given in single precision.
        lmbda = 1.0329785305
        hw = HammerWymore(lmbda=lmbda)
        self.degree = hw.degree
        self.points = hw.points
        self.weights = hw.weights
        return
