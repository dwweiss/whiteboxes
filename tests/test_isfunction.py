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

from coloredlids.tools.isfunction import is_function


def f():
    return 0.0

class C(object):
    def f(self): 
        pass


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        c = C()
    
        for x in [f, lambda a: 1.0, c.f, c]:
            print('x:', str(x)[:str(x).index('at')-1] + str(x)[-1],
                  '=> is_function:', is_function(x))
        print()
    
        n = None
        i = 1
        b = True
        d = 1.0
        l = [1, 2]
        t = (1, 2)
        s = 'abc'
        for x in [n, i, b, d, l, t, s]:
            print('x:', x, '=> isFunction:', is_function(x))
    
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
