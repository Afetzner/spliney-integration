"""
Author: ALex Fetzner
Date: 11/23/2022
Generate data to evaluate the integration methods
"""
import numpy as np

from topographyGenerator import volcanoTopography
from readerWriter import Writer

mountainPath = "data/mountain.csv"
gaussPath = "data/gauss.csv"
asymmetricPath = "data/asymmetric.csv"


def main():
    generateMountainData()


def generateMountainData():
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

    writer = Writer.fromArrays(xs, ys, zs)

    writer.write(mountainPath)


if __name__ == '__main__':
    main()
