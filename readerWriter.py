"""
Alex Fetzner
11/21/2022
Functions for reading and writing 2D data from file
"""
from itertools import islice, product
from typing import Callable, Iterable, Tuple, List

import numpy as np

D2Function = Callable[[float, float], float]


class Reader:
    def __init__(self, path):
        self._path = path
        self._xs = []
        self._ys = []
        self._zs = []

    def read(self):
        with open(self._path, "r") as f:
            for line in f:
                x, y, z = line.split(',')
                x, y, z = float(x), float(y), float(z)
                self._xs.append(x)
                self._ys.append(y)
                self._zs.append(z)
        return self

    def toIterables(self) -> Tuple[Iterable[float], Iterable[float], Iterable[float]]:
        return self._xs, self._ys, self._zs

    def toIterable(self) -> Iterable[Tuple[float, float, float]]:
        return zip(self._xs, self._ys, self._zs)

    def toArrays(self) -> Tuple[np.array, np.array, np.array]:
        ny = self._ys[1:].index(self._ys[0]) + 1
        nx, nz = len(self._zs) // ny, len(self._zs)
        ys = np.fromiter(self._ys[:ny], dtype=float, count=ny)
        xs = np.fromiter(islice(self._xs, None, None, ny), dtype=float, count=nx)
        zs = np.array(self._zs, dtype=float).reshape((nx, ny))
        return xs, ys, zs

    _path: str
    _xs: List[float]
    _ys: List[float]
    _zs: List[float]


class Writer:
    @classmethod
    def fromFunction(cls, xs: Iterable[float], ys: Iterable[float], source: D2Function):
        domain = product(xs, ys)
        return cls(xs, ys, iter(map(lambda t: source(*t), domain)))

    @classmethod
    def fromIterables(cls, xs: Iterable[float], ys: Iterable[float], source: Iterable[float]):
        return cls(xs, ys, source)

    @classmethod
    def fromArrays(cls, xs: np.array, ys: np.array, zs: np.ndarray):
        nx, ny = len(xs), len(ys)
        nz = zs.shape[0] * zs.shape[1]
        if nz != nx * ny:
            raise ValueError(f"Dimension mismatch: x:{nx} *y:{ny} != z:{nz}")
        long_zs = map(lambda t: zs[t], product(range(nx), range(ny)))
        return cls(xs, ys, long_zs)

    def write(self, path: str, decimals: int = 6):
        with open(path, "w") as f:
            for (x, y), z in zip(product(self._xs, self._ys), self._source):
                print("{:.{d}f},{:.{d}f},{:.{d}f}".format(x, y, z, d=decimals), file=f)

    def __init__(self, xs: Iterable[float], ys: Iterable[float], source: Iterable[float]):
        self._xs = xs
        self._ys = ys
        self._source = source

    _xs: Iterable[float]
    _ys: Iterable[float]
    _source: Iterable[float]
