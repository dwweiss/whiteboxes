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

  Version
      2018-09-17 DWW
"""

import __init__
__init__.init_path()

import unittest
import os

from coloredlids.matter.sutherland import sutherland_viscosity


class TestUM(unittest.TestCase):
    def setUp(self):
        print('///', os.path.basename(__file__))

    def tearDown(self):
        pass

    def test1(self):
        s = 'Sutherland viscosity (change relative to reference value)'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        mu_tilde = sutherland_viscosity("AIR", 100 + 273.15, 20 + 273.15, 1.)
        print('mu_tilde:', mu_tilde)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
