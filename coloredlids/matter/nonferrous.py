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
      2018-09-17 DWW
"""

from typing import Optional

from coloredlids.matter.parameter import C2K
from coloredlids.matter.generic import NonFerrous


class Aluminum(NonFerrous):
    """
        Properties of aluminum
    """

    def __init__(self, identifier: str='Al',
                 latex: Optional[str]=None,
                 comment: Optional[str]=None) -> None:
        """
        Args:
            identifier:
                identifier of matter

            latex:
                Latex-version of identifier. If None, identifier is assigned

            comment:
                comment on matter. If None, comment is empty

        Reference:
            http://en.wikipedia.org/wiki/Aluminum, 2008-06-20, 01:30pm CET
        """
        super().__init__(identifier, latex=latex, comment=comment)

        self.T.ref = C2K(20)

        self.nu_mech      = None
        self.friction     = None
        self.E.calc       = lambda T=0, p=0, x=0: None

        self.T_sol        = 933.47
        self.T_liq        = 933.47
        self.T_vap        = 2793.0
        self.M            = 26.9815386e-3  # [kg/mol]
        h_melt_mol        = 10.71e3        # [J/mol]
        h_vap_mol         = 294e3          # [J/mol]
        self.h_melt       = h_melt_mol / self.M
        self.h_vap        = h_vap_mol / self.M

        self.beta.calc    = lambda T=0, p=0, x=0: 23.1e-6
        self.c_p.calc     = lambda T=0, p=0, x=0: 24.2 / self.M
        self.Lambda.calc  = lambda T=0, p=0, x=0: 237
        self.rho.calc     = lambda T=0, p=0, x=0: 2700 if T < self.T_sol \
                                                           else 2375
        self.rho_el.calc  = lambda T=0, p=0, x=0: 26.5e-9


class Copper(NonFerrous):
    """
        Properties of copper
    """

    def __init__(self, identifier: str='Cu',
                 latex: Optional[str]=None,
                 comment: Optional[str]=None) -> None:
        """
        Args:
            identifier:
                identifier of matter

            latex:
                Latex-version of identifier. If None, identifier is assigned

            comment:
                comment on matter. If None, comment is empty
        """
        super().__init__(identifier, latex=latex, comment=comment)

        self.T.ref = C2K(20)

        self.nu_mech      = None
        self.friction     = None
        self.E.calc       = lambda T=0, p=0, x=0: 137.8e+9

        self.T_sol        = C2K(2560)
        self.beta.calc    = lambda T=0, p=0, x=0: 16.3e-6
        self.c_p.calc     = lambda T=0, p=0, x=0: 129
        self.Lambda.calc  = lambda T=0, p=0, x=0: 386
        self.rho.calc     = lambda T=0, p=0, x=0: 8960
