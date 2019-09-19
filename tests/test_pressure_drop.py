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
      2018-09-12 DWW
"""

import __init__
__init__.init_path()

import unittest
import numpy as np
import matplotlib.pyplot as plt

from coloredlids.flow.pressure_drop import (pressure_drop, resistance_pipe, 
    poiseulle_colebrook, resistance_pipe_bend, 
    resistance_tapered_pipe_reduction, resistance_square_pipe_expansion,
    resistance_square_pipe_reduction, resistance_tapered_pipe_expansion,
    dp_in_red_mid_exp_out, dp_tapered_in_red_mid_exp_out)


D1, L1 = 20e-3, 20e-3
D2, L2 = 5e-3, 200e-3
eps_rough = 10e-6
nu = 5e-5
rho = 1000
rho_seq = (800, 900, 1000, 1100, 1200, 1300, 1400, 1600, 1800, 2000)
v1_seq = (0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10)

# DN80/2  -> equivalent pipe diameter: 56.57 mm
D1, D2, v1 = 40e-3, 20e-3, 1.
D1, D2, v1, r_bend, DN = 56.57e-3, 40e-3, 8.5, 113.5e-3, 80e-3
D1 = 80e-3

D3, L3 = D1, L1

eps_rough = 10e-6
k_functions = (resistance_square_pipe_reduction, 
               resistance_square_pipe_expansion,
               resistance_tapered_pipe_reduction, 
               resistance_tapered_pipe_expansion)


class TestUM(unittest.TestCase):

    def setUp(self):
        fontsize = 10
        plt.rcParams.update({'font.size': fontsize})
        plt.rcParams['legend.fontsize'] = fontsize

    def tearDown(self):
        pass

    def test1(self):
        s = 'Pressure loss in straight pipe'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        def f():
            rho = 1000
            nu = 1e-6
            D = 50e-3
            L = 1
            eps_rough = 10e-6
            v = 1
            Re = v * D / nu

            k = resistance_pipe(v=v, D=D, L=L, nu=nu, eps_rough=eps_rough)
            dp = pressure_drop(k=k, v=v, rho=rho)

            maxKey = max(map(len, locals()))
            for key, val in locals().items():
                if key != 'maxKey':
                    s = '{:>' + str(maxKey + 4) + '}: {}'
                    print(s.format(key, val))
        f()

        self.assertTrue(True)

    def test2(self):
        s = 'Pressure loss in straight->reduct->straight->expansion->straight'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        function = dp_in_red_mid_exp_out
        # function = dp_tapered_in_red_mid_exp_out

        print('+++ nu:', nu)

        # dp_set is array of [dp_total, dp1, ..., dp3]
        dp_set = [function(v1=v1, D1=D1, L1=L1,
                           D2=D2, L2=L2, D3=D3, L3=L3, nu=nu, rho=rho,
                           eps_rough=eps_rough) for v1 in v1_seq]
        dp_set = 1e-6 * np.atleast_2d(dp_set)

        for withoutTotalLoss in (True, False):
            labels = ('total', 'inlet', 'reduce', 'middle', 'expand', 'outlet')
            for i in range(int(withoutTotalLoss), len(dp_set[0])):
                if labels[i] == 'middle':
                    plt.plot(v1_seq, dp_set[:, i], label=labels[i], ls='--')
                else:
                    plt.plot(v1_seq, dp_set[:, i], label=labels[i])
            plt.xlabel('$v$ [m/s]')
            plt.ylabel(r'$\Delta p$ [MPa]')
            plt.legend(bbox_to_anchor=(0, 1), loc='upper left')
            plt.grid()
            plt.show()

        self.assertTrue(True)

    def test3(self):
        s = 'Pressure loss  tapered: straight->redu->straight->expan->straight'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        function = dp_tapered_in_red_mid_exp_out
        # function = dp_in_red_mid_exp_out

        id_seq = ('2', '3', '6', '10')
        D1_seq = (17.3e-3, 17.3e-3, 17.3e-3, 17e-3)
        L1_seq = (.5e-3, .5e-3, .5e-3, 0)
        D2_seq = (2.05e-3, 3e-3, 6e-3, 10e-3)
        L2_seq = (20e-3, 20e-3, 20e-3, 46.6e-3)
        D3_seq, L3_seq = D1_seq, L1_seq
        alpha12_seq = (30, 26.8, 16, 16)
        alpha23_seq = alpha12_seq
        eps_rough = 0.1e-6
        nu = 1e-6
        rho = 1000
        v1_seq = (0.1, 0.2, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

        print('+++ nu:', nu)
        dp_total_collect = []

        for i, identifier in enumerate(id_seq):
            L1, L2, L3 = L1_seq[i], L2_seq[i], L3_seq[i]
            D1, D2, D3 = D1_seq[i], D2_seq[i], D3_seq[i]
            alpha12, alpha23 = alpha12_seq[i], alpha23_seq[i]

            # dp_set is array of [dp_total, dp1, ..., dp3]
            dp_set = [function(v1=v1, D1=D1, L1=L1,
                               D2=D2, L2=L2, D3=D3, L3=L3,
                               alpha12=alpha12, alpha23=alpha23,
                               nu=nu, rho=rho, eps_rough=eps_rough)
                      for v1 in v1_seq]
            dp_set = 1e-6 * np.atleast_2d(dp_set)
            dp_total_collect.append(dp_set[:, 0])

            for withoutTotalLoss in [True, False]:
                labels = ['total', 'inlet', 'reduce', 'middle', 'expand',
                          'outlet']
                for j in range(int(withoutTotalLoss), len(dp_set[0])):
                    if labels[j] == 'middle':
                        plt.plot(v1_seq, dp_set[:, j], label=labels[j],
                                 ls='--')
                    else:
                        plt.plot(v1_seq, dp_set[:, j], label=labels[j])
                plt.title('Id:'+identifier)
                plt.xlabel('$v$ [m/s]')
                plt.ylabel(r'$\Delta p$ [MPa]')
                plt.legend(bbox_to_anchor=(0, 1), loc='upper left')
                plt.grid()
                plt.show()

        plt.title('All diameters')
        for i, dp_total in enumerate(dp_total_collect):
            plt.plot(v1_seq, dp_total, label='DN'+id_seq[i])
        plt.xlabel('$v$ [m/s]')
        plt.ylabel(r'$\Delta p$ [MPa]')
        plt.legend(bbox_to_anchor=(0, 1), loc='upper left')
        plt.grid()
        plt.show()

        self.assertTrue(True)

    def test4(self):
        Re_seq = np.linspace(1e0, 1e4, 10000)
        k = [poiseulle_colebrook(Re, D1, eps_rough) for Re in Re_seq]
        plt.plot(Re_seq, k)
        plt.xlabel('Re')
        plt.ylabel('$k_{straight}$ [/]')
        plt.show()

        self.assertTrue(True)

    def test5(self):
        # plot of k(r_bend), phiBend=const
        k = resistance_pipe_bend

        # D1 = 40e-3 ; r_bend = 112.5e-3
        x = np.linspace(0.01, 10.0, 100)
        y = [k(v=v, D=D1, r_bend=r_bend, phi_bend_deg=75) for v in x]
        plt.xlabel('$v$')
        plt.ylabel('$k_{bend}$ [/]')
        plt.plot(x, y)
        plt.show()
        x = np.linspace(0.05, 5.0, 1000) * 112.5e-3
        y = [k(v=v1, D=D1, r_bend=r, phi_bend_deg=75) for r in x]
        plt.plot(x, y)
        plt.xlabel('$r_{bend}$')
        plt.show()

        x = np.linspace(0.0, 90.0, 100)
        y = [k(v=5.0, D=D1, r_bend=100e-3, phi_bend_deg=phi) for phi in x]
        plt.xlabel(r'$\varphi_{bend}$')
        plt.plot(x, y)
        plt.show()

        self.assertTrue(True)

    def test6(self):
        # plot dp(nu)  for v-sequence
        for v in [0.05, 0.1, 0.2, 1, 10]:
            plt.xlabel(r'$\nu$ [mm$^2$/s]')
            plt.ylabel('$p$ [kPa]')
            nu_seq = np.linspace(1e-7, 1e-3, 1000)
            for k in k_functions:
                print('\n\n***', k.__name__)
                if str(k).find('Expansion') == -1:
                    v1 = v
                else:
                    v1 = v * (D1/D2)**2
                dp1 = np.array([pressure_drop(k(v1=v1, D1=D1, D2=D2, nu=nu,
                                              eps_rough=eps_rough), v1, rho)
                                for nu in nu_seq])
                s = str(k).split(sep=' ')[1][10:]
                plt.title('v_low: '+str(v)+', D1: '+str(D1)+', D2: '+str(D2) +
                          ', eps: '+str(eps_rough)+' v1_expan=v2_reduc')
                plt.plot(nu_seq*1e6, dp1*1e-3, label=s)
            plt.show()

        self.assertTrue(True)

    def test7(self):
        # dp(nu)  for a v-sequence
        for k in k_functions:
            print('\n\n***', k.__name__)
            if 1:
                nu_seq = [x * 1e-7 for x in range(1, int(1e5))]
                dp1 = [pressure_drop(k(v1=v1, D1=D1, D2=D2, nu=nu,
                                      eps_rough=eps_rough), v1, rho)
                       for nu in nu_seq]
                x = [x * 1e6 for x in nu_seq]
                y = [y * 1e-3 for y in dp1]
                plt.title('v: '+str(v1))
                plt.xlabel(r'$\nu$ [mm$^2$/s]')
                plt.ylabel('$p$ [kPa]')
                plt.plot(x, y)
                plt.show()

            if 1:
                plt.xlabel('$v$ [m/s]')
                plt.ylabel('$p$ [kPa]')
                v_seq = np.linspace(0.1, 10., 50)
                nu_seq = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
                for nu in nu_seq:
                    dp2 = [pressure_drop(k(v1=v1, D1=D1, D2=D2, nu=nu,
                                           eps_rough=eps_rough), v1, rho)
                           for v1 in v_seq]
                    y = [y * 1e-3 for y in dp2]
                    plt.plot(v_seq, y,
                             label='nu:'+str(round(nu*1e6, 1))+'e-6')
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.show()

            if 1:
                plt.xlabel(r'$Re \cdot 10^{-3}$ [/]')
                plt.ylabel('$p$ [kPa]')
                v1_seq = np.array([.1, .2, .4, .6, .8, 1, 2, 3, 4, 5, 6, 7, 8,
                                   9, 10])
                nu_seq = np.array([1e-7, 1e-6, 1e-5, 1e-4, 1e-3])
                for nu in nu_seq:
                    Re_seq = v1_seq * D1 / nu
                    dp_seq = [pressure_drop(k(v1=v1, D1=D1, D2=D2, nu=nu,
                              eps_rough=eps_rough), v1, rho) for v1 in v1_seq]
                    dp_kPa = 1e-3 * np.array(dp_seq)
                    plt.plot(Re_seq * 1e-3, dp_kPa,
                             label='nu:'+str(round(nu*1e6, 1))+'e-6')
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.show()

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
