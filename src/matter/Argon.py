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
from Parameter import C2K, K2C
from GenericMatter import Gas


class Argon(Gas):
    """
    Physical and chemical properties of Argon
    """

    def __init__(self, identifier='Ar', latex=None, comment=None):
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
        self.T.operational = C2K(np.array([0, 100])).tolist()
        self.T.ref = C2K(15)
        self.T.val = self.T.ref
        self.p.operational = (np.array([0, 100e5]) + 1.01325e5).tolist()
        self.p.ref = 1.01325e5
        self.p.val = self.p.ref

        # constants
#        self.E = 
#        self.hMelt = 
#        self.hVap = 
#        self.T_liq = 
#        self.T_boil = 
        self.composition['Ar'] = 100.
        self.M = 39.948e-3
        self.Z = 0.9994

        # functions of temperature, presssure and spare parameter 'x'
        self.rho.calc = self._rho
        self.nu.calc = self._nu
        self.mu.calc = self._mu
        self.c_p.calc = self._c_p
        self.Lambda.calc = self._lambda
#        self.c_sound.calc = self._c_sound
#        self.beta.calc = self._beta

    def _rho(self, T, p=1e5, x=0.):
        Tp = C2K([20, 20])
        Up = [1.6339, 1.6339]
        return np.interp(T, Tp, Up)

    def _c_p(self, T, p=1e5, x=0.):
        Tp = C2K([0, 100, 200, 300, 400, 500, 600, 700, 800])
        Up = [0.522, 0.521, 0.521, 0.521, 0.521, 0.520, 0.520, 0.520, 0.520]
        return np.interp(T, Tp, Up)

    def _nu(self, T, p=1e5, x=0.):
        return self._mu(T, p, x) / self._rho(T, p, x)

    def _mu(self, T, p=1e5, x=0.):
        Tp = np.array([0, 100, 200, 300, 400, 500, 600])
        Up = np.array([21.2, 27.1, 32.1, 36.7, 41.0, 45.22, 48.7]) * 1e-6
        return np.interp(T, Tp, Up)

    def _lambda(self, T, p=1e5, x=0.):
        Tp = C2K([0, 100, 200, 300, 400, 500, 600])
        Up = np.array([16.51, 21.17, 25.59, 29.89, 33.96, 37.91, 39.43]) * 1e-3
        return np.interp(T, Tp, Up)


# Examples ####################################################################

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    def curve1(x, y, xl='x', yl='y'):
        plt.figure(figsize=(6, 4))
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.plot(x, y)
        plt.rcParams.update({'font.size': 14})
        plt.grid()
        plt.show()

    if 1:
        foo = Argon('')
        foo.plot(property='c_p')
        foo.Lambda.plot()
        foo.c_sound.plot()
        print('*' * 79)
        foo.plot()

    if 1:
        T_Kelvin = C2K(np.linspace(0., 100., num=50))
        rho = foo.rho(T_Kelvin, 0.)
        nu = foo.nu(T_Kelvin, 0.)
        Lambda = foo.Lambda(T_Kelvin, 0.)

        curve1(K2C(T_Kelvin), rho,
               xl=r'$T$ [$^o$C]', yl=foo.rho.latex)
        curve1(K2C(T_Kelvin), 1e6 * nu,
               xl=r'$T$ [$^o$C]', yl=foo.nu.latex+r'$\cdot 10^6$')
        curve1(K2C(T_Kelvin), 1e6 * Lambda,
               xl=r'$T$ [$^o$C]', yl=foo.Lambda.latex+r'$\cdot 10^6$')

        print('rho(T=10C, p=1MPa):', foo.rho(C2K(10), 1e6))
