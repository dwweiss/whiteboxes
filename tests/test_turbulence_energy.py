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
      2018-09-14 DWW
"""

import __init__
__init__.init_path()

import unittest
import matplotlib.pyplot as plt

from coloredlids.flow.turbulence_energy import \
    initial_turbulence_energy_and_dissipation


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        D = 25e-3
        nu = 1e-6
        v_seq = [0.1, 0.2, 0.5, 1, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9,
                 10]
        nu_seq = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]

        for nu in nu_seq:
            kk, ee = [], []
            for v in v_seq:
                k, eps = initial_turbulence_energy_and_dissipation(v, D, nu)
                kk.append(k)
                ee.append(eps)
            plt.plot(v_seq, kk, ls='--', label=r'$k(\nu:'+str(nu*1e6)+')$')
            plt.plot(v_seq, ee, label=r'$\varepsilon(\nu:'+str(nu*1e6)+')$')
        fontsize = 12
        plt.title(r'Axial velocity $v_z(r) = f(n, \nu)$')
        plt.rcParams.update({'font.size': fontsize})
        plt.rcParams['legend.fontsize'] = fontsize
        plt.xlabel('$v$ [m/s]')
        plt.ylabel(r'$k, \varepsilon$ [/]')
        plt.yscale('log', nonposy='clip')
        plt.grid()
        plt.legend(bbox_to_anchor=(1.1, 1.03), loc='upper left')
        plt.show()

        # same as above, y-axis is linear
        for nu in nu_seq:
            kk, ee = [], []
            for v in v_seq:
                k, eps = initial_turbulence_energy_and_dissipation(v, D, nu)
                kk.append(k)
                ee.append(eps)
            plt.plot(v_seq, kk, ls='--', label=r'$k(\nu:'+str(nu*1e6)+')$')
            # plt.plot(v_seq, ee, label=r'$\varepsilon(\nu:'+str(nu*1e6)+')$')
        fontsize = 12
        plt.title(r'Axial velocity $v_z(r) = f(n, \nu)$')
        plt.rcParams.update({'font.size': fontsize})
        plt.rcParams['legend.fontsize'] = fontsize
        plt.xlabel('$v$ [m/s]')
        plt.ylabel(r'$k, \varepsilon$ [/]')
        plt.grid()
        plt.legend(bbox_to_anchor=(1.1, 1.03), loc='upper left')
        plt.show()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
