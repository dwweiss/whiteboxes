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
      2018-06-25 DWW
"""

import numpy as np
from coloredlids.matter.parameter import C2K
from coloredlids.matter.genericmatter import Fluid
from coloredlids.matter.air import Air


class FreeConvectionPlate(object):
    """
      Heat transfer coefficient for free convection and radiation on heated
      plates:
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
            The formulas for horizontal plates are also applicable to cold
            plates if alpha_LUpper() is used for the LOWER cooled plate and
            alpha_LLower() for the UPPER cooled plate

        Reference:
            [INCR96] Incropera and DeWitt: Fundamentals of Heat and Mass
                Transfer, Wiley 1996

        Example:
            TSurf = C2K(100)     # [K]
            TInf = C2K(20)       # [K]
            phiPlate = 90        # [deg], vertical plate

            foo = PlateConvRad()
            foo.fluid = Air()
            foo.epsRad = 0.95
            alpha = foo.alphaConvRad(TSurf, TInf, L, phiPlate)
    """

    def __init__(self, fluid=None, eps_rad=None):
        self._fluid = fluid if fluid is not None else Air()

        # emissivity of plate surface
        self._eps_rad = eps_rad if eps_rad is not None else 0.5

    @property
    def fluid(self):
        return self._fluid

    @fluid.setter
    def fluid(self, value):
        if value is not None:
            if self._fluid is not None:
                del self._fluid
            self._fluid = value

    @property
    def eps_rad(self):
        return self._eps_rad

    @eps_rad.setter
    def eps_rad(self, value):
        self._eps_rad = np.clip(value, 0, 1)

    def alphaConv(self, TSurf, TInf, L, phiPlate=0):
        """
        Computes convective heat transfer coefficient for natural convection

        Args:
            TSurf (float):
                surface temperature [K]

            TFluid (float):
                temperature outside film [K]

            L (float):
                characteristic length [m],
                vertical plate: L = height, horizontal: L = width

            phiPlate (float, optional):
                counter-clockwise rotation of plate around y-axis [deg],
                - phi = 0        deg : horizontal upper face of heated plate
                - phi = 90       deg : vertical heated plate
                - phi = 180      deg : horizontal lower face of heated plate
                - 30 <= phi < 90 deg : inclined face of heated plate

        Returns:
            (float):
                Convective heat transfer coefficient alpha_conv [W/(m^2 K)]

           z ^
           |
           |<-__
           |phi \   cold
           +-====\=======----> x
           y         hot
        """
        assert TSurf > TInf

        if phiPlate == 0:
            return self.alpha_LUpper(TSurf, TInf, L)
        elif 30 <= phiPlate and phiPlate <= 90:
            return self.alpha_LVert(TSurf, TInf, L, np.abs(90 - phiPlate))
        elif phiPlate == 180:
            return self.alpha_LUpper(TSurf, TInf, L)
        else:
            print('??? alphaConv() phiPlate:', phiPlate)
            return np.inf

    def alphaRad(self, TSurf, TInf):
        """
        Computes equivalent heat transfer coefficient for radiation

        Args:
            TSurf (float):
                surface temperature [K]

            TInf (float):
                fluid temperature outside film [K]

        Returns:
            (float):
                Equivalent radiative heat transfer coefficient
                alpha_rad [W/(m^2 K)]
        """
        dT = TSurf - TInf
        if np.abs(dT) < 1e-20:
            return 0
        e = self.eps_rad * 5.67e-8 * (TSurf**4 - TInf**4)
        return e / dT

    def alphaCombined(self, TSurf, TInf, L, phiPlate=0):
        """
        Computes convective heat transfer coefficient for natural
        convection and radiation

        Args:
            TSurf (float):
                surface temperature [K]

            TInf (float):
                fluid temperature outside film [K]

            L (float):
                characteristic length [m], vertical plate: L = heigth,
                horizontal: L = width

            phiPlate (float, optional):
                counter-clockwise rotation of plate around y-axis [deg],
                - phi=0      deg : horizontal upper face of heated plate
                - phi=90     deg : vertical heated plate
                - phi=180    deg : horizontal lower face of heated plate
                - 30<=phi<90 deg : inclined face of heated plate

         Returns:
             (float):
                 Combined heat transfer coefficient alpha_eff
                 considering convection and radiation [W/(m^2 K)]

        z ^
          |
          | <-_
          |phi \  cold
          +-====\=======----> x
         y        hot
        """
        return self.alphaConv(TSurf, TInf, L, phiPlate) + \
            self.alphaRad(TSurf, TInf)

    def alpha_LVert(self, TSurf, TInf, L, theta=0):
        """
        Computes convective heat transfer coefficient for natural
        convection on vertical or inclined plates

        Args:
            TSurf (float):
                surface temperature [K]

            TInf (float):
                fluid temperature outside film [K]

            L (float):
                characteristic length [m], vertical plate: L = heigth

            theta (float):
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
            (float):
                Convective heat transfer coefficient alpha_conv [W/(m^2 K)]

        """
        isinstance(self.fluid, Fluid)
        assert L > 1e-20
        assert 0 <= theta and theta <= 60

        TFilm = 0.5 * (TSurf + TInf)
        Ra_L = self.rayleigh_L(TSurf, TInf, L, theta)

        return self.nusselt_LVert(Ra_L, L) * self.fluid.Lambda(TFilm) / L

    def alpha_LUpper(self, TSurf, TInf, L):
        """
        Computes convective heat transfer coefficient for natural convection at
        the upper side of a HEATED horizontal plate TSurf > TInf

        Args:
            TSurf (float):
                surface temperature [K]

            TInf (float):
                fluid temperature outside film [K]

            L (float):
                characteristic length of geometry [m]

        Returns:
            (float):
                Convective heat transfer coefficient [W/(m K)]

        Note:
            This function is also applicable to upper COOLED plates with
            TSurf < TInf
        """
        assert isinstance(self.fluid, Fluid)
        assert L > 1e-20

        TFilm = 0.5 * (TSurf + TInf)
        Ra_L = self.rayleigh_L(TSurf, TInf, L)

        return self.nusselt_LUpper(Ra_L) * self.fluid.Lambda(TFilm) / L

    def alpha_LLower(self, TSurf, TInf, L):
        """
        Computes convective heat transfer coefficient for natural convection at
        the lower side of a HEATED horizontal plate where TSurf > TInf

        Args:
            TSurf (float):
                surface temperature [K]

            TInf (float):
                fluid temperature outside film [K]

            L (float):
                characteristic length of geometry [m]

        Returns:
            (float):
                Convective heat transfer coefficient [W/(m K)]

        Note:
            This function is also applicable to upper COOLED plates with
            TSurf < TInf
        """
        assert isinstance(self.fluid, Fluid)
        assert L > 1e-20

        TFilm = 0.5 * (TSurf + TInf)
        Ra_L = self.rayleigh_L(TSurf, TInf, L)

        return self.nusselt_LLower(Ra_L) * self._fluid.Lambda(TFilm) / L

    def nusselt_LVert(self, Ra_L, Pr):
        """
        Computes Nusselt number Nu = Nu( Ra_L, Pr ) for natural convection
        at the vertical plate

        Args:
           Ra_L (float):
               Rayleigh number [/] Ra = Gr_L * Pr

           Pr (float):
               Prandtl number [/]

        Returns:
            (float):
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

    def nusselt_LUpper(self, Ra_L):
        """
        Computed Nusselt number Nu = Nu( Ra_L ) for natural convection
        at the upper surface of a heated plate

        Args:
            Ra_L Raleigh number [/] Ra = Gr_L * Pr

        Returns:
            (float):
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

    def nusselt_LLower(self, Ra_L):
        """
        Computes Nusselt number Nu = Nu( Ra_L ) for natural convection at
        the lower surface of a heated plate

        Args:
            Ra_L Raleigh number [/], Ra = Gr_L * Pr

        Returns:
            (float):
                Nusselt number [/]

        References:
            [INCR96] Equ (9.32) if Ra_L <= 1e10
        """
        assert 1e5 <= Ra_L and Ra_L <= 1e11

        return 0.27 * Ra_L**0.25

    def rayleigh_L(self, TSurf, TInf, L, theta=0):
        """
        Computes Rayleigh number Ra_L = Gr_L * Pr as function of
        temperature and characteristic length; theta can be optionally
        used for tuning of Ra_L in case of inclined plates

        Args:
            TSurf (float):
                surface temperature [K]

            TInf (float):
                fluid temperature outside film [K]

            L (float):
                chacteristic length of geometry [m]

            theta (float, optional):
                angle between vertical axis and inclined plate [deg],
                  theta_plate = 0 corresponds to the vertical plate

        Returns:
            (float):
                Rayleigh number Ra [/]

        Note:
             Maximum of theta is 60 deg

        Reference:
            B R Rich: An Investigation of Heat Transfer from an Inclined Flat
            Plate in Free Convection, Trans. ASME,(75) 489, 1953

                         /|
                        / |
                       /  |
                      L   |
               plate /    |
                    /<--->|
                   / theta|
           """
        assert isinstance(self.fluid, Fluid)
        assert TInf > 200                         # both temperatures in Kelvin
        assert TSurf > 0 and np.abs(TSurf - TInf) > 0
        assert L > 0

        TFilm = 0.5 * (TSurf + TInf)
        beta = 1.0 / TFilm
        nu = self.fluid.nu(TFilm)
        a = self.fluid.a(TFilm)
        g = 9.81 * np.cos(np.radians(theta))

        return g * beta * np.abs(TSurf - TInf) * L**3 / (nu * a)

    def prandtl(self, TSurf, TInf):
        """
        Computes Prandtl number Pr as function of film temperature
        T_film = (T_surf + T_inf) / 2

        Args:
            TSurf (float):
                surface temperature [K]

            TInf (float):
                fluid temperature outside film [K]

        Returns:
            (float):
                Prandtl number [/]
        """

        assert isinstance(self.fluid, Fluid)
        assert TSurf > 0 and TInf > 0

        TFilm = 0.5 * (TSurf + TInf)

        return self.fluid.Pr(TFilm)


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 0 or ALL:
        def main():
            TSurf = C2K(40)      # [K]
            TInf = C2K(20)       # [K]
            phiPlate = 90        # [deg], vertical plate
            L = 0.1

            foo = FreeConvectionPlate(fluid=Air(), eps_rad=0.5)
            alphaConv = foo.alphaConv(TSurf=TSurf, TInf=TInf, L=L,
                                      phiPlate=phiPlate)
            alphaRad = foo.alphaRad(TSurf=TSurf, TInf=TInf)
            alphaComb = foo.alphaCombined(TSurf=TSurf, TInf=TInf, L=L,
                                          phiPlate=phiPlate)

            for key in sorted(locals(), key=lambda s: s.lower()):
                if key not in ('foo', 'kwargs'):
                    x = locals()[key]
                    if isinstance(x, float) and abs(x) > 0.1:
                        x = round(x, 3)
                    print('{:>15}: {}'.format(key, x))

        main()
