"""
Author: Alex Fetzner
Date: 11/18/2022
Description: Given a 2-dimensional array of (x,y)s, find a quadratic interpolation on the points
"""
import numpy as np
from math import floor
from typing import Iterable, Tuple, Callable
from itertools import pairwise
from functools import partial


class Spline:
    """
    A class for generating 1-dimensional quadratic splines of functions using
    a set of uniformly spaced data points

    Usage:
    S = Spline.FromIterable([(0, 5), (1, 3), (2, 4), ...])
    S = Spline.FromArrays(np.linspace(0, 50), np.array([5, 3, 4, ...])

    S.At(1.5)
    f = S.ToFunc()
    f(1.5)
    """
    _coefficients: np.ndarray
    _start: float       # minimum of x-values
    _spacing: float     # uniform spacing between x-values
    _count: int         # number of x/y-values

    def __init__(self, coefficients, start, spacing, count):
        self._coefficients = coefficients
        self._start = start
        self._spacing = spacing
        self._count = count

    @classmethod
    def FromIterable(cls, points: Iterable[Tuple[float, float]]):
        """Generates a Spline from a list of (x,y) tuples"""
        xs = np.Array(map(lambda x: x[0], points))
        if not _isUniformSpacing(xs):
            raise Exception("x-values must be uniformly spaced and ascending")
        start = xs[0]
        spacing = xs[1] - xs[0]
        count = len(xs)
        ys = np.Array(map(lambda x: x[1], points))
        coefs = _generateSplineCoefficients(ys, spacing)
        return Spline(coefs, start, spacing, count)

    @classmethod
    def FromArrays(cls, xs: np.array, ys: np.array):
        """Generate a Spline from a pair of numpy arrays"""
        if not _isUniformSpacing(xs):
            raise Exception("x-values must be uniformly spaced and ascending")
        start = xs[0]
        spacing = xs[1] - xs[0]
        count = len(xs)
        coefs = _generateSplineCoefficients(ys, spacing)
        return Spline(coefs, start, spacing, count)

    def At(self, x: float) -> float:
        """Evaluates the spline at a point x"""
        end = self._start + (self._spacing * self._count)
        if x < self._start or x > end:
            raise ValueError(f"Value x={x} must be between {self._start} and {end}")
        i = floor((x - self._start) // self._spacing)
        a = self._coefficients[i][0]
        b = self._coefficients[i][1]
        c = self._coefficients[i][2]
        return (a * x * x) + (b * x) + c

    def ToFunc(self) -> Callable:
        """Returns an ordinary callable function of the interpolated Spline"""
        return partial(self.At, self)

    def Coefficients(self) -> np.ndarray:
        """
        Returns the spline-coefficients where Arr[i][0], Arr[i][1], Arr[i][2]
        are the coefficients a_i, b_i, c_i respectively (Q_i(x) = a_ix^2 + b_ix = c_i)
        """
        return self._coefficients


def _isUniformSpacing(xs: np.array) -> bool:
    """Returns True if 'xs' is an array of ascending, equally spaced values"""
    spacing = xs[1] - xs[0]
    if spacing <= 0:
        return False
    for (a, _), (b, _) in pairwise(xs):
        if b - a != spacing:
            return False
    return True


def _generateSplineCoefficients(ys: np.array, spacing: float) -> np.ndarray:
    """Generates the coefficients a,b,c for each sub-interval of the spline"""
    n = len(ys)
    coefs = np.ndarray(shape=(n-1, 3), dtype=float)
    z_0, z_1 = 0, 0
    for i, (y_0, y_1) in enumerate(pairwise(ys)):
        z_1 = -z_0 + (2 * (y_1 - y_0) / spacing)
        coefs[i][0] = (z_1 - z_0) / (2 * spacing)
        coefs[i][1] = z_0
        coefs[i][2] = y_0
        z_0 = z_1
    return coefs
