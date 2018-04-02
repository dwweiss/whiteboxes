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

from GenericMatter import Liquid
from Parameter import K2C, C2K


class Diesel(Liquid):
    """
    Thermophysical properties of diesel fuel

    Reference:
        [NIT11] I Nita and S Geacai: Study of density and viscosity variation
            with temperature for fules use4d for Diesel engine. Ovidius Univ.
            Annals of Chemistry, Vol. 22, No. 1, pp.357-61, 2011
    """

    def __init__(self, identifier='Diesel', latex=None, comment=None):
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
        self.version = '191217_dww'

        # reference point and operational range
        self.T.operational = [x for x in C2K([0, 100])]
        self.T.ref = C2K(15)
        self.T.val = self.T.ref
        self.p.operational = [x + 1.01325e5 for x in [0, 100e5]]
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

    def _lambda(self, T, p=1e5, x=0):
        return 0.15


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    import matplotlib.pyplot as plt
    import numpy as np

    def curve1(x, y, xl='x', yl='y'):
        plt.figure(figsize=(6, 4))
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.plot(x, y)
        plt.rcParams.update({'font.size': 14})
        plt.grid()
        plt.show()

    if 0 or ALL:
        foo = Diesel('')
        foo.plot(property='c_p')
        foo.rho.plot()
        foo.c_sound.plot()
        print('foo:', foo.Lambda)
        foo.Lambda.plot()
        foo.plot(property='Lambda')

    if 0 or ALL:
        foo = Diesel('')
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
