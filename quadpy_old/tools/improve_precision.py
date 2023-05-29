import math

import numpy
from scipy.optimize import least_squares, lsq_linear, minimize

import orthopy
import quadpy
from quadpy.helpers import untangle
from quadpy.sphere._helpers import cartesian_to_spherical
from quadpy.sphere._heo_xu import _f, _f1, _f2, _f11


def partition(boxes, balls):
    """Create all nonnegative tuples of length d which sum up to n.
    """
    # <https://stackoverflow.com/a/36748940/353337>
    # See <https://stackoverflow.com/a/45348441/353337> for an alterative
    # solution.
    def rec(boxes, balls, parent=tuple()):
        if boxes > 1:
            for i in range(balls + 1):
                for x in rec(boxes - 1, i, parent + (balls - i,)):
                    yield x
        else:
            yield parent + (balls,)

    return list(rec(boxes, balls))


def integrate_monomial_over_enr(k):
    if numpy.any(k % 2 == 1):
        return 0
    n = len(k)
    return (
        2
        * math.factorial(sum(k) + n - 1)
        * numpy.prod([math.gamma((kk + 1) / 2.0) for kk in k])
        / math.gamma((sum(k) + n) / 2)
    )


def one():
    def weights_from_points(azimuthal, polar):
        out = orthopy.sphere.tree_sph(
            polar, azimuthal, scheme.degree, standardization="quantum mechanic"
        )

        A = numpy.array([row for level in out for row in level])

        b = numpy.zeros(A.shape[0])
        # b[0] = numpy.sqrt(4 * numpy.pi)
        b[0] = 1.0 / (2 * numpy.sqrt(numpy.pi))

        # solve linear least-squares problem for the weights
        res = lsq_linear(A, b, tol=1.0e-15)
        return res.x, res.fun

    def f(x):
        azimuthal, polar = x.reshape(2, -1)
        _, err = weights_from_points(azimuthal, polar)
        v = numpy.sqrt(err.real ** 2 + err.imag ** 2)
        return v

    scheme = quadpy.sphere.heo_xu_13()
    print(scheme.points)

    # x0 = numpy.column_stack([scheme.weights, scheme.points]).T.reshape(-1)
    x0 = scheme.azimuthal_polar.T.reshape(-1)
    # x0 += 1.0e-10 * numpy.random.rand(*x0.shape)

    out = least_squares(f, x0, gtol=1.0e-16, xtol=1.0e-16)
    # print(out.x)
    # print(out.status, out.nfev, out.njev)
    # print(out.message)
    assert out.success

    azimuthal, polar = out.x.reshape(2, -1)
    w, _ = weights_from_points(azimuthal, polar)
    assert numpy.all(numpy.imag(w) < 1.0e-14)
    w = numpy.real(w)
    print("weights:")
    for item in w:
        print("{:.15e}".format(item))

    x = numpy.sin(polar) * numpy.cos(azimuthal)
    y = numpy.sin(polar) * numpy.sin(azimuthal)
    z = numpy.cos(polar)
    X = numpy.column_stack([x, y, z])
    print()
    print("points:")
    for item in X:
        print("{:.15e}  {:.15e}  {:.15e}".format(*item))
    return


def heo_xu_13():
    def f(x):
        degree = 13
        data = [
            (x[0], _f((1.0, 1))),
            (x[1], _f2(x[4])),
            (x[2], _f2(x[5])),
            (x[3], _f1(x[6])),
        ]
        points, weights = untangle(data)
        # print(sum(weights))
        azimuthal, polar = cartesian_to_spherical(points).T

        out = orthopy.sphere.tree_sph(
            polar, azimuthal, degree, standardization="quantum mechanic"
        )

        A = numpy.array([row for level in out for row in level])
        out = numpy.dot(A, weights)
        out[0] -= 1.0 / (2 * numpy.sqrt(numpy.pi))
        v = numpy.sqrt(out.real ** 2 + out.imag ** 2)
        # return v
        norm_v = numpy.sqrt(numpy.vdot(v, v))
        print(norm_v)
        return norm_v

    x0 = [
        0.013_866_592_105,
        0.013_050_931_863,
        0.013_206_423_223,
        0.011_942_663_555,
        0.286_640_146_767,
        0.659_905_001_656,
        0.539_490_098_706,
    ]
    out = minimize(f, x0, method="Nelder-Mead", tol=1.0e-17)
    print(out.status, out.nfev)
    print(out.message)
    assert out.success
    print()
    for x in out.x:
        print(f"{x:.15e}")
    return


