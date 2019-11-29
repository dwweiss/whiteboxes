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
      2019-11-27 DWW
"""

import __init__
__init__.init_path()

import numpy as np
import matplotlib.pyplot as plt
import unittest

from coloredlids.property.range import (Range, Scalar, in_range,  
    relative_to_absolute_range, in_range_abs_rel_error, in_range_full_scale)


class TestUM(unittest.TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test1(self):
        print('+++ Scalar')
        x: Scalar = 9.
        print(x)
        print('-' * 40)


    def test2(self):
        print('+++ constructor')
        x = Range('a','b','c')
        print(x)
        print('-' * 40)
        
        print('+++ set_range')
        x.set_range('-1','1%FS', '95%')
        print(x)
        x.set_range(-1)
        print(x)
        x.set_range('-1', None, '95%')
        print(x)
        x.set_range(None)
        print(x)
        x.set_range('90%')
        print(x)
        x.set_range('-1', None, '95%')
        print(x)
        print('-' * 40)
        
        print('+++ get_range')
        x = Range('a','b','c')
        print(x.get_range())
        print('-' * 40)
        
        print('+++ get_bound')
        print(x.get_bound('lo'))
        print(x.get_bound('up'))
        print(x.get_bound('distr'))
        print('-' * 40)
        
        print('+++ index [] (alternative indices and keys)')
        print(x)
        print(x['lo'], x['min'])
        print(x['hi'], x['up'], x['max'])
        print(x['distr'], x['distribution'], x['prob'])
        print(x['lo'])
        print(x['hi'])
        print(x['distr'])
        print(x[0])
        print(x[1])
        print(x[2])
        print('-' * 40)
        
        print('+++ getter')
        print(x.lo)
        print(x.up)
        print(x.distr)
        print('-' * 40)

        self.assertTrue(True)
        
        
    def test3(self):
        print('*** test: range.in_range()')
        
        ok = in_range(-2, (-10, 10))
        self.assertTrue(ok)

        ok = in_range(['-2', -100, 2], (-10, 10))
        self.assertFalse(ok)

        ok = in_range([-11, 3, 5], (-10, 10))
        self.assertFalse(ok)

        ok = in_range_full_scale(-2, Range('-20%' ,'21%'), Range(-10, 10))
        self.assertTrue(ok)

        ok = in_range_full_scale(-2, Range('20%' ,'21%'), Range(-10, 10))
        self.assertTrue(ok)

        ok = in_range_full_scale(-2, Range(-3 , '10%'), Range(None, 10))
        self.assertTrue(ok)

        ok = in_range_full_scale(-2, Range('3%' , '10%'), Range(None, 10))
        self.assertFalse(ok)


    def test4(self):
        print('*** test: range.in_range_abs_rel_error()')
        x = np.linspace(0, np.pi*2, 20)
        Y = np.sin(x) + 2
        y = Y + np.random.normal(scale=0.02, size=Y.size)
        dy = y - Y
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(5, 10))
        ax1.plot(x, y, label='y')
        ax1.plot(x, Y, label='Y')
        ax1.legend()
        ax1.grid()
        ax2.plot(x, dy, color='blue', label='abs')
        ax2.legend()
        ax2.legend()
        ax2.grid()
        ax3.plot(x, dy/Y*100, c='green', label='rel %')
        ax3.legend()
        ax3.grid()
        plt.show()
        
        print('\ndy.min dy.max', (dy.min(), dy.max()))
        print('dy/Y.min dy/Y.max %', ((dy/Y).min()*100, (dy/Y).max()*100))
        
        ok = in_range_abs_rel_error(y, Y, Range('-0.2', '0.3'))
        self.assertTrue(ok)

        ok = in_range_abs_rel_error(y, Y, Range(0.01, 0.02))
        self.assertFalse(ok)

        ok = in_range_abs_rel_error(y, Y, Range('-6%', '6%'))
        self.assertTrue(ok)


    def test5(self):
        print('+++ range.relative_to_absolute_range')
        print(relative_to_absolute_range(Range(-1, 1), Range(-11, 22)))
        print(relative_to_absolute_range(Range(None, 1), Range(-11, 22)))
        print(relative_to_absolute_range(Range(None, None), Range(-11, 22)))
        print(relative_to_absolute_range(Range('-1%', 2), Range(-11, 22)))
        print(relative_to_absolute_range(Range('1%', '-2%'), Range(-11, 22)))
        print(relative_to_absolute_range(Range(-1, '-2%'), Range(-11, 22)))
        print(relative_to_absolute_range(Range(-1, 'abc'), Range(-11, 22)))
        print(relative_to_absolute_range(Range(-1, 'abc'), Range(-11, '100%')))
        print(relative_to_absolute_range(Range('-10%', 7), Range(-3, 8)))
        
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
