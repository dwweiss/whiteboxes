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
      2018-09-16 DWW
"""

import unittest
import sys
import os

sys.path.append(os.path.abspath('..'))

from coloredlids.tools.date_to_seconds import date_to_seconds


class TestUM(unittest.TestCase):
    """
    Test of function date_to_seconds() 
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test1(self):
        date = '2019-08-14T12.34.56'
        date_ref = '2019-08-14T03.01.02'
        t = date_to_seconds(date)
        print('date, no reference:', date)
        print('t:', t, '[s]')

        dt = date_to_seconds(date, date_ref)
        print('date:', date, 'date_ref:', date_ref)
        print('dt:', dt, '[s]')
        print('difference in hours:', dt // 3600,
              ', minutes:', (dt % 3600) // 60, 
              ', seconds:', (dt % 3600 % 60))
        self.assertEqual(dt // 3600, 9)
        self.assertEqual((dt % 3600) // 60, 33)
        self.assertEqual((dt % 3600 % 60), 54)

    def test2(self):
        date = '2019-08-14T12:34:56'
        date_ref = '2019-08-14T03:01:02'
        t = date_to_seconds(date)
        print('date, no reference:', date)
        print('t:', t, '[s]')

        dt = date_to_seconds(date, date_ref)
        print('date:', date, 'date_ref:', date_ref)
        print('dt:', dt, '[s]')
        print('difference in hours:', dt // 3600,
              ', minutes:', (dt % 3600) // 60, 
              ', seconds:', (dt % 3600 % 60))
        self.assertEqual(dt // 3600, 9)
        self.assertEqual((dt % 3600) // 60, 33)
        self.assertEqual((dt % 3600 % 60), 54)
       
        
if __name__ == '__main__':
    unittest.main()
