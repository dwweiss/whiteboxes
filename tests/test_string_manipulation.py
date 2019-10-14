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
import os

from coloredlids.tools.string_manipulation import (ensure_hex_format, 
    scientific_to_standard_if_greater_1, reverse)


class TestUM(unittest.TestCase):
    def setUp(self):
        print('///', os.path.basename(__file__))

    def tearDown(self):
        pass

    def test1(self):
        def f():
            s = 'abc dde'
            length        = len(s)                # ==> 7
            repetitions   = s.count('d')          # ==> 2
            if 'dde' in s:
                index     = s.index('dde')        # ==> 4
            split         = s.split('c')          # ==> ['ab', ' dde']
            rev           = s[::-1]               # ==> 'edd cba'
            replaced      = s.replace('d', 'x')   # ==> 'abc xxe'
            capitilised   = ' '.join([x.capitalize() for x in s.split()])
                                                  # ==> 'Abc Dde'
            for key in sorted(locals()):
                print('{:>15}: {}'.format(key, locals()[key]))
        f()

        self.assertTrue(True)

    def test2(self):
        f = ensure_hex_format("#06x ")    # "06" is total string length
        x = 14
        s = format(x, f)                  # returns "0x000e"
        print('1 x:', x, ' f:', f, ' s:', s)

        f = ensure_hex_format("#11x")     # "06" is total string length
        x = -155
        s = format(x, f)                  # returns "0x000e"
        print('2 x:', x, ' f:', f, ' s:', s)
        print()

        self.assertTrue(True)

    def test3(self):
        S = ['1e3', '-.1e2', '1.2.34e3', '1.2.34D3', '1e-20', '1e-3', '1e20']
        for s in S:
            print('3 s:', s, 'replaced:', 
                  scientific_to_standard_if_greater_1(s))
        print()

        self.assertTrue(True)

    def test4(self):
        s = 'abcdef'
        print('4 s:', s, ' reverse:', reverse(s))
        print()
        
        self.assertTrue(True)
        

if __name__ == '__main__':
    unittest.main()
