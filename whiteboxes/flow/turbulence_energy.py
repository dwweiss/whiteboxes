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
      2018-09-14 DWW
"""

from typing import Tuple


def initial_turbulence_energy_and_dissipation(v: float, D: float, nu: float) \
        -> Tuple[float, float]:
    """
    Turbulence kinetic energy and dissipation rate

    Args:
        v:
            axial component of velocity [m/s]

        D:
            inner pipe diameter [m]

        nu:
            kinematic viscosity [m^2/s]

    Returns:
        k_turb:
            turbulent kinetic energy [m^2/s^2]

        eps_turb:
            turbulence dissipation rate [m/s^2]
    """
    C_u = 0.09                              # turbulence model constant [m/s^2]
    Re = v * D / nu                         # Reynolds number [/]
    I = 0.16 * Re**-0.125                   # turbulence intensity [/]
    L = 0.07 * D                            # turbulence length scale [m]
    k_turb = 1.5 * (v * I)**2               # turb. kinetic energy [m^2/s^2]
    eps_turb = C_u**0.75 * k_turb**1.5 / L  # turb. dissipation rate [m/s^2]
    return k_turb, eps_turb

