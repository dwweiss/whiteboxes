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

  Version
      2018-09-17 DWW
"""

from math import sqrt
from typing import Optional


def sutherland_viscosity(identifier: str,
                         T: float,
                         T0: float,
                         mu0: float) -> Optional[float]:
    """
    Sutherland approximation of gas viscosity

    Args:
        identifier:
            Identifier out of [ "AIR" "CO2" "H2" "N2" "NH3" "O2" ]

        T:
            Temperature [K]

        T0:
            Reference temperature [K]

        mu0:
            Reference dynamic viscosity [Pa s]

    Returns:
        Dynamic viscosity [Pa s],
        or
        None if identifier is unknown

    Reference:
        Crane: Flow of fluids trough valves, fittings and pipe. Technical paper
        No 410, 1988

        Gas             C_s [K] T0 [K]  mu0 [micro-Pa s]
        air             120     291.15  18.27
        nitrogen        111     300.55  17.81
        oxygen          127     292.25  20.18
        carbon dioxide  240     293.15  14.8
        carbon monoxide 118     288.15  17.2
        hydrogen        72      293.85  8.76
        ammonia         370     293.15  9.82
        sulfur dioxide  416     293.65  12.54
        helium          79.4    273     19
    """

    identifier.upper()
    if   identifier == "AIR": C_s = 120.0
    elif identifier == "CO2": C_s = 240.0
    elif identifier == "H2" : C_s =  72.0
    elif identifier == "N2" : C_s = 111.0
    elif identifier == "NH3": C_s = 370.0
    elif identifier == "O2" : C_s = 127.0
    else:
        return None

    a = 0.555 * T0 + C_s
    b = 0.555 * T + C_s
    T_tilde = T / T0

    return mu0 * a / b * T_tilde * sqrt(T_tilde)
