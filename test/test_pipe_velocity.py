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
      2018-08-28 DWW
"""

import __init__
__init__.init_path()

import unittest
import numpy as np
import matplotlib.pyplot as plt

from coloredlids.flow.pipe_velocity import v_axial


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        D = 50e-3
        v_mean = 1
        r = np.linspace(0, D*0.5, num=100)
        n_seq = [3, 4, 6, 8, 10]
        nu_seq = [1e-6, 1e-2]
    
        for n in n_seq:
            for nu in nu_seq:
                vz = v_axial(v_mean=v_mean, d_pipe=D, r=r, nu=nu, n=n)
                plt.plot(vz, r, label='$n:'+str(n)+r',\ \nu: '+str(nu)+'$')
    
        fontsize = 12
        plt.title(r'Axial velocity $v_z(r) = f(n, \nu)$')
        plt.rcParams.update({'font.size': fontsize})
        plt.rcParams['legend.fontsize'] = fontsize
        plt.xlim(0, 2.2 * v_mean)
        plt.ylabel('$r$ [m]')
        plt.xlabel('$v_z$ [m/s]')
        plt.grid()
        plt.legend(bbox_to_anchor=(1.1, 1.03), loc='upper left')
        plt.show()
 
        self.assertTrue(True)
        
        
if __name__ == '__main__':
    unittest.main()

