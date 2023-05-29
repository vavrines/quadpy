"""
Import data from Witherden/Vincent.
zip file: https://www.sciencedirect.com/science/article/pii/S0898122115001224
"""
import json
import os
import re

import numpy


def read_data_tri(filename):
    data = numpy.loadtxt(filename, dtype=float)
    if len(data.shape) == 1:
        data = numpy.array([data])

    points = data[:, :2]
    weights = data[:, 2]
    # The reference triangle is (-1, -1), (1, -1), (-1, 1). Transform the
    # points to barycentric coordinates.
    points += 1.0
    points *= 0.5
    points = numpy.array(
        [points[:, 0], points[:, 1], 1.0 - numpy.sum(points, axis=1)]
    ).T
    return points, weights * 0.5


def read_data_tet(filename):
    data = numpy.loadtxt(filename)
    if len(data.shape) == 1:
        data = numpy.array([data])
    points = data[:, :3]
    weights = data[:, 3]
    # Transform to barycentric coordinates.
    points += 1.0
    points *= 0.5
    points = numpy.array(
        [points[:, 0], points[:, 1], 1.0 - numpy.sum(points, axis=1)]
    ).T
    return points, weights * 0.75


def _grp_start_len(a, tol):
    '''Given a sorted 1D input array `a`, e.g., [0 0, 1, 2, 3, 4, 4, 4], this
    routine returns the indices where the blocks of equal integers start and
    how long the blocks are.
    '''
    # https://stackoverflow.com/a/50394587/353337
    m = numpy.concatenate([[True], numpy.abs((a[:-1] - a[1:])) > tol, [True]])
    idx = numpy.flatnonzero(m)
    return idx[:-1], numpy.diff(idx)


def data_to_json(degree, points, weights):
    d = {"s1": [], "s2": [], "s3": []}

    idx = numpy.argsort(weights)
    weights = weights[idx]
    points = points[idx]

    # get groups of equal weights
    for s, length in zip(*_grp_start_len(weights, 1.0e-12)):
        weight = weights[s]
        pts = points[s: s + length]
        if length == 1:
            d["s3"].append([weight])
        elif length == 3:
            # Symmetry group [[a, a, b], [a, b, a], [b, a, a]].
            # Find the equal value `a`.
            tol = 1.0e-12
            beta = pts[0] - pts[0][0]
            ct = numpy.count_nonzero(abs(beta) < tol)
            assert ct in [1, 2], beta
            val = pts[0][0] if ct == 2 else pts[0][1]
            d["s2"].append([weight, val])
        else:
            # Symmetry group perm([[a, b, c]]). Deliberately take the two smallest of a,
            # b, c as representatives.
            assert length == 6
            srt = numpy.sort(pts[0])
            d["s1"].append([weight, srt[0], srt[1]])

    d["degree"] = degree

    if len(d["s1"]) == 0:
        d.pop("s1")
    if len(d["s2"]) == 0:
        d.pop("s2")
    if len(d["s3"]) == 0:
        d.pop("s3")

    # Getting floats in scientific notation in python.json is almost impossible, so do
    # some work here. Compare with <https://stackoverflow.com/a/1733105/353337>.
    class PrettyFloat(float):
        def __repr__(self):
            return '{:.16e}'.format(self)

    def pretty_floats(obj):
        if isinstance(obj, float):
            return PrettyFloat(obj)
        elif isinstance(obj, dict):
            return dict((k, pretty_floats(v)) for k, v in obj.items())
        elif isinstance(obj, (list, tuple)):
            return list(map(pretty_floats, obj))
        return obj

    with open('wv{:02d}.json'.format(degree), "w") as f:
        string = pretty_floats(d).__repr__() \
            .replace("'", "\"") \
            .replace("[[", "[\n  [") \
            .replace("],", "],\n   ") \
            .replace("]],", "]\n  ],")
        f.write(string)

    return


def import_triangle():
    directory = 'zip/expanded/tri/'
    for k, file in enumerate(os.listdir(directory)):
        filename = os.fsdecode(file)
        out = re.match("([0-9]+)-([0-9]+)\.txt", filename)
        degree = int(out.group(1))
        x, weights = read_data_tri(os.path.join(directory, filename))
        data_to_json(degree, x, weights)
    return


def import_tet():
    filenames = [
        "1-1.txt",
        "2-4.txt",
        "3-8.txt",
        "5-14.txt",
        "6-24.txt",
        "7-35.txt",
        "8-46.txt",
        "9-59.txt",
        "10-81.txt",
    ]
    for k, filename in enumerate(filenames):
        out = re.match("([0-9]+)-([0-9]+)\.txt", filename)
        strength = out.group(1)
        print("elif degree == {}:".format(strength))
        print("    data = [")
        x, weights = read_data_tet(filename)
        data_to_code(x, weights)
        print(8 * " " + "]")
    return


if __name__ == "__main__":
    import_triangle()
    # import_tet()
