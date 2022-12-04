"""
Author: Alex Fetzner
Date: 11/18/2022
Description: Quick, manual tests for functions
"""
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

from spline import Spline
from integration import integrateSpline, integrateSimpsons
from readerWriter import Writer, Reader
from utils import pairwise, sets_of_n, is_evenly_spaced
from multiIntegration import multiIntegrate


def main():
    # TestSpline()
    # TestIntegration()
    # TestReaderWriter()
    # TestUtils()
    TestMultiIntegration()


def TestSpline():
    xs = np.linspace(0, 5, 10)
    ys = np.sin(xs)

    spline = Spline.FromArrays(xs, ys)
    func = spline.ToFunc()

    _ = func(2.11)
    inter_xs = np.linspace(0, 5, 100)
    inter_ys = func(inter_xs)

    plt.scatter(inter_xs, inter_ys, s=2)
    plt.scatter(xs, ys, s=6)
    plt.show()


def TestIntegration():
    xs = np.linspace(0, 5, 100)
    ys = np.sin(xs)
    spline = Spline.FromArrays(xs, ys)
    integral = integrateSpline(spline)
    expected = 1 - np.cos(5)  # ~=0.71634
    print("Spline Integration")
    print(f"Expected={expected}")
    print(f"Actual  ={integral}")

    integral = integrateSimpsons(xs, ys)
    print("\nSimpson's Rule Integration")
    print(f"Expected={expected}")
    print(f"Actual  ={integral}\n\n")


def TestMultiIntegration():
    xs = np.linspace(0, 1, 100)
    ys = np.linspace(0, 1, 100)
    xy_mesh = np.meshgrid(xs, ys)
    plane = np.vectorize(lambda x, y: x+y)
    zs = plane(*xy_mesh)

    integral = multiIntegrate(xs, ys, zs)
    integral_y_first = multiIntegrate(xs, ys, zs, y_first=True)
    integral_simpsons = multiIntegrate(xs, ys, zs, use_simpsons=True)
    integral_y_first_simpsons = multiIntegrate(xs, ys, zs, y_first=True, use_simpsons=True)

    print("Multiple Integration")
    print(f"Spline, x-first: {integral}")
    print(f"Spline, y-first: {integral_y_first}")
    print(f"Simpsons, x-first: {integral_simpsons}")
    print(f"Simpsons, y-first: {integral_y_first_simpsons}\n")


def TestReaderWriter():
    def f(x, y):
        return (100 * x) + y
    xs = range(5)
    ys = range(0, 10, 2)
    zs = [f(x, y) for x, y in product(xs, ys)]

    path1 = "data/writer_test1.csv"
    writer1 = Writer.fromFunction(xs, ys, f)
    writer1.write(path1)

    path2 = "data/writer_test2.csv"
    writer2 = Writer.fromIterables(xs, ys, zs)
    writer2.write(path2)

    reader1 = Reader(path1)
    reader1.read()
    read_xs, read_ys, read_zs = reader1.toIterables()
    read_xyzs = list(reader1.toIterable())
    reader2 = Reader(path2)
    reader2.read()
    read2_xs, read2_ys, read2_zs = reader2.toIterables()

    do_break = False
    for i, ((x0, y0), x1, y1, z1, (x2, y2, z2), x3, y3, z3) in \
            enumerate(zip(product(xs, ys), read_xs, read_ys, read_zs, read_xyzs, read2_xs, read2_ys, read2_zs)):
        x0 = float(x0)
        y0 = float(y0)
        z0 = f(x0, y0)
        x3 = float(x3)
        y3 = float(y3)
        z3 = f(x3, y3)

        if i in range(0, 15, 6):
            fmt = "{:3s}\t{:8s}\t{:8s}\t{:8s}\t{:8s}"
            if i == 0:
                print(fmt.format("i", "source", "x", "y", "z"))
            print(fmt.format(str(i), "orig", str(x0), str(y0), str(z0)))
            print(fmt.format(str(i), "iters", str(x1), str(y1), str(z1)))
            print(fmt.format(str(i), "iter", str(x2), str(y2), str(z2)))
            print(fmt.format(str(i), "iter2", str(x3), str(y3), str(z3)))
            print()

        def close(a, b, c, d):
            margin = 0.000001
            return abs(a - b) < margin and abs(b - c) < margin and abs(d - c) < margin

        if not close(x0, x1, x2, x3):
            print(f"Line {i} x's do not match (orig={x0}, toIter={x1}, toIters={x2}")
            do_break = True
        if not close(y0, y1, y2, y3):
            print(f"Line {i} y's do not match (orig={y0}, toIter={y1}, toIters={y2}")
            do_break = True
        if not close(z0, z1, z2, z3):
            print(f"Line {i} z's do not match (orig={z0}, toIter={z1}, toIters={z2}")
            do_break = True
        if do_break:
            break

    if not do_break:
        print("All read lines match")


def TestUtils():
    any_fail = False

    # Test pairwise
    lst = [0, 1, 2, 3, 4, 5]
    expected = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
    result = list(pairwise(lst))
    if expected != result:
        print(f"pairwise failed. Expected {expected}, got {result}")
        any_fail = True

    # Test sets_of_n
    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    expected = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    result = list(sets_of_n(lst, 3))
    if expected != result:
        print(f"sets_of_n failed. Expected {expected}, got {result}")
        any_fail = True

    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    expected = [(0, 1), (2, 3), (4, 5), (6, 7), (8, None)]
    result = list(sets_of_n(lst, 2))
    if expected != result:
        print(f"sets_of_n failed. Expected {expected}, got {result}")
        any_fail = True

    # Test is_evenly_spaced
    lst = [0, 1, 2, 3, 4, 5, 6]
    expected = (True, 1)
    result = is_evenly_spaced(lst)
    if expected != result:
        print(f"is_evenly_spaced failed. Expected {expected}, got {result}")
        any_fail = True

    lst = [0, 1, 2, 7, 8, 9]
    expected = (False, 0)
    result = is_evenly_spaced(lst)
    if expected != result:
        print(f"is_evenly_spaced failed. Expected {expected}, got {result}")
        any_fail = True

    if not any_fail:
        print("All utils tests passed")
    print()


if __name__ == '__main__':
    main()
