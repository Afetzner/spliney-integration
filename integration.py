"""
Author: Alex Fetzner
Date: 11/19/2022
Description: given a function, compute its integral
"""
import numpy as np
from typing import Optional
from spline import Spline
from utils import sets_of_n, is_evenly_spaced


def IntegrateSpline(spline: Spline, start: Optional[float] = None, stop: Optional[float] = None):
    """Computes the 1D integral of quadratic spline function from start to stop"""
    lower, upper = spline.Domain()
    if start is None:
        start = lower
    if stop is None:
        stop = upper
    if start < lower or stop > upper:
        raise ValueError(f"Integration over [{start}, {stop}] not defined on domain [{lower}, {upper}]")

    xs = spline.Intervals()
    delta_xs = np.diff(xs)
    coefs = spline.Coefficients()
    i = np.searchsorted(xs, start)   # lower sub interval index
    j = np.searchsorted(xs, stop)    # upper sub interval index

    # sum of integrals of ax^2 terms
    a_terms = coefs.take(0, 1)[i:j]
    integral = np.sum(np.dot(np.power(delta_xs, 3), a_terms)) / 3

    # sum of integrals of bx terms
    b_terms = coefs.take(1, 1)[i:j]
    integral += np.sum(np.dot(np.power(delta_xs, 2), b_terms)) / 2

    # sum of integrals of c terms
    c_terms = coefs.take(2, 1)[i:j]
    integral += np.sum(np.dot(delta_xs, c_terms))

    return integral


def IntegrateSimpsons(xs: np.array, ys: np.array, start: Optional[float] = None, stop: Optional[float] = None):
    """Integrate a list of data-points using simpson's rule"""
    if len(xs) != len(ys):
        raise ValueError(f"Dimension mismatch between xs ({len(xs)}) and ys ({len(ys)})")
    lower, upper = min(xs), max(xs)
    if start is None:
        start = lower
    if stop is None:
        stop = upper
    if start < lower or stop > upper:
        raise ValueError(f"Integration over [{start}, {stop}] not defined on domain [{lower}, {upper}]")
    is_even, spacing = is_evenly_spaced(xs)
    if not is_even:
        raise ValueError(f"Simpson's rule does not support non-evely-spaced data")

    i = np.searchsorted(xs, start)   # lower sub interval index
    j = np.searchsorted(xs, stop, side='right')    # upper sub interval index

    integral = 0
    for y_0, y_1, y_2 in sets_of_n(ys[i:j], 3):
        if y_0 is not None and y_1 is not None and y_2 is not None:
            integral += y_0 + (4 * y_1) + y_2
        else:
            integral += y_0 if y_0 else 0
            integral += y_1 if y_1 else 0
    return integral * spacing / 2
