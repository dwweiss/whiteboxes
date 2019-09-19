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

from coloredlids.flow.flowbase import FlowBase
from coloredlids.matter.parameter import C2K
from coloredlids.matter.liquids import HydraulicOil


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        foo = FlowBase()
        foo.T.val = C2K(50)
        foo.v = 2.0

        print('foo.T:', foo.T())
        print('foo.T:', foo.T.val)
        print('*' * 60)

        self.assertTrue(foo.T.val == foo.T())

    def test2(self):
        foo = FlowBase(w_h_pipe = (4e-3, 5e-3))

        foo.T.val = C2K(50)
        foo.v = 1.
        print(foo)
        print('*' * 60)

        self.assertTrue(True)

    def test3(self):
        foo = FlowBase(d_pipe=25e-3)

        foo.T.val = C2K(50)
        foo.v = 1.
        print(foo)
        print('*' * 60)

        self.assertTrue(True)

    def test4(self):
        foo = FlowBase(fluid=HydraulicOil())

        foo.T.val = C2K(50)
        foo.v = 1.
        print(foo)
        print('*' * 60)

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
