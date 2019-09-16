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
      2019-09-16 DWW
"""

import os
import sys
import unittest

sys.path.append(os.path.abspath('../..'))

from coloredlids.flow.flowbase import FlowIncompressible
from coloredlids.matter.parameter import C2K


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        foo = FlowIncompressible()
        foo.T.val = C2K(50)
        foo.v = 2.0
        print(foo)
        print('foo.T:', foo.T())

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
