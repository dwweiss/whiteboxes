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
      2019-03-18 DWW
"""

import __init__
__init__.init_path()

import unittest

from coloredlids.data.inrange import in_range


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        self.assertFalse(in_range(2, [3, 4]))
        self.assertFalse(in_range(None, [1, 4]))
        self.assertTrue(in_range(2, [1, 4]))
        self.assertFalse(in_range(2, [3, 4], 3, (2, 9)))
        self.assertTrue(in_range(2, [1, 4], 3, (None, 9), 3, (None, None)))
        self.assertFalse(in_range(None, [1, 4], None, (None, 9), None, (7, 0)))


if __name__ == '__main__':
    unittest.main()
