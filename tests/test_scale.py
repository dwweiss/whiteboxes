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
      2019-09-18 DWW
"""

import __init__
__init__.init_path()

import unittest
import numpy as np

from coloredlids.data.scale import scale, batch_normalize, batch_denormalize


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        X = np.array([39, 50, 41, 100, 90])
        x = scale(X, lo=-1, hi=2)
        print('1 X:', X, 'x:', x)

        x = scale(X)
        print('2 X:', X, 'x:', x)

        self.assertTrue(True)

    def test2(self):
        X = np.array([39, 50, 41, 100, 90])
        x = batch_normalize(X, eps=1000)
        print('3 X:', X, 'x:', x)

        x = batch_denormalize(x)
        print('4 x:', x)
        print('5 x == X:', all(x == X))        

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
