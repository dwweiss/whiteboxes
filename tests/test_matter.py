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
      2018-09-17 DWW
"""

import unittest
import sys
import os

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../coloredlids'))
sys.path.append(os.path.abspath('../coloredlids/matter'))
from coloredlids.matter.genericmatter import C2K
from coloredlids.matter.matter import Matter


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        print('collection:', [m.identifier for m in Matter()('all')])

        matter = Matter()
        for mat in matter('all'):
            print('mat:', mat.identifier)
            if True:
                mat.plot()

    def test2(self):
        s = 'Water'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        collection = Matter()
        print('Collection:', collection)
        mat = collection('Water')
        mat.plot('c_p')

        rho = mat.plot('rho')
        Lambda = mat.Lambda(T=C2K(100))
        print('Lambda:', Lambda)
        c_p = mat.c_p(T=C2K(20), p=mat.p.ref)

        mat.plot('all')


if __name__ == '__main__':
    unittest.main()