"""
Author: Alex Fetzner
Date: 12/3/2022
Description: Uses repeated single integration to accomplish multi-dimension integration
"""
import numpy as np

from integration import integrate


def multiIntegrate(xs: np.array, ys: np.array, zs: np.ndarray,
                   y_first: bool = False, use_simpsons: bool = False):
    """Computes the numerical 2D integration of the arrays using repeated single integration"""
    if y_first:
        xs, ys = ys, xs
        zs = zs.transpose()

    ny = len(ys)
    line_integrals = np.ndarray(shape=(ny,), dtype=float)
    for i in range(ny):
        line_integrals[i] = integrate(xs, zs[i], use_simpsons=use_simpsons)
    return integrate(ys, line_integrals, use_simpsons=use_simpsons)
