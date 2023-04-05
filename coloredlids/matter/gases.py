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
      2022-08-23 DWW

  Acknowledgements:
      CoolProp is a contribution by Ian Bell (github.com/CoolProp/CoolProp)
"""

import numpy as np
import sys

from conversion import atm, C2K
from gasmix import GasMix
from importpack import import_package
from matter import Gas
# from mixformulas import mass_to_mole_fractions
from range import Range

try:
    import CoolProp
except ImportError:
    CoolProp = import_package('CoolProp')
assert 'CoolProp' in sys.modules


class _GenericCP(Gas):
    """
    Physical and chemical properties of gases based on CoolProp
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
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
        self.version = '23.04'

        # reference point and operational range
        self.T._ranges['operational'] = Range(C2K(0.01), C2K(300))
        self.T.ref = C2K(20)
        self.T.val = self.T.ref
        self.p._ranges['operational'] = Range(atm(), atm() + 100e5)
        self.p.ref = atm()
        self.p.val = self.p.ref

        # constants
        self.components[self] = 1.

        # functions of temperature, pressure and spare parameter 'x'
        self.c_sound.calc = self._c_sound
        self.c_p.calc = self._c_p
        self.k.calc = self._k
        self.M.calc = self._M
        self.mu.calc = self._mu
        self.rho.calc = self._rho

    def _c_p(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                dummy parameter [/]

        Returns:
            specific heat capacity [J/kg/k]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.PropsSI('C', 'T', T, 'P', p,
                                             self.identifier)
        except:
            return None

    def _rho(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                dummy parameter [/]

        Returns:
            density [kg/m3]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.PropsSI('Dmass', 'T', T, 'P', p,
                                             self.identifier)
        except:
            return None

    def _k(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                dummy parameter [/]

        Returns:
            thermal conductivity [W/m/K]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.PropsSI('conductivity', 'T', T, 'P', p,
                                             self.identifier)
        except:
            return None

    def _M(self, T: float = C2K(20), p: float = atm(),
           x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                dummy parameter [/]

        Returns:
            molar mass [kg/mol]

        Note:
            All arguments of this method are dummy parameters
        """
        try:
            return CoolProp.CoolProp.PropsSI('molemass', self.identifier)
        except:
            return None

    def _mu(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                dummy parameter [/]

        Returns:
            dynamic viscosity [Pa s]
            OR
            None if parameters out of range

        Note:
            kinematic viscosity: nu = mu / rho
        """
        try:
            return CoolProp.CoolProp.PropsSI('viscosity', 'T', T, 'P', p,
                                             self.identifier)
        except:
            return None

    def _c_sound(self, T: float, p: float = atm(),
                 x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                dummy parameter [/]

        Returns:
            speed of sound [m/s]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.PropsSI('A', 'T', T, 'P', p,
                                             self.identifier)
        except:
            return None


class StandardAir(GasMix):
    """
    Properties of standard air (zero air) composed from components

    Reference:
        https://en.wikipedia.org/wiki/Atmosphere_of_Earth#:~:text=By%20mole%20fraction%20(i.e.%2C%20by,0.4%25%20over%20the%20entire%20atmosphere.
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None,
                 k_mix_formula: str | None = None):
        super().__init__(identifier=identifier, latex=latex,
                         comment='standard air', k_mix_formula=k_mix_formula)
        self.add(O2, 20.95e-2)
        self.add(Ar, 0.93e-2)
        self.add(CO2, 0.04e-2)
        #
        # TODO Thermal conductivity model is not available for this
        #      fluid : PropsSI("conductivity","T",298.15,"P",10132.5,"Neon")
        # self.add(Neon, 0.002e-2)
        self.add(He, 0.0005e-2)
        self.fill_up(N2)


class HumidAir(_GenericCP):
    """
    Properties of humid air from CoolProp library

    Note:
        Argument 'x' in class methods represents relative humidity
        in [0, 1]-range

    Reference:
        coolprop.org/fluid_properties/HumidAir.html#molar-volume
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        super().__init__(identifier=identifier, latex=latex, comment=comment)

    def _M(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                dummy parameter [/]

        Returns:
            Molar mass [kg/mol]

        Note:
            All arguments of this method are dummpy parameters
        """
        try:
            psi_w = self.RH_to_y(T, p, x)  # [mol/mol_humid_air]
        except:
            psi_w = 0.

        if psi_w is None:
            psi_w = 0.
        M_air = 28.96e-3   # cp.CoolProp.PropsSI('molemass', 'air')
        M_h2o = 18.02e-3   # cp.CoolProp.PropsSI('molemass', 'H2O')

        return psi_w * M_h2o + (1. - psi_w) * M_air


    def T_and_T_dew_to_RH(self, T: float, T_dew: float) -> float:
        """
        Args:
            T:
                air temperature [K]

            T_dew:
                dew point temperature [K]

        Returns:
            relative humidity (RH) [/]

        Literature:
            bmcnoldy.rsmas.miami.edu/Humidity.html
        """
        T_C = T - 273.15
        T_dew_C = T_dew - 273.15
        RH = np.exp((17.625*T_dew_C) / (243.04+T_dew_C)) \
           / np.exp((17.625*T_C    ) / (243.04+T_C    ))

        return RH


    def T_and_RH_to_T_dew(self, T: float, RH: float) -> float:
        """
        Args:
            T:
                air temperature [K]
            RH:
                relative humidity [/]

        Returns:
            dew point temperature (T_dew) [K]

        Literature:
            bmcnoldy.rsmas.miami.edu/Humidity.html
        """
        T_C = T - 273.15
        ln_RH = np.log(RH)
        a = (17.625 * T_C) / (243.04 + T_C)
        T_dew_C = 243.04 * (ln_RH + a) / (17.625 - ln_RH - a)

        return T_dew_C + 273.15


    def humidity_ratio(self, T: float, p: float = atm(),
                       RH: float = 0.) -> float | None:
        """
        Calculates water mass per unit MASS of DRY air from relative humdity

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            RH:
                relative humidity [/]

        Returns:
            humidity ratio (W) [kg/kg_dry_air]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('HumRat', 'T', T, 'P', p,
                                               'RH', RH)
        except:
            return None


    def mole_fraction(self, T: float, p: float = atm(),
                      RH: float = 0.) -> float | None:
        """
        Calculates water mole fraction from relative humdity

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            RH:
                relative humidity [/]

        Returns:
            water mole fraction (y) [mol/mol_humid_air]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('psi_w', 'T', T, 'P', p,
                                               'RH', RH)
        except:
            return None

    def relative_humidity(self, T: float, p: float = atm(),
                          y: float = 0.) -> float | None:
        """
        Calculates relative humdity from water mole fraction

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            y:
                mole fraction [mol/mol_humid_air]

        Returns:
            relative humidity (RH) [/]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('RH', 'T', T, 'P', p,
                                               'psi_w', y)
        except:
            return None

    def W_to_AH(self, T: float, p: float = atm(),
                W: float = 0.) -> float | None:
        """
        Calculates water mass per unit VOLUME of DRY air

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            W:
                water mass per unit MASS of dry air [kg/kg_dry_air]

        Returns:
            absolute humidity (AH) [kg/m3 dry air]
            OR
            None if parameters out of range
        """
        rho = self.rho(T, p, 0.)
        if rho is None:
            return None

        return W * rho

    def y_to_AH(self, T: float, p: float = atm(),
                y: float = 0.) -> float | None:
        """
        Calculates water mass per unit VOLUME of DRY air

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            y:
                water mass per unit MASS of DRY air [kg/kg_dry_air]

        Returns:
            absolute humidity (AH) [kg water/m3_dry_air]
            OR
            None if parameters out of range
        """
        W = self.y_to_W(T, p, y=y)
        if W is None:
            return None

        return self.W_to_AH(T, p, W=W)


    def RH_to_AH(self, T: float, p: float = atm(),
                 RH: float = 0.) -> float | None:
        """
        Calculates water mass per unit VOLUME of DRY air

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            RH:
                relative humidity [/]

        Returns:
            absolute humidity (AH) [kg/m3_dry_air]
            OR
            None if parameters out of range
        """
        W = self.RH_to_W(T, p, RH=RH)
        if W is None:
            return None

        return self.W_to_AH(T, p, W=W)


    def RH_to_y(self, T: float, p: float = atm(),
                RH: float = 0.) -> float | None:
        """
        Calculates water mole fraction from relative humdity

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            RH:
                relative humidity [/]

        Returns:
            Water mole fraction (y) [mol/mol_humid_air]
            OR
            None if parameters out of range
        """
        return self.mole_fraction(T, p, RH=RH)

    def RH_to_W(self, T: float, p: float = atm(),
                RH: float = 0.) -> float | None:
        """
        Calculates water mass per unit MASS of DRY air (humidity ratio)
        from relative humdity

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            RH:
                relative humidity [/]

        Returns:
            humidity ratio (W) [kg/kg_dry_air]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('W', 'T', T, 'P', p, 'RH', RH)
        except:
            return None

    def y_to_RH(self, T: float, p: float = atm(),
                y: float = 0.) -> float | None:
        """
        Calculates relative humdity from water mole fraction

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            y:
                Water mole fraction [mol/mol_humid_air]

        Returns:
            Relative humidity (RH) [/]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('RH', 'T', T, 'P', p,
                                               'psi_w', y)
        except:
            return None

    def y_to_W(self, T: float, p: float = atm(),
               y: float = 0.) -> float | None:
        """
        Calculates water mass per unit MASS of DRY air (humidity ratio)
        from water mole fraction

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            y:
                water mole fraction [mol/mol_humid_air]

        Returns:
            Humidity ratio (W) [kg/kg_dry_air]
            OR
            None if parameters out of range
        """
        return self.humidity_ratio(T, p, RH=y)

    def W_to_RH(self, T: float, p: float = atm(),
                W: float = 0.) -> float | None:
        """
        Calculates relative humdity from water mass per unit MASS of
        DRY air (humidity ratio)

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            W:
                water mass per unit MASS of DRY air (humidity ratio)
                [kg/kg_dry_air]

        Returns:
            relative humidity (RH) [/]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('RH', 'T', T, 'P', p,
                                               'HumRat', W)
        except:
            return None

    def W_to_y(self, T: float, p: float = atm(),
               W: float = 0.) -> float | None:
        """
        Calculates water mole fraction from water mass per unit MASS of
        DRY air (humidity ratio)

        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            W:
                water mass per unit MASS of DRY air (humidity ratio)
                [kg/kg_dry_air]

        Returns:
            Water mole fraction (y) [mol/mol_humid_air]
            OR
            None if parameters out of range
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('psi_w', 'T', T, 'P', p,
                                               'HumRat', W)
        except:
            return None

    def RH1_to_RH2(self, RH1: float, T1: float, T2: float,
                   p1: float = atm(), p2: float | None = None
                   ) -> float | None:
        """
        Converts relative humidity from RH(T1, p2) to RH(T2, p2)
        at constant humidity ratio W

        Args:
            RH1:
                relative humidity at (T1, p1) [/]
            T1:
                first temperature [K]
            T2:
                second temperature [K]
            p1:
                first pressure [Pa]
            p2:
                second pressure [Pa]
                if p2 is None, then p2=p1

        Returns:
            relative humidity at (T2, p2) [/]
            OR
            None if parameters out of range
        """
        if not 0. < RH1 < 1.:
            return None
        if p2 is None:
            p2 = p1

        try:
            W = self.RH_to_W(T1, p1, RH1)
            return self.W_to_RH(T2, p2, W)
        except:
            return None

    def _c_p(self, T: float, p: float = atm(),
             x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                relative humidity [/]

        Returns:
            Specific heat capacity [J/kg/K]
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('cp_ha', 'T', T, 'P', p,
                                               'RH', x)
        except:
            return None

    def _rho(self, T: float, p: float = atm(),
             x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                relative humidity [/]

        Returns:
            density [kg/m3]

        Note:
            CoolProp's Vha-function returns mixture volume per unit humid
            air in [m3/kg] -> density is inverse value
        """
        try:
            return 1. / CoolProp.CoolProp.HAPropsSI('Vha', 'T', T, 'P', p,
                                                    'RH', x)
        except:
            return None

    def _k(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                relative humidity [/]

        Returns:
            thermal conductivity [W/m/K]
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('k', 'T', T, 'P', p, 'RH', x)
        except:
            return None

    def _mu(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        """
        Args:
            T:
                temperature [K]
            p:
                pressure [Pa]
            x:
                relative humidity [/]

        Returns:
            dynamic viscosity [Pa s]
        """
        try:
            return CoolProp.CoolProp.HAPropsSI('mu', 'T', T, 'P', p, 'RH', x)
        except:
            return None


class Air(_GenericCP):
    """
    Note:
        Dry air, 100 kPa T=25C, rh=0
        Engineering tool box: 26.24 mW/m/K
        CoolProp:             26.25 mW/m/K

    Literature:
        https://www.engineeringtoolbox.com/air-properties-viscosity-conductivity-heat-capacity-d_1509.html
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)


class Ar(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.D_in_air.calc = lambda T, p=atm(), x=0: 1.89e-5*(T/C2K(20))**1.75


class CH4(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.D_in_air.calc = lambda T, p=atm(), x=0: 2.1e-5 * (T/C2K(20))**1.75


class CO(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.D_in_air.calc = lambda T, p=atm(), x=0: 2.08e-5*(T/C2K(20))**1.75
        assert 0, f'??? {self.identifier}: k() does not work'


class CO2(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.D_in_air.calc = lambda T, p=atm(), x=0: 1.6e-5 * (T/C2K(20))**1.75


class H2(_GenericCP):
    def __init__(self, identifier: str = 'H2', latex: str | None = None,
                 comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.D_in_air.calc = lambda T, p=atm(), x=0: 7.56e-5*(T/C2K(20))**1.75


class H2O(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)
        # Equ. by Bolz and Tuve:
        self.D_in_air.calc = lambda T, p=atm(), x=0.: (
                                    -2.775e-6 + T * (4.479e-8 + T*1.656e-10))


class He(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.D_in_air.calc = lambda T, p=atm(), x=0: 6.97e-5*(T/C2K(20))**1.75


class N2(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)


class Neon(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        print(f'??? {self.identifier}: k() does not work')


class NH3(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.D_in_air.calc = lambda T, p=atm(), x=0: 2.57e-5*(T/C2K(20))**1.75


class O2(_GenericCP):
    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None, comment: str | None = None):
        super().__init__(identifier=identifier, latex=latex, comment=comment)


class _Generic(_GenericCP):
    """
    Physical and chemical properties of gases based on parent class
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
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
