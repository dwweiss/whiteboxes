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
      2019-10-18 DWW
"""

import __init__
__init__.init_path()

import unittest

from coloredlids.data.plot_csv_sequences import plot_csv_sequences


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
                               
    def test1(self):
        ok = plot_csv_sequences(
            path='../../moos/instrument/191',
            identifier='flowcell',
            x_iso=[350, 500, 650, 800, 1100, 1200, 1300, 1400], 
            p1_file='T_sys.csv', p2_file='p_sys.csv', p3_file='Q_sys.csv',
            )
        
        self.assertTrue(ok)
        

if __name__ == '__main__':
    unittest.main()
