"""
Author: Alex Fetzner
Date: 11/18/2022
Description: Write quick, manual tests for functions you wrote
"""
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

from spline import Spline
from integration import IntegrateSpline
from readerWriter import Writer, Reader


def main():
    # TestSpline()
    # TestIntegration()
    TestReaderWriter()


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
    integral = IntegrateSpline(spline)
    expected = 1 - np.cos(5)  # ~=0.71634
    print("Integration")
    print(f"Expected={expected}")
    print(f"Actual  ={integral}")


def TestReaderWriter():
    def f(x, y):
        return (100 * x) + y
    xs = range(5)
    ys = range(0, 10, 2)

    path = "data/writer_test.txt"
    writer = Writer.fromFunction(f, xs, ys)
    writer.write(path)

    reader = Reader(path)
    reader.read()
    read_xs, read_ys, read_zs = reader.toIterables()
    read_xyzs = list(reader.toIterable())

    do_break = False
    for i, ((x0, y0), x1, y1, z1, (x2, y2, z2)) in enumerate(zip(product(xs, ys), read_xs, read_ys, read_zs, read_xyzs)):
        x0 = float(x0)
        y0 = float(y0)
        z0 = f(x0, y0)

        if i in range(0, 15, 6):
            fmt = "{:3s}\t{:8s}\t{:8s}\t{:8s}\t{:8s}"
            if i == 0:
                print(fmt.format("i", "source", "x", "y", "z"))
            print(fmt.format(str(i), "orig", str(x0), str(y0), str(z0)))
            print(fmt.format(str(i), "iters", str(x1), str(y1), str(z1)))
            print(fmt.format(str(i), "iter", str(x2), str(y2), str(z2)))
            print()

        def close(a, b, c):
            margin = 0.000001
            return abs(a - b) < margin and abs(a - c) < margin and abs(b - c) < margin

        if not close(x0, x1, x2):
            print(f"Line {i} x's do not match (orig={x0}, toIter={x1}, toIters={x2}")
            do_break = True
        if not close(y0, y1, y2):
            print(f"Line {i} y's do not match (orig={y0}, toIter={y1}, toIters={y2}")
            do_break = True
        if not close(z0, z1, z2):
            print(f"Line {i} z's do not match (orig={z0}, toIter={z1}, toIters={z2}")
            do_break = True
        if do_break:
            break

    if not do_break:
        print("All read lines match")


if __name__ == '__main__':
    main()
