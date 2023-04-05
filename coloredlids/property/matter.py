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
      2023-03-29 DWW
"""

from collections import OrderedDict
import numpy as np
from typing import Callable, Dict, Optional

from conversion import atm, C2K
from property import Property


class Matter(Property):
    """
    Collection of physical and chemical properties of generic matter

    Literature:
        https://dashamlav.com/difference-matter-vs-material/


    Note:
        components_to_str() returns the chemical composition
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier.
                If None, latex is identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.components: Dict[Matter, float] | None = None

        self.a = Property('a', 'm$^2$/s', comment='thermal diffusity',
                          calc=self._a)
        self.beta = Property('beta', '1/K', latex=r'$\beta_{th}$',
                             comment='volumetric thermal expansion')
        self.c_p = Property('c_p', 'J/kg/K', comment='specific heat capacity')
        self.c_sound = Property('c_sound', 'm/s', latex='$c_{sound}$')
        self.c_sound.calc = lambda T, p, x: None
        self.components: Dict[str, float] = OrderedDict()
        self.compressible: bool = False
        self.E = Property('E', 'Pa', comment="Young's (elastic) modulus")
        self.h_melt: float = 0.
        self.h_vap: float = 0.
        self.k = Property('k', 'W/m/K', comment='thermal conductivity')
        self.M = Property('M', 'kg/mol', comment='molar mass')
        self.M.calc = lambda T=0., p=0., x=0.: None
        self.nu_mech: float = None
        self.rho = Property('rho', 'kg/m$^3$', latex=r'$\varrho$', ref=1.,
                            comment='density')
        self.rho.T.ref = C2K(20.)
        self.rho.p.ref = atm()
        self.rho_el = Property('rho_el', 'Ohm', latex=r'$\varrho_{el}$',
                               comment='electric resistance')
        self.safety_class: str | None = None
        self.T_boil: float = 0.
        self.T_flash: float = 0.
        self.T_liq: float = 0.
        self.T_melt: float = 0.
        self.T_sol: float = 0.

        if self.E() is None or np.abs(self.E()) < 1e-20:
            self.rho.calc = lambda T, p, x: self.rho.ref \
                / (1. + (T - self.rho.T.ref) * self.beta())
        else:
            self.rho.calc = lambda T, p, x: self.rho.ref \
                / (1. + (T - self.rho.T.ref) * self.beta()) \
                / (1. - (p - self.rho.p.ref) / self.E())



    def dk_dT(self, T: float, p: float, x: float, 
              dT: float = 0.1) -> float | None:
        try:
            return (self.k(T+dT, p, x) - self.k(T, p, x)) / dT
        except:
            return None

    def dk_dp(self, T: float, p: float, x: float, 
              dp: float = 1.) -> float | None:
        try:
            return (self.k(T, p+dp, x) - self.k(T, p, x)) / dp
        except:
            return None

    def dk_dx(self, T: float, p: float, x: float, 
              dx: float = 0.001) -> float | None:
        try:
            return (self.k(T, p, x+dx) - self.k(T, p, x)) / dx
        except:
            return None


    def drho_dT(self, T: float, p: float, x: float, 
                dT: float = 0.1) -> float | None:
        try:
            return (self.rho(T+dT, p, x) - self.rho(T, p, x)) / dT
        except:
            return None

    def drho_dp(self, T: float, p: float, x: float, 
                dp: float = 1.) -> float | None:
        try:
            return (self.rho(T, p+dp, x) - self.rho(T, p, x)) / dp
        except:
            return None


    def drho_dx(self, T: float, p: float, x: float, 
                dx: float = 1e-4) -> float | None:
        try:
            return (self.rho(T, p, x+dx) - self.rho(T, p, x)) / dx
        except:
            return None


    def dcp_dT(self, T: float, p: float, x: float, 
               dT: float = 0.1) -> float | None:
        try:
            return (self.c_p(T+dT, p, x) - self.c_p(T, p, x)) / dT
        except:
            return None

    def dcp_dp(self, T: float, p: float, x: float, 
               dp: float = 1.) -> float | None:
        try:
            return (self.c_p(T, p+dp, x) - self.c_p(T, p, x)) / dp
        except:
            return None


    def dcp_dx(self, T: float, p: float, x: float, 
               dx: float = 0.001) -> float | None:
        try:
            return (self.c_p(T, p, x+dx) - self.c_p(T, p, x)) / dx
        except:
            return None


    def _a(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        try:
            k = self.k(T, p, x)
            c_p = self.c_p(T, p, x)
            rho = self.rho(T, p, x)
            if k is None or c_p is None or rho is None:
                return None
            cp_rho = c_p * rho
            if cp_rho < 1e-10:
                return None
            return k / cp_rho
        except:
            return None

    def set_all_ref(self, T: float, p: float = atm(), x: float = 0.) -> bool:
        any_property_set = False
        for attr in dir(self):
            if not attr.startswith('_'):
                val = getattr(self, attr)
                if isinstance(val, Property):
                    print(f'{attr=}, {val=}')
                    any_property_set = True
                    val.T.ref = T
                    val.p.ref = p
                    val.x.ref = x
        return not any_property_set

    def plot(self, prop: Property | str | None = None) -> None:
        if prop is None or prop.lower() == 'all':
            for key, val in self.__dict__.items():
                if isinstance(val, Property):
                    print(f'{val.T.ref=}, {val.p.ref=}, {val.x.ref=}')

                    print(f"+++ Plot matter: '{self.identifier}', "
                          f"property: '{key}'")
                    val.plot()
        else:
            if prop in self.__dict__:
                if prop is not None:
                    self.__dict__[prop].plot(title=self.identifier)
                else:
                    self.write(f'!!! No plot of property: {prop}')

    def add(self, component: Optional['Matter'],
            mole_fraction: float | None = None) -> bool:
        """
        Adds a component. Alternatively, mixture can be filled up
        so that sum of mole fractions equals one

        Args:
            component:
                object or instance of child class of Fluid

            mole_frac:
                mole fraction of component [mol/mol], equals volume fraction
                [m3/m3] or partial pressure ratio [Pa/Pa] if ideal gas
                OR
                None -> filling up array of components with
                'mole_fraction' so that sum of mole fractions equals 1.0

        Returns:
            False if component is None
        """
        if component is None:
            return False

        if not isinstance(component, Matter):
            component = component()

        if mole_fraction is None:
            mole_fraction = 1. - np.sum(list(self.components.values()))
            # print(f'mat173 fill_up: {mole_fraction=}')
        self.components[component] = mole_fraction

        M = 0.
        for component, mole_frac in self.components.items():
            # print(f'{component.identifier=} {component.M()=}')

            M += mole_frac * component.M()
        self.M.calc: Callable = lambda T, p, x: M

        return True

    def fill_up(self, component: Optional['Matter']) -> bool:
        """
        This is a convenience function ensuring sum of 100%vol.
        Adds last component and fills up to sum of mole fractions equalling 1.0

        Args:
            component:
                object or instance of child class of Fluid

        Returns:
            False if component is False
        """
        return self.add(component)

    def components_to_str(self) -> str:
        """
        Returns:
            components as string
        """

        if self.components is None:
            return ''
        s = '{'
        for component, mole_fraction in self.components.items():
            s += f'{component.identifier}:{mole_fraction:.2%} '
        s = s[:-1] + '} %v'
        return s


class Solid(Matter):
    """
    Collection of physical and chemical properties of generic solid
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier.
                If None, latex identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.R_p02 = Property('Rp0.2', 'Pa', latex='$R_{p,0.2}$',
                              comment='yield strength')
        self.R_m = Property('R_m', 'Pa', latex='$R_{m}$',
                            comment='tensile strength')
        self.R_compr = Property('R_compr', 'Pa', latex='$R_{compr}$',
                                comment='compressive strength')
        self.T_recryst = 0.


class NonMetal(Solid):
    """
    Collection of physical and chemical properties of generic non-metal
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier. If None, identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)


