"""
Alex Fetzner
11/21/2022
Functions for reading and writing 2D data from file
"""
import itertools
from typing import Callable, Iterable, Tuple, List

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

    _path: str
    _xs: List[float]
    _ys: List[float]
    _zs: List[float]


class Writer:
    @classmethod
    def fromFunction(cls, source: D2Function, xs: Iterable[float], ys: Iterable[float]):
        domain = itertools.product(xs, ys)
        return cls(xs, ys, iter(map(lambda t: source(*t), domain)))

    @classmethod
    def fromIterables(cls, source: Iterable[float], xs: Iterable[float], ys: Iterable[float]):
        return cls(xs, ys, source)

    def write(self, path: str, decimals: int = 6):
        with open(path, "w") as f:
            for (x, y), z in zip(itertools.product(self._xs, self._ys), self._source):
                print("{:.{d}f},{:.{d}f},{:.{d}f}".format(x, y, z, d=decimals), file=f)

    def __init__(self, xs: Iterable[float], ys: Iterable[float], source: Iterable[float]):
        self._xs = xs
        self._ys = ys
        self._source = source

    _xs: Iterable[float]
    _ys: Iterable[float]
    _source: Iterable[float]
