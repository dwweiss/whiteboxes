"""
  Copyright (c) 2016- by Dietmar W Weiss

  This is free software; you can redistribute it and/or modify it
  under the terms of the GNU Lesser General Public License as
  published by the Free Software Foundation; either version 3.0 of
  the License, or (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  Lesser General Public Licqense for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this software; if not, write to the Free
  Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
  02110-1301 USA, or see the FSF site: http://www.fsf.org.

  Version:
      2018-09-17 DWW
"""
import unittest

from whiteboxes.matter.matters import Matters
from whiteboxes.property.conversion import C2K


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        print('collection:', [m.identifier for m in Matters()('all')])

        matters = Matters()
        for mat in matters('all'):
            print('mat:', mat.identifier)
            if True:
                mat.plot()

        self.assertTrue(True)

    def test2(self):
        s = 'Water'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        collection = Matters()
        print('Collection:', collection)
        mat = collection('Water')
        mat.plot('c_p')

        rho = mat.plot('rho')
        print('rho:', rho)
        lambda_ = mat.lambda_(T=C2K(100))
        print('lambda_:', lambda_)
        c_p = mat.c_p(T=C2K(20), p=mat.p.ref)
        print('c_p:', c_p)

        mat.plot('all')

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
