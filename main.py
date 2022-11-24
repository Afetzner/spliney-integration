"""
Author: Alex Fetzner
Date: 11/18/2022
Description: Compare methods of integrating 3D volumes using splines and interpolation
"""
import matplotlib.pyplot as plt

from readerWriter import Reader
import dataGenerator


def main():
    reader = Reader(dataGenerator.mountainPath)
    x, y, z = reader.read().toArrays()
    levels = 20
    is_three_d = True

    # Plot the topography
    if not is_three_d:
        plt.contourf(x, y, z, levels=levels)
        plt.axis('scaled')
        plt.colorbar()
    else:
        ax = plt.axes(projection="3d")
        ax.contour3D(x, y, z, levels=levels)

    plt.show()


if __name__ == '__main__':
    main()
