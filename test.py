"""
Author: Alex Fetzner
Date: 11/18/2022
Description: Write quick, manual tests for functions you wrote
"""
import numpy as np
import matplotlib.pyplot as plt

from spline import Spline
from integration import IntegrateSpline


def main():
    TestSpline()
    TestIntegration()


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


if __name__ == '__main__':
    main()
