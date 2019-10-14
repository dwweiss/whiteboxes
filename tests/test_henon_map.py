"""
  Copyright (c) 2016- by Dietmar W Weiss

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
      2019-09-19 DWW
"""

import __init__
__init__.init_path()

import unittest
import os
import numpy as np
import matplotlib.pyplot as plt

from coloredlids.data.henon_map import henon_map


class TestUM(unittest.TestCase):
    def setUp(self):
        print("/// file:'" + os.path.basename(__file__) + "'")

    def tearDown(self):
        pass

    def test1(self):
        print("\n/// test:'" + self.id()[self.id().rfind('.')+1:] + "'")
        
        X, Y, Z = henon_map(a=1.4, b=0.3, n=1000)
        print('+++ n:', len(X))
        
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
            from grayboxes.plot import plot_trajectory
            plot_trajectory(X, Y, Z)
        except ImportError:
            print("??? Module 'plot' not imported")

        self.assertTrue(True)

    def test2(self):
        print("\n/// test:'" + self.id()[self.id().rfind('.')+1:] + "'")

        n = 1000
        X = np.linspace(-1.5, 1.5, n)
        Y = np.full_like(X, 0.0)
        X[0], Y[0] = 0.1, 0.3
        for i in range(len(X)):
            x, y, z = henon_map(x=X[i], n=n)
            X[i], Y[i] = x[-1], y[-1]

        plt.xlabel('$t$')
        plt.ylabel('$u$')
        plt.plot(X, Y, 'b,')
        plt.show()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