def heo_xu_15():
    def f(x):
        degree = 15
        data = [
            (x[0], _f((1.0, 1))),
            (x[1], _f((math.sqrt(0.5), 2))),
            (x[2], _f2(x[5])),
            (x[3], _f2(x[6])),
            (x[4], _f1(x[7])),
        ]
        points, weights = untangle(data)
        azimuthal, polar = cartesian_to_spherical(points).T

        out = orthopy.sphere.tree_sph(
            polar, azimuthal, degree, standardization="quantum mechanic"
        )

        A = numpy.array([row for level in out for row in level])
        out = numpy.dot(A, weights)
        out[0] -= 1.0 / (2 * numpy.sqrt(numpy.pi))
        v = numpy.sqrt(out.real ** 2 + out.imag ** 2)
        norm_v = numpy.sqrt(numpy.vdot(v, v))
        print(norm_v)
        return norm_v

    x0 = [
        0.013_191_522_874,
        0.011_024_070_845,
        0.010_538_971_114,
        0.011_656_960_715,
        0.010_660_818_696,
        0.337_785_899_794,
        0.658_511_676_782,
        0.399_194_381_765,
    ]
    out = minimize(f, x0, method="Nelder-Mead", tol=1.5e-16, options={"maxiter": 10000})
    print(out.status, out.nfev)
    print(out.message)
    assert out.success
    print()
    for x in out.x:
        print(f"{x:.15e}")
    return


def heo_xu_17():
    def f(x):
        degree = 17
        data = [
            (x[0], _f((math.sqrt(1.0 / 3.0), 3))),
            (x[1], _f((1.0, 1))),
            (x[2], _f2(x[6])),
            (x[3], _f2(x[7])),
            (x[4], _f1(x[8])),
            (x[5], _f1(x[9])),
        ]
        points, weights = untangle(data)
        azimuthal, polar = cartesian_to_spherical(points).T

        out = orthopy.sphere.tree_sph(
            polar, azimuthal, degree, standardization="quantum mechanic"
        )

        A = numpy.array([row for level in out for row in level])
        out = numpy.dot(A, weights)
        out[0] -= 1.0 / (2 * numpy.sqrt(numpy.pi))
        v = numpy.sqrt(out.real ** 2 + out.imag ** 2)
        norm_v = numpy.sqrt(numpy.vdot(v, v))
        print(norm_v)
        return norm_v

    x0 = [
        +0.009_103_396_603,
        -0.002_664_002_664,
        +0.010_777_836_655,
        +0.009_161_945_784,
        +0.009_798_544_912,
        +0.009_559_874_447,
        0.357_406_744_337,
        0.678_598_344_546,
        0.542_521_185_161,
        0.222_866_509_741,
    ]
    out = minimize(f, x0, method="Nelder-Mead", tol=1.0e-17, options={"maxiter": 10000})
    print(out.status, out.nfev)
    print(out.message)
    assert out.success
    print()
    for x in out.x:
        print(f"{x:.15e}")

    return


def heo_xu_19_1():
    def f(x):
        degree = 19
        data = [
            (x[0], _f((math.sqrt(1.0 / 3.0), 3))),
            (x[1], _f((1.0, 1))),
            (x[2], _f((math.sqrt(0.5), 2))),
            (x[3], _f2(x[7])),
            (x[4], _f2(x[8])),
            (x[5], _f1(x[9])),
            (x[6], _f11(x[10], x[11])),
        ]
        points, weights = untangle(data)
        azimuthal, polar = cartesian_to_spherical(points).T

        out = orthopy.sphere.tree_sph(
            polar, azimuthal, degree, standardization="quantum mechanic"
        )

        A = numpy.array([row for level in out for row in level])
        out = numpy.dot(A, weights)
        out[0] -= 1.0 / (2 * numpy.sqrt(numpy.pi))
        v = numpy.sqrt(out.real ** 2 + out.imag ** 2)
        norm_v = numpy.sqrt(numpy.vdot(v, v))
        print(norm_v)
        return norm_v

    x0 = [
        0.008_559_575_701,
        0.006_231_186_664,
        0.007_913_582_691,
        0.007_736_373_931,
        0.004_644_831_902,
        0.007_625_284_540,
        0.006_646_198_191,
        0.201_742_306_653,
        0.675_586_904_541,
        0.443_668_207_806,
        0.496_188_289_109,
        0.814_892_033_188,
    ]

    out = minimize(f, x0, method="Nelder-Mead", tol=1.0e-16, options={"maxiter": 10000})
    print(out.status, out.nfev)
    print(out.message)
    assert out.success
    print()
    for x in out.x:
        print(f"{x:.15e}")

    return