class Metal(Solid):
    """
    Collection of physical and chemical properties of generic metal
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier. If None, identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)


class NonFerrous(Metal):
    """
    Collection of physical and chemical properties of generic nonferrous metal
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier. If None, identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)


class Ferrous(Metal):
    """
    Collection of physical and chemical properties of generic ferrous metal
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier. If None, identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)


class Fluid(Matter):
    """
    Collection of physical and chemical properties of generic fluid
    """

    def __init__(self, identifier: str = __qualname__,
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier. If None, identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.mu = Property('mu', 'Pa s', latex=r'$\mu$',
                           comment='dynamic viscosity', calc=self._mu)
        self.nu = Property('nu', 'm^2/s', latex=r'$\nu$',
                           comment='kinematic viscosity', calc=self._nu)

    def _mu(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        try:
            return self.nu(T, p, x) * self.rho(T, p, x)
        except:
            return None

    def _nu(self, T: float, p: float = atm(), x: float = 0.) -> float | None:
        try:
            rho = self.rho(T, p, x)
            if rho is None or rho < 1e-10:
                return None
            return self.mu(T, p, x) / rho
        except:
            return None


class Liquid(Fluid):
    """
    Collection of physical and chemical properties of generic liquid
    """

    def __init__(self, identifier: str = 'liquid',
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier. If None, identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.T.ref = C2K(20.)


class Gas(Fluid):
    """
    Collection of physical and chemical properties of gases

    References:
        - Natural gas http://petrowiki.org/PEH%3AGas_Properties#Real_Gases
        - http://www.pipeflowcalculations.com/tables/gas.php
        - Gases (mu,rho)  http://www.alicat.com/documents/conversion/
              Gas_VDC_25C.pdf
        - Noble gases  http://www.chem.umass.edu/~rbmetz/CHEM477/KestinA.pdf
        - Ar  http://www.nist.gov/data/PDFfiles/jpcrd305.pdf
        - gas pipeline hydraulics: http://books.google.de/
              books?id=nP46tA8MOr8C&pg=PA17&lpg=PA17&dq=
              pseudo+reduced+temperature&source=bl&ots=GVlc0l88v_&sig=
              Lit0LL31h79-1hB6RdE4qFgbfaE&hl=de&sa=X&ei=
              O0jSU6SlFMvY7AaA3oDoCA&ved=0CDcQ6AEwBA#v=onepage&q=
              pseudo%20reduced%20temperature&f=false
        - gas visc calc http://www.lmnoeng.com/Flow/GasViscosity.php
        - https://www.cedengineering.com/upload/Gas%20Pipeline%20Hydraulics.pdf
        - http://www.squinch.org/gas/aga10.htm

        - http://www.amazon.de/Gas-Pipeline-Hydraulics-Shashi-Menon/dp/
          0849327857/ref=tmm_hrd_title_0?ie=UTF8&qid=1406292142&sr=1-1-catcorr

        AGA-8 and AGA-10:
        1) Compressibility Factors of Natural Gas and Other Related Hydrocarbon
           Gases by K.E. Starling and J.L. Savidge. 2nd.Ed. Nov.1992. 2nd
           Printing Jul.1994

        2) AGA Report No. 10, Speed of Sound in Natural Gas and Other Related
           Hydrocarbon Gases, Catalog #XQ0310, Prepared by Transmission
           Measurement Committee, 2003 American Gas Association.

        3) Lee, A., Gonzalex, M., Ekain, B. (1966), "The Viscosity of Natural
           Gases", SPE Paper 1340, Journal of Petroleum Technology, vol, 18,
           p. 997-1000.
    """

    def __init__(self, identifier: str = 'gas',
                 latex: str | None = None,
                 comment: str | None = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier. If None, identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.D_in_air = Property('D_in_air', 'm2/s', latex='$D_{air}$',
                                 calc=lambda T, p=atm(), x=0.: 0.,
                                 comment='diffusity in air')
        self.T.ref = C2K(20.)
