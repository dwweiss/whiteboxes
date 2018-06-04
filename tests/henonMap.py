"""
  Copyright (c) 2016-18 by Dietmar W Weiss

  This is free software; you can redistribute it and/or modify it
  under the terms of the GNU Lesser General Public License as
  published by the Free Software Foundation; either version 3.0 of
  the License, or (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this software; if not, write to the Free
  Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
  02110-1301 USA, or see the FSF site: http://www.fsf.org.

  Version:
      2017-12-31 DWW
"""

import numpy as np
import matplotlib.pyplot as plt


def henonMap(a=1.4, b=0.3, x=0.1, y=0.3, n=10000):
    """
    Computes the 3D function u = u(x, y, z) for a Henon map. It is a series of
    u(x, y) solutions and z can be interpreted as a time index.

    Args:
        a (float): tuning parameter of function
        b (float): tuning parameter of function
        x (float): initial value of first variable
        y (float): initial value of second variable
        n (int):   maximum number of time steps

    Returns:
        X, Y (array of float): x- and y-coordinates (size equals 'n')
        Z    (array of float): array of time step indices (size equals 'n')
    """
    X, Y = np.zeros(n), np.zeros(n)
    Z = np.array(range(n))
    for z in Z:
        x, y = y + 1. - a * x * x, b * x
        X[z], Y[z] = x, y
    Z = (Z - min(Z)) / (max(Z) - min(Z))

    return X, Y, Z


# Examples ####################################################################

if __name__ == "__main__":
    if 1:
        X, Y, Z = henonMap(a=1.4, b=0.3, n=1000)
        print(len(X))
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        plt.plot(X, Y, 'b,')
        plt.rcParams.update({'axes.titlesize': 'large'})
        plt.rcParams.update({'axes.labelsize': 'large'})
        plt.show()

        plt.xlabel('$z$')
        plt.ylabel('$x$')
        plt.plot(Z, X)
        plt.rcParams.update({'axes.titlesize': 'large'})
        plt.rcParams.update({'axes.labelsize': 'large'})
        plt.show()

        plt.xlabel('$z$')
        plt.ylabel('$y$')
        plt.plot(Z, Y)
        plt.rcParams.update({'axes.titlesize': 'large'})
        plt.rcParams.update({'axes.labelsize': 'large'})
        plt.show()
        try:
            import plotArrays
            plotArrays.plotTrajectory(X, Y, Z)
        except ImportError:
            print('??? Module plotArrays not imported')

    if 0:
        n = 10000
        X = np.linspace(-1.5, 1.5, n)
        Y = np.full_like(X, 0.0)
        X[0], Y[0] = 0.1, 0.3
        for i in range(len(X)):
            x, y, z = henonMap(x=X[i], n=n)
            X[i], Y[i] = x[-1], y[-1]

        plt.xlabel('$t$')
        plt.ylabel('$u$')
        plt.plot(X, Y, 'b,')
        plt.show()
