"""
Author: Alex Fetzner
Date: 11/18/2022
Description: Compare methods of integrating 3D volumes using splines and interpolation
"""
import matplotlib.pyplot as plt
from readerWriter import Reader
import dataGenerator
from multiIntegration import multiIntegrate

functions = [("gauss", dataGenerator.generateGaussianData, dataGenerator.gaussPath),
             ("wavelet", dataGenerator.generateWaveletData, dataGenerator.waveletPath),
             ("asymmetric", dataGenerator.generateAsymmetricData, dataGenerator.asymmetricPath),
             ("mountain", dataGenerator.generateMountainData, dataGenerator.mountainPath)]


def main():
    plot_functions()
    integrate_functions()


def plot_functions():
    for _, _, path in functions:
        plot_from_path(path)


def plot_from_path(path):
    """Reads and plots a pre-saved data file"""
    levels = 20         # number of contour lines
    is_three_d = True   # contour plot or 3D contour projection

    reader = Reader(path)
    xs, ys, zs = reader.read().toArrays()
    if not is_three_d:
        plt.contourf(xs, ys, zs, levels=levels)
        plt.axis('scaled')
        plt.colorbar()
    else:
        ax = plt.axes(projection="3d")
        ax.contour3D(xs, ys, zs, levels=levels)

    plt.show()


def integrate_functions():
    print("Multiple Integration")
    for name, generator, _ in functions:
        xs, ys, zs = generator()
        integral_x_first_spline = multiIntegrate(xs, ys, zs)
        integral_y_first_spline = multiIntegrate(xs, ys, zs, y_first=True)
        integral_x_first_simpsons = multiIntegrate(xs, ys, zs, use_simpsons=True)
        integral_y_first_simpsons = multiIntegrate(xs, ys, zs, y_first=True, use_simpsons=True)

        print(f"Function: {name}")
        print(f"Spline, x-first: {integral_x_first_spline}")
        print(f"Spline, y-first: {integral_y_first_spline}")
        print(f"Simpsons, x-first: {integral_x_first_simpsons}")
        print(f"Simpsons, y-first: {integral_y_first_simpsons}\n")


if __name__ == '__main__':
    main()
