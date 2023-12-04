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
      2019-11-19 DWW
"""

import numpy as np
from typing import Optional

from whiteboxes.matter.gases import Air
from whiteboxes.matter.generic import Fluid


class FreeConvectionPlate(object):
    """
      Heat transfer coefficient for free convection and radiation on 
      heated plates:
         - horizontal upper face of heated plate
         - vertical heated plate
         - horizontal lower face of heated plate
         - inclined face of heated plate

       \begin{array}{rcl}
                 \dot Q & = & \alpha_{eff} \, \Delta T\, A \\[2mm]
           \alpha_{eff} & = & \alpha_{rad} \, +\, \alpha_{conv} \\[2mm]
           \alpha_{rad} & = & \varepsilon_{rad}\, \sigma_{rad}\,
                              \frac{T_{surf}^4\, -\, T_{\infty}^4}
                                   {T_{surf}\,   -\, T_{|infty}  } \\[2mm]
          \alpha_{conv} & = & \frac{\lambda\, Nu}{L} \\[2mm]
                     Nu & = & Nu( Ra, Pr ) \\[2mm]
                     Ra & = & Gr\, Pr \\[2mm]
                     Gr & = & \frac{g\,\beta\,\vert T_{surf}\,-\,T_\infty
                              \vert\, L^3}
                      {\nu^2\, a} \\[2mm]
                     Pr & = & \frac{\nu}{a} \\[2mm]
       \end{array}

        Note:
            The formulas for horizontal plates are also applicable to 
            cold plates if alpha_LUpper() is used for the LOWER cooled 
            plate and alpha_LLower() for the UPPER cooled plate

        Reference:
            [INCR96] Incropera and DeWitt: Fundamentals of Heat and Mass
                Transfer, Wiley 1996

        Example:
            from colordlids.data.conversion import C2K
            
            T_surf = C2K(100)     # [K]
            T_inf = C2K(20)       # [K]
            phi_plate = 90        # [deg], vertical plate

            foo = PlateConvRad()
            foo.fluid = Air()
            foo.eps_rad = 0.95
            alpha = foo.alpha_conv_rad(T_surf, T_inf, L, phi_plate)
    """

    def __init__(self, fluid: Optional[Fluid] = None, 
                       eps_rad: Optional[float] = None) -> None:
        self._fluid = fluid if fluid is not None else Air()

        # emissivity of plate surface
        self._eps_rad = eps_rad if eps_rad is not None else 0.5

    @property
    def fluid(self) -> Fluid:
        return self._fluid

    @fluid.setter
    def fluid(self, value: Fluid) -> None:
        if value is not None:
            if self._fluid is not None:
                del self._fluid
            self._fluid = value

    @property
    def eps_rad(self) -> float:
        return self._eps_rad

    @eps_rad.setter
    def eps_rad(self, value: float) -> None:
        self._eps_rad = np.clip(value, 0, 1)

    def alpha_conv(self, T_surf: float, T_inf: float, L: float, 
                   phi_plate: float = 0.) -> float:
        """
        Convective heat transfer coefficient for natural convection

        Args:
            T_surf:
                surface temperature [K]

            T_inf:
                temperature outside film [K]

            L:
                characteristic length [m],
                vertical plate: L = height, horizontal: L = width

            phi_plate:
                counter-clockwise rotation of plate around y-axis [deg],
                - phi = 0        deg : horizontal upper face of heated plate
                - phi = 90       deg : vertical heated plate
                - phi = 180      deg : horizontal lower face of heated plate
                - 30 <= phi < 90 deg : inclined face of heated plate

        Returns:
            Convective heat transfer coefficient alpha_conv [W/(m^2 K)]

           z ^
           |
           |<-__
           |phi \   cold
           +-====\=======----> x
           y         hot
        """
        assert T_surf > T_inf

        phi_plate = float(phi_plate)
        if phi_plate == 0.:
            return self.alpha_LUpper(T_surf, T_inf, L)
        elif 30. <= phi_plate and phi_plate <= 90.:
            return self.alpha_L_vert(T_surf, T_inf, L, np.abs(90. - phi_plate))
        elif phi_plate == 180.:
            return self.alpha_L_upper(T_surf, T_inf, L)
        else:
            print('??? invalid alpha_conv() phi_plate:', phi_plate)
            return np.inf

    def alpha_rad(self, T_surf: float, T_inf: float) -> float:
        """
        Computes equivalent heat transfer coefficient for radiation

        Args:
            T_surf:
                surface temperature [K]

            T_inf:
                fluid temperature outside film [K]

        Returns:
            Equivalent radiative heat transfer coefficient
            alpha_rad [W/(m^2 K)]
        """
        dT = T_surf - T_inf
        if np.abs(dT) < 1e-20:
            return 0
        e = self.eps_rad * 5.67e-8 * (T_surf**4 - T_inf**4)
        return e / dT

    def alpha_combined(self, T_surf: float, T_inf: float, L: float, 
                       phi_plate: float = 0.) -> float:
        """
        Computes convective heat transfer coefficient for natural
        convection and radiation

        Args:
            T_surf:
                surface temperature [K]

            T_inf:
                fluid temperature outside film [K]

            L:
                characteristic length [m], vertical plate: L = heigth,
                horizontal: L = width

            phi_plate:
                counter-clockwise rotation of plate around y-axis [deg],
                - phi=0      deg : horizontal upper face of heated plate
                - phi=90     deg : vertical heated plate
                - phi=180    deg : horizontal lower face of heated plate
                - 30<=phi<90 deg : inclined face of heated plate

         Returns:
             Combined heat transfer coefficient alpha_eff
             considering convection and radiation [W/(m^2 K)]

        z ^
          |
          | <-_
          |phi \  cold
          +-====\=======----> x
         y        hot
        """
        return self.alpha_conv(T_surf, T_inf, L, phi_plate) + \
            self.alpha_rad(T_surf, T_inf)

    def alpha_L_vert(self, T_surf: float, T_inf: float, L: float, 
                     theta: float = 0.) -> float:
        """
        Computes convective heat transfer coefficient for natural
        convection on vertical or inclined plates

        Args:
            T_surf:
                surface temperature [K]

            T_inf:
                fluid temperature outside film [K]

            L:
                characteristic length [m], vertical plate: L = heigth

            theta:
                angle between vertical and inclined plate, 0 <= theta <= 60,
                theta=0 corresponds to the full vertical plate [deg]

                   /|
                  / |
                 /  |
                L   |
         plate /    |
              /<--->|
             / theta|

        Returns:
            Convective heat transfer coefficient alpha_conv [W/(m^2 K)]

        """
        isinstance(self.fluid, Fluid)
        assert L > 1e-20
        assert 0 <= theta and theta <= 60

        T_film = 0.5 * (T_surf + T_inf)
        Ra_L = self.rayleigh_L(T_surf, T_inf, L, theta)

        return self.nusselt_L_vert(Ra_L, L) * self.fluid.lambda_(T_film) / L

    def alpha_L_upper(self, T_surf: float, T_inf: float, L: float) -> float:
        """
        Computes convective heat transfer coefficient for natural convection at
        the upper side of a HEATED horizontal plate T_surf > T_inf

        Args:
            T_surf:
                surface temperature [K]

            T_inf:
                fluid temperature outside film [K]

            L:
                characteristic length of geometry [m]

        Returns:
            Convective heat transfer coefficient [W/(m K)]

        Note:
            This function is also applicable to upper COOLED plates with
            T_surf < T_inf
        """
        assert isinstance(self.fluid, Fluid)
        assert L > 1e-20

        T_film = 0.5 * (T_surf + T_inf)
        Ra_L = self.rayleigh_L(T_surf, T_inf, L)

        return self.nusselt_L_upper(Ra_L) * self.fluid.lambda_(T_film) / L

    def alpha_L_lower(self, T_surf: float, T_inf: float, L: float) -> float:
        """
        Computes convective heat transfer coefficient for natural 
        convection at lower side of a HEATED horizontal plate where 
        T_surf > T_inf

        Args:
            T_surf:
                surface temperature [K]

            T_inf:
                fluid temperature outside film [K]

            L:
                characteristic length of geometry [m]

        Returns:
            Convective heat transfer coefficient [W/(m K)]

        Note:
            This function is also applicable to upper COOLED plates with
            T_surf < T_inf
        """
        assert isinstance(self.fluid, Fluid)
        assert L > 1e-20

        T_film = 0.5 * (T_surf + T_inf)
        Ra_L = self.rayleigh_L(T_surf, T_inf, L)

        return self.nusselt_L_lower(Ra_L) * self._fluid.lambda_(T_film) / L

    def nusselt_L_vert(self, Ra_L: float, Pr: float) -> float:
        """
        Computes Nusselt number Nu = Nu( Ra_L, Pr ) for natural convection
        at the vertical plate

        Args:
           Ra_L:
               Rayleigh number [/] Ra = Gr_L * Pr

           Pr:
               Prandtl number [/]

        Returns:
            Nusselt number [/]

        Reference:
            [INCR96] Equ (9.26) if Ra_L <= 1e9 and Equ. (9.27)
                     if Ra_L > 1e9
        """
        assert Pr > 1e-20
        assert 0 < Ra_L and Ra_L < 1e30

        if Ra_L <= 1e9:
            return 0.68 + 0.67 * pow(Ra_L, 0.25) \
                / pow(1 + pow(0.492 / Pr, 9./16), 4./9)
        else:
            return np.sqr(0.825 + 0.387 * np.pow(Ra_L, 1./6)
                          / pow(1 + pow(0.492 / Pr, 9./16), 8./27))

    def nusselt_L_upper(self, Ra_L: float) -> float:
        """
        Computed Nusselt number Nu = Nu( Ra_L ) for natural convection
        at the upper surface of a heated plate

        Args:
            Ra_L:
                Raleigh number [/] Ra = Gr_L * Pr

        Returns:
            Nusselt number [/]

        Reference:
            [INCR96] Equ (9.30) if Ra_L <= 1e7 and
                     Equ. (9.31) if Ra_L > 1e7
        """
        assert 1e4 <= Ra_L and Ra_L <= 1e11

        if Ra_L <= 1e7:
            return 0.54 * Ra_L**0.25
        else:
            return 0.15 * Ra_L**0.3333333

    def nusselt_L_lower(self, Ra_L: float) -> float:
        """
        Computes Nusselt number Nu = Nu( Ra_L ) for natural convection at
        the lower surface of a heated plate

        Args:
            Ra_L:
                Raleigh number [/], Ra = Gr_L * Pr

        Returns:
            Nusselt number [/]

        References:
            [INCR96] Equ (9.32) if Ra_L <= 1e10
        """
        assert 1e5 <= Ra_L and Ra_L <= 1e11

        return 0.27 * Ra_L**0.25

    def rayleigh_L(self, T_surf: float, T_inf: float, L: float, 
                   theta: float = 0.) -> float:
        """
        Computes Rayleigh number Ra_L = Gr_L * Pr as function of
        temperature and characteristic length; theta can be optionally
        used for tuning of Ra_L in case of inclined plates

        Args:
            T_surf:
                surface temperature [K]

            T_inf:
                fluid temperature outside film [K]

            L:
                chacteristic length of geometry [m]

            theta:
                angle between vertical axis and inclined plate [deg],
                  theta_plate = 0 corresponds to the vertical plate

        Returns:
            Rayleigh number Ra [/]

        Note:
             Maximum of theta is 60 deg

        Reference:
            B R Rich: An Investigation of Heat Transfer from an Inclined 
            Flat Plate in Free Convection, Trans. ASME,(75) 489, 1953

                         /|
                        / |
                       /  |
                      L   |
               plate /    |
                    /<--->|
                   / theta|
           """
        assert isinstance(self.fluid, Fluid)
        assert T_inf > 200                 # both temperatures in Kelvin
        assert T_surf > 0 and np.abs(T_surf - T_inf) > 0
        assert L > 0

        T_film = 0.5 * (T_surf + T_inf)
        beta = 1.0 / T_film
        nu = self.fluid.nu(T_film)
        a = self.fluid.a(T_film)
        g = 9.81 * np.cos(np.radians(theta))

        return g * beta * np.abs(T_surf - T_inf) * L**3 / (nu * a)

    def prandtl(self, T_surf: float, T_inf: float) -> float:
        """
        Computes Prandtl number Pr as function of film temperature
        T_film = (T_surf + T_inf) / 2

        Args:
            T_surf:
                surface temperature [K]

            T_inf:
                fluid temperature outside film [K]

        Returns:
            Prandtl number [/]
        """

        assert isinstance(self.fluid, Fluid)
        assert T_surf > 0 and T_inf > 0

        T_film = 0.5 * (T_surf + T_inf)

        return self.fluid.Pr(T_film)
