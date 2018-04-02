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
      2017-12-21 DWW
"""

import numpy as np

from Parameter import C2K, K2C
from GenericMatter import Liquid


class Water(Liquid):
    """
    Physical and chemical properties of water
    """

    def __init__(self, identifier='Water', latex='$H_2O$', comment=None):
        """
        Args:
            identifier (string, optional):
                identifier of matter

            latex (string, optional):
                Latex-version of identifier. If None, identical with identifier

            comment (string, optional):
                comment on matter
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)
        self.version = '301017_dww'

        # reference point and operational range
        self.T.operational = [val for val in C2K([0, 100])]
        self.T.ref = C2K(15)
        self.T.val = self.T.ref
        self.p.operational = [val + 1.01325e5 for val in [0, 100e5]]
        self.p.ref = 1.01325e5
        self.p.val = self.p.ref

        # constants
        self.hMelt = 334.0e3
        self.hVap = 2270.0e3
        self.T_liq = C2K(0.0)
        self.T_boil = C2K(99.9839)
        self.composition['H2O'] = 100.

        # functions of temperature, presssure and spare parameter 'x'
        self.rho.calc = self._rho
        self.nu.calc = self._nu
        self.mu.calc = self._mu
        self.c_p.calc = self._c_p
        self.Lambda.calc = self._lambda
        self.c_sound.calc = self._c_sound
        self.E.calc = self._E

    def _rho(self, T, p=0., x=0.):
        """
                Density of water [kg/m3] versus temperature at 101.325 kPa
          1000 ***********-+----------+-----------+----------+----------++
               +          ******      +           +          +           +
           995 ++...............*****...................................++
               |           :         ****         :          :           |
           990 ++........................****...........................++
               |           :          :     ****  :          :           |
           985 ++..............................****.....................++
               |           :          :           :**        :           |
           980 ++....................................***................++
           975 ++.......................................***.............++
               |           :          :           :        ***           |
           970 ++............................................***........++
               |           :          :           :          :  **       |
           965 ++.................................................***...++
               |           :          :           :          :      ***  |
           960 ++......................................................**+
               +           +          +           +          +          **
           955 ++----------+----------+-----------+----------+----------++
               0           20         40          60         80         100
                                        T [deg C]


                    Density of water  [kg/m3] versus pressure at 20 deg C
          1001 ++---------+----------+-----------+----------+---------++
               +          +          +           +          +          +
               |          :          :           :          :          |
        1000.5 ++...................................................****
               |          :          :           :          :   *****  |
               |          :          :           :          ****       |
          1000 ++......................................*****..........++
               |          :          :           : *****    :          |
         999.5 ++..............................*****..................++
               |          :          :     ****  :          :          |
               |          :          :*****      :          :          |
           999 ++.................*****...............................++
               |          :   *****  :           :          :          |
               |          ****       :           :          :          |
         998.5 ++....*****............................................++
               | *****    :          :           :          :          |
               ***        +          +           +          +          +
           998 ++---------+----------+-----------+----------+---------++
               0          1          2           3          4          5
                                        p [MPa]

          Table rho( T in [degC], p = 101.325 kPa ) in [kg/m3]
                100 958.4
                 80 971.8
                 60 983.2
                 40 992.2
                 30 995.6502
                 25 997.0479
                 22 997.7735
                 20 998.2071
                 15 999.1026
                 10 999.7026
                  4 999.9720
                  0 999.8395
        """
        T = K2C(np.atleast_1d(T))
        if any(T < 0.):
            print('!!! T_celsius less than 0: ', [t for t in T if t < 0])
        if any(T > 100.):
            print('!!! T_celsius greater 100: ', [t for t in T if t > 100])
        if self.rho.p.absolute:
            pRef = 0.
        else:
            pRef = self.p.ref
        rho = 1e3 * (1 - (T + 288.9414) / (508929 * (T + 68.129630)) *
                         (T - 3.9863) * (T - 3.9863))
        E = self.E.calc(T, p, x)
        if E:
            rho /= 1. - (p - pRef) / max(E, 1e-20)
        return rho

    def _nu(self, T, p=0., x=0.):
        """
         Kinematic viscosity of water [mm2/s] versus temperature at 101.325 kPa
     1.8 *+------------+-------------+------------+-------------+------------++
         +*            +             +            +             +             +
     1.6 +**.................................................................++
         |  *          :             :            :             :             |
     1.4 ++..**..............................................................++
         |     **      :             :            :             :             |
     1.2 ++......**..........................................................++
         |         **  :             :            :             :             |
         |           **:             :            :             :             |
       1 ++............****..................................................++
         |             :  ****       :            :             :             |
     0.8 ++...................****...........................................++
         |             :          *****           :             :             |
     0.6 ++............................*******...............................++
         |             :             :       **********         :             |
     0.4 ++...........................................***************........++
         +             +             +            +             +   ***********
     0.2 ++------------+-------------+------------+-------------+------------++
         0             20            40           60            80          100
                                     T [°C]
        """
        return self._mu(T, p, x) / self._rho(T, p, x)

    def _c_p(self, T, p=0., x=0.):
        if T < self.T_liq:
            return 2108.
        elif T < self.T_boil:
            return 1e3 * (28.07 + T * (-0.2817 + T * (1.25e-3 +
                          T * (-2.48e-6 + T * 1.857e-9))))
        else:
            return 1996.

    def _mu(self, T, p=0., x=0.):
        A = 2.414e-5
        B = 247.8
        C = 140.
        return A * 10. ** (B / (T - C))

    def _lambda(self, T, p=0., x=0.):
        return -0.5752 + (T * (6.397e-3 - T * 8.151e-6))

    def _c_sound(self, T, p=0., x=0.):
        return 20.05 * np.sqrt(T)

    def _E(self, T, p=0., x=0.):
        return 2.2e9


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    import matplotlib.pyplot as plt

    def curve1(x, y, xl='x', yl='y'):
        plt.figure(figsize=(6, 4))
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.plot(x, y)
        plt.rcParams.update({'font.size': 14})
        plt.grid()
        plt.show()

    if 0 or ALL:
        foo = Water('')
        foo.plot(property='c_p')
        foo.rho.plot()
        foo.c_sound.plot()

    if 0 or ALL:
        T_celsius = np.linspace(0., 100., num=50)
        T_kelvin = C2K(T_celsius)
        rho = foo.rho(T=T_kelvin)
        nu = foo.nu(T_kelvin)
        Lambda = foo.Lambda(T_kelvin)
        curve1(T_celsius, rho, xl=r'$T$ [$\degree$C]', yl=foo.rho.latex)
        curve1(T_celsius, 1e6 * nu, xl=r'$T$ [$\degree$C]',
               yl=foo.nu.latex+r'$\,\cdot 10^6$')
        curve1(T_celsius, Lambda, xl=r'$T$ [$\degree$C]',
               yl=foo.Lambda.latex)

        print('rho(T=10C):', foo.rho.calc(C2K(10), 1e6))
