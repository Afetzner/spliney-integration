"""
Author: Alex Fetzner
Date: 11/18/2022
Description: Write quick, manual tests for functions you wrote
"""
import numpy
import matplotlib.pyplot as plt
from spline import Spline


def main():
    TestSpline()


def TestSpline():
    xs = numpy.linspace(0, 5, 10)
    ys = numpy.sin(xs)

    spline = Spline.FromArrays(xs, ys)
    func = spline.ToFunc()

    _ = func(2.11)
    inter_xs = numpy.linspace(0, 5, 100)
    inter_ys = func(inter_xs)

    plt.scatter(xs, ys, s=5)
    plt.scatter(inter_xs, inter_ys, s=2)
    plt.show()


if __name__ == '__main__':
    main()
