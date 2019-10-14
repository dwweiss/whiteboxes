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
      2019-09-17 DWW
"""

import __init__
__init__.init_path()

import unittest
import os
import numpy as np

from coloredlids.numerics.tdma import tdma


class TestUM(unittest.TestCase):
    def setUp(self):
        print('///', os.path.basename(__file__))

        self.is_32bit = False

    def tearDown(self):
        pass

    def test1(self):
        from time import perf_counter
        import sys
        import matplotlib.pyplot as plt
    
        print('*** Begin test TDMA')
        n = 1 * 64
        n = int(1e6)
        lo = np.random.random(n)
        dg = np.random.random(n)
        up = np.random.random(n)
        rs = np.random.random(n)

        if self.is_32bit:
            lo, dg = np.float32(lo), np.float32(dg)
            up, rs = np.float32(up), np.float32(rs)
    
        if n <= 100:
            plt.plot(lo, label='lo')
            plt.plot(dg, label='dg')
            plt.plot(up, label='up')
            plt.plot(rs, label='rs')
            plt.legend()
            plt.show()
    
        print('+++ type:', rs.dtype)
        print('+++ type and shapes: lo dg up rs:', rs.dtype, lo.shape, 
              dg.shape, up.shape, rs.shape)
        print('NOTE: Code is not precompiled at start of first run')
    
        sys.stdout.flush()
        for i in range(10):
            start = perf_counter()
            x = tdma(lo, dg, up, rs)
            print('+++ t(' + str(i) + '):', (perf_counter() - start)*1e3, 
                  '[ms] dtype:', dg.dtype, x.dtype)
    
        del lo, dg, up, rs
    
        print('*** End test TDMA')

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
