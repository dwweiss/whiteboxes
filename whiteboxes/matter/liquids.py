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
      2019-11-25 DWW
"""

import numpy as np
from scipy.interpolate import interp2d
from typing import Optional

try:
    from conversion import C2K, K2C
    from generic import Liquid
    from range import Range
except:
    from coloredlids.property.conversion import atm, C2K, K2C
    from coloredlids.property.matter import Liquid
    from coloredlids.property.range import Range


class Diesel(Liquid):
    """
    Thermophysical properties of diesel fuel

    Reference:
        [NIT11] I Nita and S Geacai: Study of density and viscosity variation
            with temperature for fules used for Diesel engine. Ovidius Univ.
            Annals of Chemistry, Vol. 22, No. 1, pp.357-61, 2011
    """

    def __init__(self, identifier: str='Diesel',
                 latex: Optional[str]=None,
                 comment: Optional[str]=None) -> None:
        super().__init__(identifier=identifier)
        """
        Args:
            identifier:
                identifier of matter

            latex:
                Latex-version of identifier. If None, identical with identifier

            comment:
                comment on matter
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)
        self.version = '09.19_dww'

        # reference point and operational range
        self.T.operational = Range(C2K(0), C2K(100))
        self.T.ref = C2K(15)
        self.T.val = self.T.ref
        self.p.operational = Range(0. + atm(), 100e5 + atm())
        self.p.ref = atm()
        self.p.val = self.p.ref

        # constants
#        self.hMelt =
#        self.hVap =
#        self.T_liq = C2K(  )
#        self.T_boil = C2K(   )
        self.composition['C12H24'] = 100  # TODO

        # functions of temperature, presssure and spare parameter 'x'
        self.rho.calc = self._rho
        self.nu.calc = self._nu
        self.mu.calc = self._mu
        self.c_p.calc = self._c_p
        self.k.calc = self._k
#        self.c_sound.calc = self._c_sound
#        self.E.calc = self._E

    def _rho(self, T, p=1e5, x=0):
        a, b = -0.0007, 0.8939
        rho_g_m3 = a * K2C(T) + b
        return rho_g_m3 * 1e3

    def _nu(self, T, p=1e5, x=0):
        return self._mu(T, p, x) / self._rho(T, p, x)

    def _mu(self, T, p=1e5, x=0):
        e, f, g, h = -1e-4, 0.0029, -0.2195, 8.159
        T_C = K2C(T)
        eta_mm2_s = ((((e * T_C) + f) * T_C) + g) * T_C + h
        return eta_mm2_s * 1e-6

    def _c_p(self, T, p=1e5, x=0):
        return 1750

    def _k(self, T, p=1e5, x=0):
        return 0.15


class HydraulicOil(Liquid):
    """
    Thermophysical properties of hydraulic oil
    """

    def __init__(self, identifier: str='hydraulic_oil',
                 latex: Optional[str]=None,
                 comment: Optional[str]=None) -> None:
        super().__init__(identifier=identifier)
        """
        Args:
            identifier:
                identifier of matter

            latex:
                Latex-version of identifier. 
                If None, latex is identical with identifier

            comment:
                comment on matter
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)
        self.version = '160118_dww'

        # reference point and operational range
        self.T.operational = Range(C2K(0), C2K(100))
        self.T.ref = C2K(15)
        self.T.val = self.T.ref
        self.p.operational = Range(0. + atm(), 100e5 + atm())
        self.p.ref = atm()
        self.p.val = self.p.ref

        # constants
#        self.hMelt =
#        self.hVap =
#        self.T_liq = C2K(  )
#        self.T_boil = C2K(   )
        self.composition['C12H24'] = 100  # TODO

        # functions of temperature, pressure and spare parameter 'x'
        self.rho.calc = self._rho
        self.nu.calc = self._nu
        self.mu.calc = self._mu
        self.c_p.calc = self._c_p
        self.k.calc = self._k
#        self.c_sound.calc = self._c_sound
#        self.E.calc = self._E

    def _c_p(self, T, p=1e5, x=0):
        Tp = C2K(np.array([20, 40, 60, 80, 100]))
        Pp = np.array([0.1, 10.1, 20.1]) * 1e6
        Up = np.array([[1939.6, 1936.4, 1933.4],
                       [2028.2, 2024.7, 2021.4],
                       [2116.9, 2112.9, 2110.0],
                       [2205.5, 2201.1, 2197.2],
                       [2294.2, 2289.3, 2284.9]]).T
        f = interp2d(Tp, Pp, Up)
        return f(T, p)

    def _k(self, T, p=1e5, x=0):
        return 0.1279

    def _mu(self, T, p=1e5, x=0):
        return self._nu(T, p, x) * self.rho(T, p, x)

    def _nu(self, T, p=1e5, x=0):
        Tp = C2K(np.array([20, 40, 60, 80, 100]))
        Up = np.array([90, 32, 15, 8.5, 5.5]) * 1e-6
        return np.interp(T, Tp, Up)

    def _rho(self, T, p=1e5, x=0):
        Tp = C2K(np.array([20, 40, 60, 80, 100]))
        Pp = np.array([0.1, 10.1, 20.1]) * 1e6
        Up = np.array([[874.5, 879.7, 884.6],
                       [862.1, 867.8, 873.1],
                       [849.8, 855.8, 861.6],
                       [837.4, 843.9, 850.1],
                       [825.0, 832.0, 838.6]]).T
        f = interp2d(Tp, Pp, Up)
        return f(T, p)


class Water(Liquid):
    """
    Physical and chemical properties of water
    """

    def __init__(self, identifier: str='water',
                 latex: Optional[str]='$H_2O$',
                 comment: Optional[str]=None) -> None:
        """
        Args:
            identifier:
                identifier of matter

            latex:
                Latex-version of identifier. 
                If None, latex is identical with identifier

            comment:
                comment on matter
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)
        self.version = '301017_dww'

        # reference point and operational range
        self.T.operational = Range(C2K(0), C2K(100))
        self.T.ref = C2K(15)
        self.T.val = self.T.ref
        self.p.operational = Range(0. + atm(), 100e5 + atm())
        self.p.ref = atm()
        self.p.val = self.p.ref

        # constants
        self.hMelt = 334.0e3
        self.hVap = 2270.0e3
        self.T_liq = C2K(0.0)
        self.T_boil = C2K(99.9839)
        self.composition['H2O'] = 100.

        # functions of temperature, pressure and spare parameter 'x'
        self.rho.calc     = self._rho
        self.nu.calc      = self._nu
        self.mu.calc      = self._mu
        self.c_p.calc     = self._c_p
        self.k.calc = self._k
        self.c_sound.calc = self._c_sound
        self.E.calc       = self._E

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
        T = K2C(T)
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

    def _k(self, T, p=0., x=0.):
        return -0.5752 + (T * (6.397e-3 - T * 8.151e-6))

    def _c_sound(self, T, p=0., x=0.):
        return 20.05 * np.sqrt(T)

    def _E(self, T, p=0., x=0.):
        return 2.2e9
