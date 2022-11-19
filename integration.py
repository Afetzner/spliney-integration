"""
Author: Alex Fetzner
Date: 11/19/2022
Description: given a function, compute its integral
"""
import numpy as np
from typing import Optional
from spline import Spline


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
