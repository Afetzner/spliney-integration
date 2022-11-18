"""
Alex Fetzner
10/12/2022
Generates a mountainous terrain with perlin noise and a base shape
"""
import functools
import math
from typing import Callable
from perlin_noise import PerlinNoise


def volcano_topography(height: float, cavity_depth: float, slope: float, noise: float) \
        -> Callable[[float, float], float]:
    """
    Generates a rough, volcano-like topography over the domain [0, 1]x[0, 1]
    :param height: The height scale factor of the volcano, greater factor -> taller mountain
    :param cavity_depth: The cavity scale factor of the volcano, greater factor -> deeper cavity
    :param slope: The slope of the mountain, greater factor -> more lopsided mountain
    :param noise: The degree of Perlin-noise to be added, greater factor -> rougher
    :return: A function that gives the height of the volcano  at (x, y)
    """
    _noise = perlin_noise(noise)
    _base_shape = base_shape(height, cavity_depth, slope)
    offset = 0.5
    scale = 2

    def noisy_mountain(x: float, y: float) -> float:
        x = (x - offset) * scale
        y = (y - offset) * scale
        return _base_shape(x, y) + _noise(x, y)

    return noisy_mountain


def base_shape(height: float, cavity_depth: float, slope: float) \
        -> Callable[[float, float], float]:
    """
    Generates a cone-shaped surface with a centered cavity, like a volcano, with slope
    """
    if height < 0:
        raise ValueError(f"Base-shape height less than zero ({height})")
    if cavity_depth < 0 or cavity_depth > height:
        raise ValueError(f"Base-shape cavity depth greater than height or negative ({cavity_depth})")
    if slope < 0:
        raise ValueError(f"Base-shape cavity slope cannot be negative ({slope})")

    mountain = functools.partial(two_d_cone, height=height, narrowness=1)
    cavity = functools.partial(two_d_cone, height=height - cavity_depth, narrowness=10)

    def volcano_shape(x: float, y: float) -> float:
        return mountain(x, y) - cavity(x, y) - (slope * (x + y))

    return volcano_shape


def two_d_cone(x: float, y: float, height: float, narrowness: float) -> float:
    """
    Generates a rounded cone shape like exp(-x^2 - y^2)
    """
    if narrowness <= 0:
        raise ValueError(f"Cone narrowness must be positive")
    if height <= 0:
        raise ValueError(f"Cone height must be positive")
    return height * math.exp(-narrowness * ((x * x) + (y * y)))


def perlin_noise(factor: float) -> Callable[[float, float], float]:
    """
    Generates continuous pseudo-random data at any point (x, y)
    """
    noise1 = PerlinNoise(3)
    noise2 = PerlinNoise(6)
    noise3 = PerlinNoise(12)
    factor1 = 1 * factor
    factor2 = 0.5 * factor
    factor3 = 0.125 * factor

    def get_noise(x: float, y: float) -> float:
        return (noise1([x, y]) * factor1) + (noise2([x, y]) * factor2) + (noise3([x, y]) * factor3)

    return get_noise
