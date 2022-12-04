"""
Author: ALex Fetzner
Date: 11/23/2022
Generate data to evaluate the integration methods
"""
import math

import numpy as np

from topographyGenerator import volcanoTopography
from readerWriter import Writer

mountainPath = "data/mountain.csv"
gaussPath = "data/gauss.csv"
waveletPath = "data/wavelet.csv"
asymmetricPath = "data/asymmetric.csv"


def main():
    generateMountainData()
    generateGaussianData()
    generateWaveletData()
    generateAsymmetricData()
    pass


def generateMountainData(do_write: bool = False):
    # integral unknown
    height = 1
    depth = 0.5
    slope = 0.25
    noise = 0.2
    samples = 100

    # Generate the topography of the mountain
    topography_gen = volcanoTopography(height, depth, slope, noise)
    topography = np.vectorize(topography_gen)

    # Evaluate the topography height at every position
    xs = np.linspace(0, 1, samples)
    ys = np.linspace(0, 1, samples)
    xy_mesh = np.meshgrid(xs, ys, sparse=True)
    zs = topography(*xy_mesh)

    if do_write:
        writer = Writer.fromArrays(xs, ys, zs)
        writer.write(mountainPath)
    return xs, ys, zs


def generateGaussianData(do_write: bool = False):
    # Expected integral = 1
    const = 1 / math.pi

    def gaussian_curve(x: float, y: float) -> float:
        r = (x * x) + (y * y)
        return np.exp(-r) * const

    gauss = np.vectorize(gaussian_curve)
    samples = 100
    xs = np.linspace(-10, 10, samples)
    ys = np.linspace(-10, 10, samples)
    xy_mesh = np.meshgrid(xs, ys, sparse=True)
    zs = gauss(*xy_mesh)

    if do_write:
        writer = Writer.fromArrays(xs, ys, zs)
        writer.write(gaussPath)
    return xs, ys, zs


def generateWaveletData(do_write: bool = False):
    # Integral unknown
    const = 4 * math.pi

    def wavelet_curve(x: float, y: float) -> float:
        r = (x * x) + (y * y)
        return (r <= 1) * np.sin(const * r) / (const * r)

    wave = np.vectorize(wavelet_curve)
    samples = 100
    xs = np.linspace(-1, 1, samples)
    ys = np.linspace(-1, 1, samples)
    xy_mesh = np.meshgrid(xs, ys, sparse=True)
    zs = wave(*xy_mesh)

    if do_write:
        writer = Writer.fromArrays(xs, ys, zs)
        writer.write(waveletPath)
    return xs, ys, zs


def generateAsymmetricData(do_write: bool = False):
    # Expected integral = 1
    const1 = 0.25 / (1 - np.exp(-2))
    const2 = 4 * math.pi
    const3 = 1 / math.pi

    def f(x: float) -> float:
        return (np.exp(-x) * const1) + (np.sin(const2 * x) * const3)

    def g(y: float) -> float:
        return (y-1) * (y-1) * (2-y) * 0.375

    func = np.vectorize(lambda x, y: f(x) + g(y))
    samples = 100
    xs = np.linspace(0, 2, samples)
    ys = np.linspace(0, 2, samples)
    xy_mesh = np.meshgrid(xs, ys, sparse=True)
    zs = func(*xy_mesh)

    if do_write:
        writer = Writer.fromArrays(xs, ys, zs)
        writer.write(asymmetricPath)
    return xs, ys, zs


if __name__ == '__main__':
    main()
