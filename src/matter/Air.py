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


class Air(Gas):
    """
    Physical and chemical properties of air
    """

    def __init__(self, identifier='Air', latex=None, comment=None):
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
        self.E = 2.2e9
        self.hMelt = 334e3
        self.hVap = 2270e3
        self.T_liq = C2K(0)
        self.T_boil = 83
        self.composition['N2'] = 0.76   # weight percentage, dry air
        self.composition['O2'] = 0.23   # weight percentage, dry air

        # functions of temperature, presssure and spare parameter 'x'
        self.rho.calc = self._rho
        self.nu.calc = self._nu
        self.mu.calc = self._mu
        self.c_p.calc = self._c_p
        self.Lambda.calc = self._lambda
        self.c_sound.calc = self._c_sound
        self.beta.calc = self._beta

    def _c_p(self, T, p=1e5, x=0.):
        Tp = [100,   150,  200,  250,  300,  350,  400,
              450,   500,  550,  600,  650,  700,  750,
              800,   850,  900,  950, 1000, 1100, 1200,
              1300, 1400, 1500, 1600, 1700, 1800, 1900,
              2000, 2100, 2200, 2300, 2400, 2500, 3000]
        Up = [1.032e3, 1.012e3, 1.007e3, 1.006e3, 1.007e3, 1.009e3, 1.014e3,
              1.021e3, 1.030e3, 1.040e3, 1.051e3, 1.063e3, 1.075e3, 1.087e3,
              1.099e3, 1.110e3, 1.121e3, 1.131e3, 1.141e3, 1.159e3, 1.175e3,
              1.189e3, 1.207e3, 1.230e3, 1.248e3, 1.267e3, 1.286e3, 1.307e3,
              1.337e3, 1.372e3, 1.417e3, 1.478e3, 1.558e3, 1.665e3, 2.726e3]
        return np.interp(T, Tp, Up)

    def _mu(self, T, p=1e5, x=0.):
        return self._nu(T, p, x) * self._rho(T, p, x)

    def _nu(self, T, p=1e5, x=0.):
        Tp = [100,   150,  200,  250,  300,  350,  400,
              450,   500,  550,  600,  650,  700,  750,
              800,   850,  900,  950, 1000, 1100, 1200,
              1300, 1400, 1500, 1600, 1700, 1800, 1900,
              2000, 2100, 2200, 2300, 2400, 2500, 3000]
        Up = [2e-6, 4.426e-6, 7.59e-6, 11.44e-6, 15.89e-6, 20.92e-6, 26.41e-6,
              32.39e-6, 38.79e-6, 45.57e-6, 52.69e-6, 60.21e-6, 68.10e-6,
              76.37e-6, 84.93e-6, 93.8e-6,  102.9e-6, 112.2e-6, 121.9e-6,
              141.8e-6, 162.9e-6, 185.1e-6, 213.0e-6, 240.0e-6, 268.0e-6,
              298.0e-6, 329.0e-6, 362.0e-6, 396.0e-6, 431.0e-6, 468.0e-6,
              506.0e-6, 547.0e-6, 589.0e-6, 841.0e-6]
        return np.interp(T, Tp, Up)

    def _Pr(self, T, p=1e5, x=0.):
        Tp = [100,   150,  200,  250,  300,  350,  400,
              450,   500,  550,  600,  650,  700,  750,
              800,   850,  900,  950, 1000, 1100, 1200,
              1300, 1400, 1500, 1600, 1700, 1800, 1900,
              2000, 2100, 2200, 2300, 2400, 2500, 3000]
        Up = [0.786, 0.758, 0.737, 0.720, 0.707, 0.700, 0.690,
              0.686, 0.684, 0.683, 0.685, 0.690, 0.695, 0.702,
              0.709, 0.716, 0.720, 0.723, 0.726, 0.728, 0.728,
              0.719, 0.703, 0.685, 0.688, 0.685, 0.683, 0.677,
              0.672, 0.667, 0.655, 0.647, 0.630, 0.613, 0.536]
        return np.interp(T, Tp, Up)

    def _rho(self, T, p=1e5, x=0.):
        Tp = [100,   150,  200,  250,  300,  350,  400,
              450,   500,  550,  600,  650,  700,  750,
              800,   850,  900,  950, 1000, 1100, 1200,
              1300, 1400, 1500, 1600, 1700, 1800, 1900,
              2000, 2100, 2200, 2300, 2400, 2500, 3000]
        Up = [3.5562, 2.3364, 1.7458, 1.3947, 1.1614, 0.9950, 0.8711,
              0.7740, 0.6964, 0.6329, 0.5804, 0.5356, 0.4975, 0.4643,
              0.4354, 0.4097, 0.3868, 0.3666, 0.3482, 0.3166, 0.2902,
              0.2679, 0.2488, 0.2322, 0.2177, 0.2049, 0.1935, 0.1833,
              0.1741, 0.1658, 0.1582, 0.1513, 0.1448, 0.1389, 0.1135]
        return np.interp(T, Tp, Up)

    def _lambda(self, T, p=1e5, x=0.):
        Tp = [100,   150,  200,  250,  300,  350,  400,
              450,   500,  550,  600,  650,  700,  750,
              800,   850,  900,  950, 1000, 1100, 1200,
              1300, 1400, 1500, 1600, 1700, 1800, 1900,
              2000, 2100, 2200, 2300, 2400, 2500, 3000]
        Up = [9.34e-3, 13.8e-3, 18.1e-3, 22.3e-3, 26.3e-3, 30.0e-3, 33.8e-3,
              37.3e-3, 40.7e-3, 43.9e-3, 46.9e-3, 49.7e-3, 52.4e-3, 54.9e-3,
              57.3e-3, 59.6e-3, 62e-3,   64.3e-3, 66.7e-3, 71.5e-3, 76.3e-3,
              82e-3,   91e-3,   100e-3,  106e-3,  113e-3,  120e-3,  128e-3,
              137e-3,  147e-3,  160e-3,  175e-3,  196e-3,  222e-3,  486e-3]
        return np.interp(T, Tp, Up)

    def _c_sound(self, T, p=1e5, x=0.):
        return 331.3 * np.sqrt(1 + K2C(T) / 273.15)

    def _beta(self, T, p=1e5, x=0.):
        assert T > 1e-10, str(T)
        return 1. / T


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
        foo = Air('')
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
