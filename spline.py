"""
Author: Alex Fetzner
Date: 11/18/2022
Description: Given a 2-dimensional array of (x,y)s, find a quadratic interpolation on the points
"""
import numpy as np
from typing import Iterable, Tuple, Callable
from functools import partial
from utils import pairwise


class Spline:
    """
    A class for generating 1-dimensional quadratic splines of functions

    Usage:
    S = Spline.FromIterable([(0, 5), (1, 3), (2, 4), ...])
    S = Spline.FromArrays(np.linspace(0, 50), np.array([5, 3, 4, ...])

    S.At(1.5)
    f = S.ToFunc()
    f(1.5)
    """
    _intervals: np.array    # x-values
    _coefficients: np.ndarray
    _start: float       # minimum of x-values
    _stop: float        # maximum of x-values
    _count: int         # number of x/y-values

    def __init__(self,
                 intervals: np.array,
                 coefficients: np.ndarray,
                 start: float,
                 stop: float,
                 count: int):
        self._intervals = intervals
        self._coefficients = coefficients
        self._start = start
        self._stop = stop
        self._count = count

    @classmethod
    def FromIterable(cls, points: Iterable[Tuple[float, float]]):
        """Generates a Spline from a list of (x,y) tuples"""
        xs = np.Array(map(lambda x: x[0], points))
        ys = np.Array(map(lambda x: x[1], points))
        return Spline.FromArrays(xs, ys)

    @classmethod
    def FromArrays(cls, xs: np.array, ys: np.array):
        """Generate a Spline from a pair of numpy arrays"""
        if not _isMonotoneIncreasing(xs):
            raise ValueError("x-values must be monotone increasing")
        start = xs[0]
        stop = xs[-1]
        count = len(xs)
        coefs = _generateSplineCoefficients(xs, ys)
        return Spline(xs, coefs, start, count, stop)

    def At(self, x: float) -> float:
        """Evaluates the spline at a point x"""
        if x < self._start or x > self._stop:
            raise ValueError(f"Value x={x} not in domain [{self._start}, {self._stop}]")
        i = self._intervals.searchsorted(x) - 1
        i = 0 if i == -1 else i
        x -= self._intervals[i]
        a = self._coefficients[i][0]
        b = self._coefficients[i][1]
        c = self._coefficients[i][2]
        return (a * x * x) + (b * x) + c

    def ToFunc(self) -> Callable[[np.array], np.array]:
        """Returns a vectorized callable function of the interpolated Spline"""
        return np.vectorize(partial(self.At))

    def Domain(self) -> Tuple[float, float]:
        return self._start, self._stop

    def Intervals(self) -> np.array:
        return self._intervals

    def Coefficients(self) -> np.ndarray:
        """
        Returns the spline-coefficients where Arr[i][0], Arr[i][1], Arr[i][2]
        are the coefficients a_i, b_i, c_i respectively (Q_i(x) = a_ix^2 + b_ix = c_i)
        """
        return self._coefficients


def _isMonotoneIncreasing(xs: np.array) -> bool:
    for a, b in pairwise(xs):
        if a >= b:
            return False
    return True


def _generateSplineCoefficients(xs: np.array, ys: np.array) -> np.ndarray:
    """Generates the coefficients a,b,c for each sub-interval of the spline"""
    n = len(ys) - 1
    coefs = np.ndarray(shape=(n, 3), dtype=float)
    boundary_condition = (ys[1] - ys[0]) / (xs[1] - xs[0])
    z_0, z_1 = boundary_condition, 0
    for i, ((x_0, y_0), (x_1, y_1)) in enumerate(pairwise(zip(xs, ys))):
        z_1 = -z_0 + (2 * (y_1 - y_0) / (x_1 - x_0))
        delta_z = z_1 - z_0
        coefs[i][0] = delta_z / (2 * (x_1 - x_0))
        coefs[i][1] = z_0
        coefs[i][2] = y_0
        z_0 = z_1
    return coefs
