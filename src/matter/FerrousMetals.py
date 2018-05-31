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
      2018-05-31 DWW
"""

import numpy as np

from Parameter import C2K, K2C
import GenericMatter as gm

"""
References: 
    U. Heubner: Merkblatt 821, Edelstahl Rostfrei – Eigenschaften, 
    [Informationsstelle Edelstahl Rostfrei](www.edelstahl-rostfrei.de), 
    Düsseldorf, 5. Auflage, 2014  
"""

class St1_4016(gm.Ferrous):
    def __init__(self, identifier='1.4016', latex=None, comment='X6Cr17'):
        super().__init__(identifier, latex=latex, comment=None)
        self.T.ref = C2K(20)
        self.T_sol = None
        self.E.calc = lambda T=0, p=0, x=0: 220e+9
        self.beta.calc = lambda T=0, p=0, x=0: 10.5e-6
        self.c_p.calc = lambda T=0, p=0, x=0: 460
        self.Lambda.calc = lambda T=0, p=0, x=0: 25
        self.rho.calc = lambda T=0, p=0, x=0: 7700


class St1_4003(gm.Ferrous):
    def __init__(self, identifier='1.4003', latex=None, comment='X2CrNi12'):
        super().__init__(identifier, latex=latex, comment=None)
        self.T.ref = C2K(20)
        self.T_sol = None
        self.E.calc = lambda T=0, p=0, x=0: 220e+9
        self.beta.calc = lambda T=0, p=0, x=0: 11.6e-6
        self.c_p.calc = lambda T=0, p=0, x=0: 430
        self.Lambda.calc = lambda T=0, p=0, x=0: 25
        self.rho.calc = lambda T=0, p=0, x=0: 7700


class St1_4301(gm.Ferrous):
    def __init__(self, identifier='1.4301', latex=None, 
                 comment='X5CrNi18-10, AISI 304'):
        super().__init__(identifier, latex=latex, comment=None)
        self.T.ref = C2K(20)
        self.T_sol = C2K(1400)
        self.E.calc = lambda T=0, p=0, x=0: 200e+9
        self.beta.calc = lambda T=0, p=0, x=0: 17.5e-6
        self.c_p.calc = lambda T=0, p=0, x=0: 500
        self.Lambda.calc = lambda T=0, p=0, x=0: 15
        self.rho.calc = lambda T=0, p=0, x=0: 7900


class St1_4541(gm.Ferrous):
    def __init__(self, identifier='1.4541', latex=None,
                 comment='X6CrNiTi18-10'):
        super().__init__(identifier, latex=latex, comment=None)
        self.T.ref = C2K(20)
        self.T_sol = None
        self.E.calc = lambda T=0, p=0, x=0: 200e+9
        self.beta.calc = lambda T=0, p=0, x=0: 17.5e-6
        self.c_p.calc = lambda T=0, p=0, x=0: 500
        self.Lambda.calc = lambda T=0, p=0, x=0: 15
        self.rho.calc = lambda T=0, p=0, x=0: 7900


class St1_4401(gm.Ferrous):
    def __init__(self, identifier='1.4401', latex=None,
                 comment='X5CrNiMo17-12-2'):
        super().__init__(identifier, latex=latex, comment=None)
        self.T.ref = C2K(20)
        self.T_sol = None
        self.E.calc = lambda T=0, p=0, x=0: 200e+9
        self.beta.calc = lambda T=0, p=0, x=0: 17.5e-6
        self.c_p.calc = lambda T=0, p=0, x=0: 500
        self.Lambda.calc = lambda T=0, p=0, x=0: 15
        self.rho.calc = lambda T=0, p=0, x=0: 8000


class St1_4571(gm.Ferrous):
    def __init__(self, identifier='1.4571', latex=None,
                 comment='X6CrNiMoTi17-12-2'):
        super().__init__(identifier, latex=latex, comment=None)
        self.T.ref = C2K(20)
        self.T_sol = None
        self.E.calc = lambda T=0, p=0, x=0: 200e+9
        self.beta.calc = lambda T=0, p=0, x=0: 18.5e-6
        self.c_p.calc = lambda T=0, p=0, x=0: 500
        self.Lambda.calc = lambda T=0, p=0, x=0: 15
        self.rho.calc = lambda T=0, p=0, x=0: 8000


class St1_4362(gm.Ferrous):
    def __init__(self, identifier='1.4362', latex=None, comment='X2CrNiN23-4'):
        super().__init__(identifier, latex=latex, comment=None)
        self.T.ref = C2K(20)
        self.T_sol = None
        self.E.calc = lambda T=0, p=0, x=0: 200e+9
        self.beta.calc = lambda T=0, p=0, x=0: 17.5e-6
        self.c_p.calc = lambda T=0, p=0, x=0: 500
        self.Lambda.calc = lambda T=0, p=0, x=0: 15
        self.rho.calc = lambda T=0, p=0, x=0: 7800


class St1_4462(gm.Ferrous):
    def __init__(self, identifier='1.4462', latex=None,
                 comment='X2CrNiMoN22-5-3'):
        super().__init__(identifier, latex=latex, comment=None)
        self.T.ref = C2K(20)
        self.T_sol = None
        self.E.calc = lambda T=0, p=0, x=0: 200e+9
        self.beta.calc = lambda T=0, p=0, x=0: 14.5e-6
        self.c_p.calc = lambda T=0, p=0, x=0: 500
        self.Lambda.calc = lambda T=0, p=0, x=0: 15
        self.rho.calc = lambda T=0, p=0, x=0: 7800
        
        
class Iron(gm.Ferrous, gm.Liquid):
    """
        Properties of iron
    """

    def __init__(self, identifier='Fe', latex=None, comment=None):
        """
        Args:
            identifier (string, optional):
                identifier of matter

            latex (string, optional):
                Latex-version of identifier. If None, identifier is assigned

            comment (string, optional):
                comment on matter

        Reference:
            - Heat capacity c_p^* = 41.8 [J/(mol K)] for pure iron in
              T-range 1809..1873 K, data from:
              Kubaschewski,O., Alcock,C.B.: Metallurgical thermochemistry
              (5th Edn.), Pergamon Press, Oxford, 1979, p.336, in: [IIDA93]
            - Atomic weight of pure iron: M = 55.85 kg/kmol
            - Mass-specific heat capacity of Fe:
              c_p =c_p^* / M = 41.8 * (1000 / 55.85) = 748.4 [J/(kg K)]
        """
        # calls firstly: Solid.__init__() and secondly: Liquid.__init__()
        super().__init__(identifier, latex=latex, comment=comment)

        self.version = '110118_dww'
        self.T.ref = C2K(20)

        self.nu_mech      = None
        self.friction     = None
        self.E.calc       = lambda T=0, p=0, x=0: 211e9

        self.T_sol        = C2K(1430)
        self.T_liq        = self.T_sol + 50
        self.T_vap        = C2K(2700)
        self.T_deform     = self.T_sol + 0.66 * (self.T_liq - self.T_sol)
        self.M            = 55.845e-3
        self.h_melt       = 270e+3
        self.h_vap        = 6.35e+6
        self.beta.calc    = lambda T=0, p=0, x=0: 23.1e-6
        self.workFunction = 4.3                 # JAP Vol6 1973 p.2250 [QUIG73]

        self.c_p.calc     = self._c_p
        self.Lambda.calc  = self._Lambda
        self.mu.calc      = self._mu
        self.nu.calc      = lambda T=0, p=0, x=0: self.mu(T, p, x) / \
                                                  self.rho(T, p, x)
        self.rho.calc     = self._rho
        self.rho_el.calc  = self._rho_el

    def _c_p(self, T=0, p=0, x=0):
        Tp = [300, 600, 900, 1033, 1040, 1184, 1184.1, 1400, 1673, 1673.1,
              1809, 1809.1, 2000, 3000]
        Up = [430, 580, 760, 1260, 1160, 720, 610, 640, 680, 730, 760, 790,
              790, 790]
        return np.interp(T, Tp, Up)

    def _Lambda(self, T=0, p=0, x=0):
        Tp = [300, 600, 900, 1184, 1400, 1673, 1673.1, 1809, 1809.1,
              2000, 3000]
        Up = [59.6, 54.6, 37.4, 28.2, 30.6, 33.7, 33.4, 34.6, 40.3, 42.6,
              48]
        return np.interp(T, Tp, Up)

    def _mu(self, T=0, p=0.1e6, x=0):
        """
        [JONE96]: eta = eta0 * exp(E / (R*T)), eta0 = 0.3699e-3 kg/(m s),
                  E = 41.4e3 J/mol, and R = 8.3144 J/(K mol)
        """
        return 0.3699e-3 * np.exp(41.4e3 / (8.3144*T)) \
            if T > self.T_deform else 1e20

    def _rho(self, T=0, p=0.1e6, x=0):
        """
        Reference for liquid iron:
        Steinberg, D. J.: Met. Trans. 5 (1974), 1341, in [Iida93]
        """
        T_Celsius = min(K2C(T), 1600)
        if T_Celsius > 1536:
            rho = 7030 + (-8.8e-1) * (T_Celsius - 1536)
        elif T_Celsius > 723:
            rho = (-1e-4 * T_Celsius - 0.2) * T_Celsius + 7852.3
        else:
            rho = (-1e-4 * T_Celsius - 0.3) * T_Celsius + 7849.1
        return rho

    def _rho_el(self, T=0, p=0.1e6, x=0):
        """
        Reference:
            Rykalin, in Radaj: Heat Effects of Welding, Springer 1992, p.68
            T[deg C]  rho [Ohm*mm]
            0         1.26e-4
            400       4e-4
            800       10.2e-4
            1200      12e-4
            1600      12.6e-4
        """
        T_Celsius = max(K2C(T), 20)

        # specific resistance in [Ohm m]
        if T_Celsius < 800:
            rho_el = ((1.081e-8 * T_Celsius + 2.53e-6) * T_Celsius +
                      1.26e-3) * 1e-4
        elif T < self.T_sol:
            rho_el = ((-3.75e-9 * T_Celsius + 1.2e-5) * T_Celsius +
                      3e-3) * 1e-4
        else:
            rho_el = 2 * 1.2e-6
        return rho_el


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 0

    import FerrousMetals as module
    classes = [v for c, v in module.__dict__.items()
               if isinstance(v, type) and v.__module__ == module.__name__]

    if 1:
        print('list of defined matter:', [c().identifier for c in classes])

    if 0 or ALL:
        for mat in classes:
            print('class:', mat.__name__)
            foo = mat()
            print(foo.identifier, '*' * 50)
            foo.plot()

    if 1 or ALL:
        print('-' * 55 + '\nTable of all steels defined (id, lambda, rho, '
              'c_p, E)\n' + '-' * 55)
        for mat in classes:
            foo = mat()
            T = foo.T.ref
            print('Steel: {:>8s}  {:3.1f}  {:5.1f}  {:5.1f}  {:5.3e}'.format(
                  foo.identifier, foo.Lambda(T),  foo.rho(T), foo.c_p(T), 
                  foo.E(T)))
