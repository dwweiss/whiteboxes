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
      2019-10-16 DWW
"""

import __init__
__init__.init_path()

import unittest
from coloredlids.data.compare_curves import CompareCurves


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
       
    def _test1(self):
        foo = CompareCurves()
        foo.gui = False
        foo.bars = 32
        foo.filenames = [
            './default_2019-08-16T22.13.10_spectrum_device0.data',
            './default_reference_spectrum_device0.data', 
            ]
        foo()

    def test2(self):
        foo = CompareCurves()
        foo.gui = True
        foo.bars = 32
        foo()

        
if __name__ == '__main__':
    unittest.main()
