"""
Author: Alex Fetzner
Date: 11/19/2022
Description: given a function, compute its integral
"""
import numpy as np
from spline import Spline
from utils import pairwise


def IntegrateSpline(spline: Spline, start: float, stop: float):
    """Computes the 1D integral of quadratic spline function from start to stop"""
    lower, upper = spline.Domain()
    coefs = spline.Coefficients()
    if start < lower or stop > upper:
        raise ValueError(f"Integration over [{start}, {stop}] not defined on domain [{lower}, {upper}]")

    # integrals of t^2, t from x to x + delta
    int_x2 = np.vectorize(lambda a, b: (b**3 - a**3) / 3)
    int_x = np.vectorize(lambda a, b: (b**2 - a**2) / 2)

    integral = np.sum(int_x2(coefs.take(0, 1)))  # sum of integrals of ax^2 terms
    integral += np.sum(int_x(coefs.take(1, 1)))  # sum of integrals of bx terms
    integral += np.sum(coefs.take(2, 1))         # sum of integrals of c terms

