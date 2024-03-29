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
      2023-12-14 DWW
"""
import unittest

from whiteboxes.property.matter import Fluid, Metal, Solid
from whiteboxes.property.matter import Matter
from whiteboxes.property.parameter import Parameter
from whiteboxes.property.property import Property


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        # Example of generic matter
        mat = Matter(identifier='matter')

        # Add new Parameter 'p1'
        mat.p1 = Parameter(identifier='p1', unit='p1-unit', absolute=True,
                           latex=None, val=200, ref=120,
                           comment='define bounds of p1')
        mat.p1.operational = [100, 200]
        print(mat.p1)
        print('-' * 60)

        # Add new Property 'abc'
        mat.abc = Property(identifier='abc')
        mat.abc.calc = lambda T, p, x=0: 0.1 + 1e-3 * T - 1e-4 * p
        print(mat.abc)
        mat.abc.plot('title')
        print('-' * 60)

        self.assertTrue(True)

    def test2(self):
        # Example of Fluid
        fluid = Fluid(identifier='fluid')
        fluid.c_p.plot()
        fluid.plot('c_p')
        fluid.lambda_.plot()
        fluid.plot('lambda')

        fluid.plot('mu')
        fluid.plot('nu')
        fluid.plot('Pr')
        print('-' * 60)

        self.assertTrue(True)

    def test3(self):
        # Example of Fluid
        fluid = Fluid(identifier='fluid')
        fluid.rho.plot()
        fluid.rho(T=300)
        fluid.plot('rho')
        print('-' * 60)

        self.assertTrue(True)

    def test4(self):
        # Example of Fluid
        fluid = Fluid(identifier='fluid')
        fluid.lambda_.plot()
        fluid.c_p.plot()
        fluid.rho.plot()
        fluid.a.plot()
        print('cp:', fluid.c_p(T=300, p=0, x=0),
              'rho:', fluid.rho(T=300, p=0, x=0),
              'lambda:', fluid.lambda_(T=300, p=0, x=0),
              'a:', fluid.a(T=300, p=0, x=0))
        print('-' * 60)

        self.assertTrue(True)

    def test5(self):
        # Example of Solid
        solid = Solid(identifier='solid')
        solid.plot()
        print('-' * 60)

        self.assertTrue(True)

    def test6(self):
        # Example of Metal
        solid = Metal()
        solid.plot()
        print('-' * 60)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
