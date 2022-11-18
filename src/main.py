"""
Author: Alex Fetzner
Date: 11/18/2022
Description: Compare methods of integrating 3D volumes using splines and interpolation
"""
import matplotlib.pyplot as plt
import numpy

import topographyGenerator


height = 1
depth = 0.5
slope = 0.25
noise = 0.2
samples = 100
levels = 20
isThreeD = False


def main():
    # Generate the topography of the mountain
    topography_gen = topographyGenerator.volcano_topography(height, depth, slope, noise)
    topography = numpy.vectorize(topography_gen)

    # Evaluate the topography height at every position
    x = numpy.linspace(0, 1, samples)
    y = numpy.linspace(0, 1, samples)
    xy_mesh = numpy.meshgrid(x, y, sparse=True)
    z = topography(*xy_mesh)

    # Plot the topography
    if not isThreeD:
        plt.contourf(x, y, z, levels=levels)
        plt.axis('scaled')
        plt.colorbar()
    else:
        ax = plt.axes(projection="3d")
        ax.contour3D(x, y, z, levels=levels)

    plt.show()


if __name__ == '__main__':
    main()