def heo_xu_19_2():
    def f(x):
        degree = 19
        data = [
            (x[0], _f((math.sqrt(1.0 / 3.0), 3))),
            (x[1], _f2(x[6])),
            (x[2], _f2(x[7])),
            (x[3], _f2(x[8])),
            (x[4], _f2(x[9])),
            (x[5], _f11(x[10], x[11])),
        ]

        points, weights = untangle(data)
        azimuthal, polar = cartesian_to_spherical(points).T

        out = orthopy.sphere.tree_sph(
            polar, azimuthal, degree, standardization="quantum mechanic"
        )

        A = numpy.array([row for level in out for row in level])
        out = numpy.dot(A, weights)
        out[0] -= 1.0 / (2 * numpy.sqrt(numpy.pi))
        v = numpy.sqrt(out.real ** 2 + out.imag ** 2)
        norm_v = numpy.sqrt(numpy.vdot(v, v))
        print(norm_v)
        return norm_v

    x0 = [
        0.006_159_164_865,
        0.007_661_426_126,
        0.006_632_044_977,
        0.006_075_982_031,
        0.005_261_983_872,
        0.006_991_087_353,
        0.154_480_689_145,
        0.414_167_295_917,
        0.667_293_171_280,
        0.703_446_477_338,
        0.449_332_832_327,
        0.882_270_011_260,
    ]

    out = minimize(f, x0, method="Nelder-Mead", tol=1.5e-16, options={"maxiter": 10000})
    print(out.status, out.nfev)
    print(out.message)
    assert out.success
    print()
    for x in out.x:
        print(f"{x:.15e}")

    return


def stenger_7a_5():
    from quadpy.helpers import fsd, untangle, z, get_all_exponents
    from quadpy.nball._helpers import integrate_monomial_over_unit_nball

    def f(x):
        degree = 7
        n = 5
        u = x[0]
        v = x[1]
        B = x[2:]
        data = [
            (B[0], z(n)),
            (B[1], fsd(n, (u, 1))),
            (B[2], fsd(n, (v, 1))),
            (B[3], fsd(n, (u, 2))),
            (B[4], fsd(n, (v, 2))),
            (B[5], fsd(n, (u, 3))),
        ]
        points, weights = untangle(data)

        exponents = get_all_exponents(n, degree)
        # flatten list
        exponents = numpy.array([item for sublist in exponents for item in sublist])

        def evaluate_all_monomials(x):
            return numpy.prod(x[..., None] ** exponents.T[:, None], axis=0).T

        flt = numpy.vectorize(float)
        exact_vals = flt([integrate_monomial_over_unit_nball(k) for k in exponents])

        A = evaluate_all_monomials(points.T)

        out = numpy.dot(A, weights)
        out -= exact_vals

        norm_v = numpy.sqrt(numpy.dot(out, out))
        print(norm_v)
        return norm_v

    x0 = [
        0.250_562_808_085_732,
        0.694_746_590_606_866,
        -0.220_221_371_883_822e03,
        +0.730_167_125_339_176e02,
        +0.143_281_369_027_706,
        -0.203_714_128_400_494e02,
        +0.448_293_291_677_155e-01,
        +0.383_685_702_879_441e01,
    ]

    out = minimize(f, x0, method="Powell", tol=1.0e-12, options={"maxiter": 10000})
    print(out.status, out.nfev)
    print(out.message)
    assert out.success
    print()
    for x in out.x:
        print(f"{x:.15e}")
    return


