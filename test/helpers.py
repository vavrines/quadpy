import numpy

from quadpy.helpers import get_all_exponents


def check_degree(quadrature, exact, dim, max_degree, tol):
    exponents = get_all_exponents(dim, max_degree)
    # flatten list
    exponents = numpy.array([item for sublist in exponents for item in sublist])

    flt = numpy.vectorize(float)
    exact_vals = flt([exact(k) for k in exponents])

    def evaluate_all_monomials(x):
        # Evaluate monomials.
        # There's a more complex, faster implementation using matmul, exp, log.
        # However, this only works for strictly positive `x`, and requires some
        # tinkering. See below and
        # <https://stackoverflow.com/a/45421128/353337>.
        return numpy.prod(x[..., None] ** exponents.T[:, None], axis=0).T

    vals = quadrature(evaluate_all_monomials)

    # check relative error
    err = abs(exact_vals - vals)
    is_smaller = err < (1 + abs(exact_vals)) * tol

    if numpy.all(is_smaller):
        return max_degree, numpy.max(err / (1 + abs(exact_vals)))

    k = numpy.where(~is_smaller)[0]
    # Return the max error for all exponents that are one smaller than the max_degree.
    # This is because this functions is usually called with target_degree + 1.
    idx = numpy.sum(exponents, axis=1) < max_degree
    return (
        numpy.sum(exponents[k[0]]) - 1,
        numpy.max(err[idx] / (1 + abs(exact_vals[idx]))),
    )


def find_equal(schemes):
    tol = 1.0e-13
    n = len(schemes)
    for i in range(n):
        found_equal = False
        for j in range(n):
            if schemes[i].name == schemes[j].name:
                continue
            if len(schemes[i].points) != len(schemes[j].points):
                continue
            # Check if the point sets are equal
            x = numpy.column_stack([schemes[i].weights, schemes[i].points])
            y = numpy.column_stack([schemes[j].weights, schemes[j].points])
            is_equal = True
            for x_i in x:
                diff = y - x_i
                diff = numpy.min(numpy.sum(diff ** 2, axis=-1))
                if diff > tol:
                    is_equal = False
                    break
            if is_equal:
                found_equal = True
                a = f"'{schemes[i].name}'"
                try:
                    a += f" ({schemes[i].citation.year})"
                except AttributeError:
                    pass
                b = f"'{schemes[j].name}'"
                try:
                    b += f" ({schemes[j].citation.year})"
                except AttributeError:
                    pass
                print(f"Schemes {a} and {b} are equal.")
        if found_equal:
            print()
