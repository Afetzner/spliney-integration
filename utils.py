"""
Author: Alex Fetzner
Date: 11/19/2022
Description: Commonly used functions for spliney-integration
"""
from typing import Iterable, Tuple
from itertools import tee, islice, zip_longest


def pairwise(iterable: Iterable) -> Iterable:
    """Emulates python.itertools.pairwise available in 3.10"""
    # From https://docs.python.org/3/library/itertools.html#itertools.pairwise
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def sets_of_n(iterable: Iterable, n: int) -> Iterable:
    """
    Returns an iterable of sets of n disjoint objects from the iterable
    n_sets([a, b, c, i, j, k, x, y, z, l], 3) -> (a,b,c), (i,j,k), (x,y,z) (l,None,None)
    """
    its = list(tee(iterable, n))
    for i in range(n):
        its[i] = islice(its[i], i, None, n)
    return zip_longest(*its, fillvalue=None)


def is_evenly_spaced(iterable: Iterable) -> Tuple[bool, float]:
    """Returns true if the iterable's values are evenly spaces, and the spacing. Else false and zero"""
    space = None
    for a, b in pairwise(iterable):
        if space is None:
            space = b - a
        elif b - a - space > 0.0001:
            return False, 0
    return True, space
