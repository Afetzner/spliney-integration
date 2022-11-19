"""
Author: Alex Fetzner
Date: 11/19/2022
Description: Commonly used functions for spliney-integration
"""
from typing import Iterable
from itertools import tee


def pairwise(iterable: Iterable):
    """Emulates python.itertools.pairwise available in 3.10"""
    # From https://docs.python.org/3/library/itertools.html#itertools.pairwise
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
