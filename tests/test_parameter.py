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
      2018-09-13 DWW
"""

import unittest
import sys
import os
import numpy as np

sys.path.append(os.path.abspath('..'))

from coloredlids.matter.parameter import Parameter, deg2rad, rad2deg


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        print('deg2rad(90):', deg2rad(90))
        print('rad2deg(pi*0.5):', rad2deg(np.pi*0.5))

    def test2(self):
        foo = Parameter(identifier='rhoLiq', latex=r'$\varrho_{liq}$',
                        unit='kg/m3')
        print(foo)
        print('-' * 40)

        foo.val = 3.3
        print(foo)
        print('-' * 40)

        print('foo.val, foo(), foo.ref:', (foo.val, foo(), foo.ref))
        foo.accuracy = ('1%FS', )
        foo.repeatability = ('-4ac', 11, 5)  # '-4ac' is invalid
        foo.certified = (0, 11)
        foo.operational = (-8.8, )
        print(foo)
        print('-' * 40)


if __name__ == '__main__':
    unittest.main()
