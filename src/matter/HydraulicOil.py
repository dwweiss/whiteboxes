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
      2018-01-16 DWW
"""

import numpy as np
from scipy.interpolate import interp2d

from GenericMatter import Liquid
from Parameter import C2K


class HydraulicOil(Liquid):
    """
    Thermophysical properties of hydraulic oil
    """

    def __init__(self, identifier='HydraulicOil', latex=None, comment=None):
        super().__init__(identifier=identifier)
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
        self.version = '160118_dww'

        # reference point and operational range
        self.T.operational = C2K([0, 100]).tolist()
        self.T.ref = C2K(15)
        self.T.val = self.T.ref
        self.p.operational = (np.array([0, 100e5]) + 1.01325e5).tolist()
        self.p.ref = 1.01325e5
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
        self.Lambda.calc = self._lambda
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

    def _lambda(self, T, p=1e5, x=0):
        return 0.1279

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

    def _nu(self, T, p=1e5, x=0):
        Tp = C2K(np.array([20, 40, 60, 80, 100]))
        Up = np.array([90, 32, 15, 8.5, 5.5]) * 1e-6
        return np.interp(T, Tp, Up)

    def _mu(self, T, p=1e5, x=0):
        return self._nu(T, p, x) * self.rho(T, p, x)


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 0

    import matplotlib.pyplot as plt

    def curve1(x, y, xl='x', yl='y'):
        plt.figure(figsize=(6, 4))
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.plot(x, y)
        plt.rcParams.update({'font.size': 14})
        plt.grid()
        plt.show()

    if 1 or ALL:
        foo = HydraulicOil('')
        foo.plot(property='c_p')
        foo.rho.plot()
        print('foo:', foo.rho)
        foo.rho.plot()
        foo.plot(property='nu')

    if 0 or ALL:
        foo = HydraulicOil('')
        T_celsius = np.linspace(0., 100., num=50)
        T_kelvin = C2K(T_celsius)
        rho = foo.rho(T=T_kelvin)
        nu = foo.nu(T_kelvin)
        c_p = [foo.c_p(T) for T in T_kelvin]
        Lambda = [foo.Lambda(T) for T in T_kelvin]
        curve1(T_celsius, rho, xl=r'$T$ [$\degree$C]', yl=foo.rho.latex)
        curve1(T_celsius, 1e6 * nu, xl=r'$T$ [$\degree$C]',
               yl=foo.nu.latex+r'$\,\cdot 10^6$')
        curve1(T_celsius, Lambda, xl=r'$T$ [$\degree$C]',
               yl=foo.Lambda.latex)

        print(foo.rho.calc(C2K(10), 1e6))