def stenger_11a_5():
    from quadpy.helpers import fsd, untangle, z, get_all_exponents
    from quadpy.nball._helpers import integrate_monomial_over_unit_nball

    def f(x):
        degree = 11
        n = 5
        u = x[0]
        v = x[1]
        w = x[2]
        B = x[3:]
        data = [
            (B[0], z(n)),
            (B[1], fsd(n, (u, 1))),
            (B[2], fsd(n, (v, 1))),
            (B[3], fsd(n, (w, 1))),
            (B[4], fsd(n, (u, 2))),
            (B[5], fsd(n, (v, 2))),
            (B[6], fsd(n, (w, 2))),
            (B[7], fsd(n, (u, 1), (v, 1))),
            (B[8], fsd(n, (u, 1), (w, 1))),
            (B[9], fsd(n, (u, 3))),
            (B[10], fsd(n, (v, 3))),
            (B[11], fsd(n, (w, 3))),
            (B[12], fsd(n, (u, 2), (v, 1))),
        ]
        if n > 3:
            data += [(B[13], fsd(n, (u, 4))), (B[14], fsd(n, (v, 4)))]
        if n > 4:
            data += [(B[15], fsd(n, (u, 5)))]
        points, weights = untangle(data)

        exponents = get_all_exponents(n, degree)
        # flatten list
        exponents = numpy.array([item for sublist in exponents for item in sublist])

        def evaluate_all_monomials(x):
            return numpy.prod(x[..., None] ** exponents.T[:, None], axis=0).T

        flt = numpy.vectorize(float)
        exact_vals = flt([integrate_monomial_over_unit_nball(k) for k in exponents])

        A = evaluate_all_monomials(points.T)

        out = numpy.dot(A, weights)
        out -= exact_vals

        norm_v = numpy.sqrt(numpy.dot(out, out))
        print()
        print(norm_v)
        print()
        for xx in x:
            print(f"{xx:.15e}")
        return norm_v

    x0 = [
        0.819_845_995_463_488,
        0.540_604_637_387_361,
        0.188_677_422_490_785,
        -0.455_346_412_352_218e03,
        -0.643_198_057_179_463,
        -0.313_723_910_937_508,
        +0.142_863_899_851_242e03,
        -0.115_044_196_304_602e-02,
        +0.149_484_688_898_586,
        -0.373_831_314_185_824e02,
        -0.141_469_445_049_282e-01,
        +0.104_863_970_436_266,
        -0.973_070_178_977_534e-03,
        -0.862_234_640_073_899e-02,
        +0.654_476_925_250_512e01,
        +0.153_312_717_360_660e-02,
        -0.611_928_443_128_898e-04,
        +0.622_126_777_947_090e-02,
        +0.887_274_197_302_674e-05,
    ]

    out = minimize(f, x0, method="Powell", tol=1.0e-12, options={"maxiter": 10000})
    print(out.status, out.nfev)
    print(out.message)
    assert out.success
    print()
    for x in out.x:
        print(f"{x:.15e}")
    return


