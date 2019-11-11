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

from coloredlids.tools.extract_timestamp import extract_timestamp


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
       
    def test1(self):
        for s in ['default_2019-08-16Z22.13.10_aaa_2019-08-16T23.12.17_spect',
                  'default_2019-08-16T23.14.11_spectrum',
                  '2019-08-16T23.14.11_spectrum',
                  'abc2019-08-16T23.14.11',
                  '2019-08-16T23.14.11',
                  '2019-08-16T23:14:11',
                  '2019-08-16T23.14.1',
                  '2019-08-16T01:15_spectrum',
                  'default_2019-08-16T01:15:12_spectrum']:
            stamp = extract_timestamp(s)
            print("stamp:'" + stamp + "', s: '" + s + "'")
        
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
