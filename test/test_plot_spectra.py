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
      2019-10-17 DWW
"""

import __init__
__init__.init_path()

import unittest
import sys

from coloredlids.instruments.plot_spectra import plot_spectra


class TestUM(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test1(self):
        if 1 < len(sys.argv) < 4:
            print("expected argv: 'path identifier date_time'")
            self.assertTrue(False)
            
        if len(sys.argv) == 4:
            path = sys.argv[1]
            identifier = sys.argv[2]
            date_time = sys.argv[3]     
        else:        
            path = r'../../moos/spectrography/unittest/'       
            identifier = 'default'
            date_time = '2019-08-16T22.19.26'
        
        print('path, identifier, date_time:', path, identifier, date_time)
                
        plot_spectra(path, identifier, date_time)
            
        self.assertTrue(True)
            

if __name__ == '__main__':
    unittest.main()