def stenger_11b_3():
    from quadpy.helpers import fsd, untangle, z, get_all_exponents
    from quadpy.nball._helpers import integrate_monomial_over_unit_nball

    def f(x):
        degree = 11
        n = 3

        u = 0.871_740_148_509_601
        v = 0.591_700_181_433_148
        w = 0.209_299_217_902_484

        # u = x[0]
        # v = x[1]
        # w = x[2]
        # B = x[3:]
        B = x

        data = [
            (B[0], z(n)),
            (B[1], fsd(n, (u, 1))),
            (B[2], fsd(n, (v, 1))),
            (B[3], fsd(n, (w, 1))),
            (B[4], fsd(n, (u, 2))),
            (B[5], fsd(n, (v, 2))),
            (B[6], fsd(n, (w, 2))),
            (B[7], fsd(n, (u, 1), (v, 1))),
            (B[8], fsd(n, (u, 1), (w, 1))),
            (B[9], fsd(n, (u, 3))),
            (B[10], fsd(n, (v, 3))),
            (B[11], fsd(n, (w, 3))),
            (B[12], fsd(n, (u, 2), (v, 1))),
        ]

        points, weights = untangle(data)

        exponents = get_all_exponents(n, degree)
        # flatten list
        exponents = numpy.array([item for sublist in exponents for item in sublist])

        def evaluate_all_monomials(x):
            return numpy.prod(x[..., None] ** exponents.T[:, None], axis=0).T

        flt = numpy.vectorize(float)
        exact_vals = flt([integrate_monomial_over_unit_nball(k) for k in exponents])

        A = evaluate_all_monomials(points.T)

        out = numpy.dot(A, weights)
        out -= exact_vals

        norm_v = numpy.sqrt(numpy.dot(out, out))
        # print()
        print(norm_v)
        # print()
        # for xx in x:
        #     print(f"{xx:.15e}")
        return norm_v

    x0 = [
        # 0.871_740_148_509_601,
        # 0.591_700_181_433_148,
        # 0.209_299_217_902_484,
        -0.369_608_422_804_220e02,
        -0.292_281_498_761_429,
        +0.981_554_121_166_593e-01,
        +0.200_417_005_906_264e02,
        +0.915_649_460_852_702e-03,
        +0.140_881_585_655_056,
        -0.109_681_663_185_532e02,
        -0.867_910_432_951_898e-02,
        +0.118_181_679_110_079,
        -0.172_723_379_038_583e-02,
        +0.153_215_767_717_862e-01,
        +0.614_931_311_140_891e01,
        +0.205_381_636_291_801e-02,
    ]

    out = minimize(f, x0, method="Powell", tol=1.0e-15, options={"maxiter": 20000})
    print(out.status, out.nfev)
    print(out.message)
    print()
    for x in out.x:
        print(f"{x:.15e}")
    assert out.success
    return


def stroud_e2r2_gauss():
    from quadpy.helpers import fsd

    def f(x):
        degree = 7
        data = [
            (x[0], fsd(2, (x[3], 1))),
            (x[1], fsd(2, (x[4], 1))),
            (x[2], fsd(2, (x[3], 1), (x[4], 1))),
        ]

        points = numpy.array(
            [
                [0.0, +x[3]],
                [0.0, -x[3]],
                [+x[3], 0.0],
                [-x[3], 0.0],
                #
                [0.0, +x[4]],
                [0.0, -x[4]],
                [+x[4], 0.0],
                [-x[4], 0.0],
                #
                #
                [+x[3], +x[4]],
                [+x[3], -x[4]],
                [-x[3], +x[4]],
                [-x[3], -x[4]],
            ]
        )

        points, weights = untangle(data)

        A = numpy.concatenate(orthopy.e2r2.tree(points.T, degree, symbolic=False))

        out = numpy.dot(A, weights)
        out[0] -= numpy.sqrt(numpy.pi)

        norm_v = numpy.sqrt(numpy.vdot(out, out))
        # print(norm_v)
        return norm_v

    # Cartesian product Gauss formula
    # sqrt6 = numpy.sqrt(6)
    # r, s = [numpy.sqrt((3 + p_m * sqrt6) / 2) for p_m in [+1, -1]]
    # A, B = [(5 - p_m * 2 * sqrt6) / 48 for p_m in [+1, -1]]
    # C = 1.0 / 48.0
    # A *= math.pi
    # B *= math.pi
    # C *= math.pi
    # x0 = [A, B, C, r, s]

    while True:
        x0 = numpy.random.rand(5) * 10 - 5

        print()
        print("x0", x0)

        out = minimize(
            f, x0, method="Nelder-Mead", tol=1.0e-15, options={"maxiter": 20000}
        )
        print(out.status, out.nfev, out.message, "Function value", out.fun)
        # assert out.success
        if abs(out.fun) < 1.0e-10:
            print()
            for x in out.x:
                print(f"{x:.15e}")
            break
    return


