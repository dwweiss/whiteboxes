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
import unittest

from whiteboxes.property.status import Status


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        for x in Status:
            print(x.name, ": '" + str(x.value) + "'")
        print()
    
        for x in Status:
            print(Status.symbol(x), Status.color(x))
        print('-' * 40)
    
        x = Status.FAIL
        print('status:', x)
        print('name:', x.name, ", symbol:'" + x.value[0] + "', color:", x.value[1])
        print('-' * 40)
    
        x = '-'
        print("Name(symbol='" + x + "'):", Status.name_('-'))
        print('-' * 40)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
