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
import os

from coloredlids.data.tolerance_range import ToleranceRange
from coloredlids.data.status import Status


class TestUM(unittest.TestCase):
    def setUp(self):
        print('///', os.path.basename(__file__))

    def tearDown(self):
        pass

    def test1(self):
        test = ToleranceRange()
    
        test.axes = ['U', 'I']
        test.reference = (230, 80)
        test.tolerated = ((0, 245), (0, 100))
        test.expected = ((4, 241), (0, 90))
        test.local = ((0, 300), (0, 1000))
        test.Global = ((0, 10e3), (0, 20e3))
        test.values = ((3, 355), (30, 50), (7, 66), (9, 77), (3, 33), (11, 99))
    
        stat = test.evaluate()
        print('stat:', stat)
    
        print('test.statuses:', [Status.symbol(x) for x in test.statuses])

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
