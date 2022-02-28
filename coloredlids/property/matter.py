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
      2020-12-22 DWW
"""

from collections import  OrderedDict
import numpy as np
from typing import Dict, Optional, Union

try:
    from conversion import atm, C2K
    from property import Property
except:
    from coloredlids.property.conversion import atm, C2K
    from coloredlids.property.property import Property


class Matter(Property):
    """
    Collection of physical and chemical properties of generic matter
    """

    def __init__(self, identifier: str = 'matter',
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
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

        self.a = Property('a', 'm$^2$/s', comment='thermal diffusity',
                          calc = self._a)        
        self.beta = Property('beta', '1/K', latex=r'$\beta_{th}$',
                             comment='volumetric thermal expansion')
        self.c_p = Property('c_p', 'J/kg/K',
                            comment='specific heat capacity')
        self.c_sound = Property('c_sound', 'm/s', latex='$c_{sound}$')
        self.c_sound.calc = lambda T, p, x: None
        self.composition: Dict[str, float] = OrderedDict()
        self.compressible: bool = False
        self.E = Property('E', 'Pa', comment="Young's (elastic) modulus")
        self.h_melt: float = None
        self.h_vap: float = None
        self.k = Property('k', 'W/m/K', latex='$k$',
                                comment='thermal conductivity')
        self.M = Property('M', 'kmol/kg', comment='molar mass')
        self.M.calc = lambda T=0, p=0, x=0: None
        self.nu_mech: float = None
        self.rho = Property('rho', 'kg/m$^3$', latex=r'$\varrho$', ref=1.,
                            comment='density')
        self.rho.T.ref = C2K(20.)
        self.rho.p.ref = atm()
        self.rho_el = Property('rho_el', r'$\Omega$', latex=r'$\varrho_{el}$',
                               comment='electric resistance')
        self.T_boil: float = 0.
        self.T_flash_point: float = 0.
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

    def _a(self, T: float, p: float = atm(), x: float = 0.) -> Optional[float]:
        try:
            k = self.k(T, p, x)
            c_p = self.c_p(T, p, x)
            rho = self.rho(T, p, x)
            if k is None or c_p is None or rho is None:
                return None
            c_p__rho = c_p * rho
            if np.abs(c_p__rho) < 1e-10:
                return None
            return k / c_p__rho
        except:
            return None

    def set_all_ref(self, T: float, p: float = atm(), x: float = 0.) -> bool:
        none_set = True 
        for attr in dir(self):
            if not attr.startswith('_'):
                val = getattr(self, attr)
                if isinstance(val, Property):
                    print(f'{attr=}, {val=}')
                    none_set = False
                    val.T.ref = T
                    val.p.ref = p
                    val.x.ref = x
        return not none_set


    def plot(self, prop: Optional[Union[Property, str]] = None) -> None:
        if prop is None or prop.lower() == 'all':
            for key, val in self.__dict__.items():
                
                print(f'{val.T.ref=}, {val.p.ref=}, {val.x.ref=}')
                
                if isinstance(val, Property):
                    print(f"+++ Plot matter: '{self.identifier}', "
                          f"property: '{key}'")
                    val.plot()
        else:
            if prop in self.__dict__:
                if prop is not None:
                    self.__dict__[prop].plot(title=self.identifier)
                else:
                    self.write('!!! No plot of property:', prop)

class Solid(Matter):
    """
    Collection of physical and chemical properties of generic solid
    """

    def __init__(self, identifier: str = 'solid',
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
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

    def __init__(self, identifier: str = 'nonmetal',
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
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

    def __init__(self, identifier: str = 'metal',
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
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

    def __init__(self, identifier: str = 'nonferrous',
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
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

    def __init__(self, identifier: str = 'ferrous',
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
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

    def __init__(self, identifier: str = 'fluid',
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
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

        # self.a.calc = self._a
        self.mu = Property('mu', 'Pa s', latex=r'$\mu$',
                           comment='dynamic viscosity', calc = self._mu)
        self.nu = Property('nu', 'm^2/s', latex=r'$\nu$',
                           comment='kinematic viscosity', calc = self._nu)


    # def _a(self, T: float, p: float = atm(), x: float = 0.) -> Optional[float]:
    #     try:
    #         lam = self.k(T, p, x)
    #         c_p = self.c_p(T, p, x)
    #         rho = self.rho(T, p, x)
    #         if lam is None or c_p is None or rho is None:
    #             return None
    #         c_p__rho = c_p * rho
    #         if np.abs(c_p__rho) < 1e-10:
    #             return None
    #         return lam / c_p__rho
    #     except:
    #         return None

    def _mu(self, T: float, p: float = atm(), 
            x: float = 0.) -> Optional[float]:
        try:
            return self.nu(T, p, x) * self.rho(T, p, x)
        except:
            return None

    def _nu(self, T: float, p: float = atm(), 
            x: float = 0.) -> Optional[float]:
        try:
            rho = self.rho(T, p, x)
            if rho is None or np.abs(rho) < 1e-10:
                return None
            return self.mu(T, p, x) / rho
        except:
            return None

            

class Liquid(Fluid):
    """
    Collection of physical and chemical properties of generic liquid
    """

    def __init__(self, identifier: str = 'liquid',
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
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
    Collection of physical and chemical properties of generic gas

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
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
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

        # self.a.calc = self._a
        self.D_in_air = Property('D_in_air', 'm2/s', 
                                 calc=lambda T, p=atm(), x=0.: None)
        self.T.ref = C2K(15.)        


        