def rabinowitz_richter_4():
    from quadpy.e2r._helpers import _s4, _s8, _s40

    def f(x):
        degree = 13
        data = [
            (x[0], [[x[8], x[9]]]),
            (x[1], _s40(x[10])),
            (x[2], _s40(x[11])),
            (x[3], _s4(x[12])),
            (x[4], _s4(x[13])),
            (x[5], _s4(x[14])),
            (x[6], _s8(x[15], x[16])),
            (x[7], _s8(x[17], x[18])),
        ]
        points, weights = untangle(data)

        exponents = numpy.concatenate([partition(2, d) for d in range(degree + 1)])
        exact_vals = numpy.array([integrate_monomial_over_enr(k) for k in exponents])

        def fun(x):
            k = exponents.T
            # <https://stackoverflow.com/a/46689653/353337>
            s = x.shape[1:] + k.shape[1:]
            return (
                (x.reshape(x.shape[0], -1, 1) ** k.reshape(k.shape[0], 1, -1))
                .prod(0)
                .reshape(s)
            )

        A = fun(points.T).T
        print(A)
        print(exact_vals)
        print(sum(weights))
        out = numpy.dot(A, weights) - exact_vals
        nrm = numpy.sqrt(numpy.dot(out, out))
        print(nrm)
        exit(1)
        return nrm

    x0 = [
        +0.349_777_602_241_248_0e1,
        +0.442_580_256_591_559_0e-6,
        +0.455_340_971_239_599_4e-2,
        +0.277_530_326_587_565_2e-4,
        +0.331_277_792_488_418_2e1,
        -0.101_044_092_999_506_7e1,
        +0.112_721_370_308_653_4e-3,
        +0.492_114_301_738_741_9e2,
        #
        0.0,
        0.0,
        19.676_381_860_412_46,
        8.770_037_945_037_203,
        10.205_685_192_384_36,
        3.591_105_603_680_783,
        3.242_171_893_025_389,
        11.941_693_015_408_18,
        4.911_904_665_577_694,
        3.287_383_483_530_638,
        3.162_277_660_168_379,
    ]

    out = minimize(f, x0, method="Nelder-Mead", tol=1.0e-17)
    print(out.status, out.nfev)
    print(out.message)
    assert out.success
    print()
    for x in out.x:
        print(f"{x:.15e}")
    return


def stroud_1967_5():
    from quadpy.helpers import rd

    def f(x):
        degree = 5
        n = 7

        lmbda, xi, mu, gamma = x
        eta = 0
        A = 1 / 9
        B = 1 / 72
        C = B

        # data = [
        #     (B, rd(n, [(+lmbda, 1), (+xi, n - 1)])),
        #     (B, rd(n, [(-lmbda, 1), (-xi, n - 1)])),
        #     (C, rd(n, [(+mu, 2), (+gamma, n - 2)])),
        #     (C, rd(n, [(-mu, 2), (-gamma, n - 2)])),
        #     (2 * A, numpy.full((1, n), eta)),
        # ]
        # points, weights = untangle(data)
        # weights *= numpy.sqrt(numpy.pi) ** n

        data = [
            (B, rd(n, [(+lmbda, 1), (+xi, n - 1)])),
            (B, rd(n, [(-lmbda, 1), (-xi, n - 1)])),
            (C, rd(n, [(+mu, 2), (+gamma, n - 2)])),
            (C, rd(n, [(-mu, 2), (-gamma, n - 2)])),
            (2 * A, numpy.full((1, n), eta)),
        ]

        points, weights = untangle(data)
        weights *= numpy.sqrt(numpy.pi) ** n

        A = numpy.concatenate(orthopy.enr2.tree(points.T, degree, symbolic=False))

        out = numpy.dot(A, weights)
        out[0] -= numpy.sqrt(numpy.sqrt(numpy.pi)) ** n

        norm_v = numpy.sqrt(numpy.vdot(out, out))
        return norm_v

    x0 = [
        2.009505637083749e+00,
        2.774548295173737e-01,
        -1.062215595206724e+00,
        6.698352123613097e-01,
        # 2.009_505_6,
        # 0.277_454_83,
        # -1.062_215_60,
        # 0.669_835_21,
    ]

    out = minimize(
        f, x0, method="Powell", tol=1.0e-20, options={"maxiter": 20000}
    )
    print(out.status, out.nfev, out.message, "Function value", out.fun)
    assert out.success
    print()
    for x in out.x:
        print(f"{x:.15e}")
    return


if __name__ == "__main__":
    stroud_1967_5()
