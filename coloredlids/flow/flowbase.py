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
      2019-09-27 DWW
"""

import numpy as np
from typing import Optional, Tuple

from coloredlids.matter.property import Parameter, Property, C2K
from coloredlids.matter.generic import Fluid
from coloredlids.matter.liquids import Water


class FlowBase(Property):
    """
    Properties of flow in pipework with circular or rectangular 
    cross-section
    """

    def __init__(self, identifier: str='Flow', 
                 d_pipe: Optional[float]=None, 
                 w_h_pipe: Optional[Tuple[float, float]] = None,
                 v: float=1.,
                 fluid: Optional[Fluid]= None) -> None:
        """
           ------              _---_      ^
        h |      |           _-     -_    |
          |      |           -_     _-    | d_pipe
           ------              -___-      v
             w           
        
        Args:
            identifier:
                indentifier of flow

            d_pipe:
                inner diameter if circular cross-section [m]

            w_h_pipe:
                width and height of rectangular cross-section [m, m]

            v:
                speed (mean velocity) [m/s]
                
            fluid:
                fluid object, default is Water

        Note:
            If both d_pipe and w_h_pipe are given, w_h_pipe is ignored
        """
        super().__init__(identifier=identifier)

        self._fluid: Optional[Fluid] = None

        self.T.val: float = C2K(20)
        self.p.val: float = self.p.ref

        self._v: float = Parameter(identifier='v', unit='m/s', val=v)
        self._A: float = 0.
        self._m_dot: float = 0.
        self._V_dot: float = 0.

        self._d_pipe: Optional[float] = None
        self._w_h_pipe: Optional[Tuple[float, float]] = None

        if d_pipe is not None:
            self.d_pipe = d_pipe
        elif w_h_pipe is not None:
            self.w_h_pipe = w_h_pipe
        else:
            self.d_pipe = 1.

        if fluid is None:
            self.fluid = Water()
        else:
            self.fluid = fluid 
            assert isinstance(self.fluid, Fluid)

    @property
    def fluid(self) -> Fluid:
        """
        Returns:
            fluid object
        """
        return self._fluid

    @fluid.setter
    def fluid(self, value: Fluid) -> None:
        """
        Sets fluid

        Args:
            value: 
                fluid object
        """
        del self._fluid
        self._fluid = value

    def h_dot(self) -> float:
        """
        Returns:
            enthalpy flow rate [J/kg]
        """
        return self.T() * self.fluid.c_p(self.T()) * self.m_dot

    @property
    def v(self) -> float:
        """
        Returns:
            speed [m/s]
        """
        return self._v

    @v.setter
    def v(self, value: float) -> None:
        """
        Sets speed 
        Updates volume and mass flow rate

        Args:
            value: 
                speed [m/s]
        """
        self._v = value
        self._V_dot = self._A * self._v
        self._m_dot = self._V_dot * self.fluid.rho(self.T(), self.p(), 0.)

    @property
    def d_pipe(self) -> float:
        """
        Returns:
            inner pipe diameter [m]
        """
        return self._d_pipe

    @d_pipe.setter
    def d_pipe(self, value: float) -> None:
        """
        Sets diameter of pipe with circular cross-section
        Updates area, volume flow rate and mass flow rate

        Args:
            value: 
                inner pipe diameter [m]
        """
        self._d_pipe = value
        self._A = np.pi * 0.25 * self.d_pipe**2
        self._V_dot = self._A * self.v()
        self._m_dot = self._V_dot * self.fluid.rho(self.T(), self.p(), 0.)

    @property
    def w_h_pipe(self) -> Tuple[float, float]:
        """
        Returns:
            width and height of rectangular cross-section [m]
        """
        return self._w_h_pipe

    @w_h_pipe.setter
    def w_h_pipe(self, value: Tuple[float, float]) -> None:
        """
        Sets width and height of cross-sectional area of pipe with 
            rectangular cross-section
        Updates area, volume and mass flow rate

        Args:
            width and height of rectangular cross-section [m]
        """
        self._w_h_pipe = np.atleast_1d(value)
        assert len(self._w_h_pipe) == 2, str(self._w_h_pipe)

        self._A = self._w_h_pipe[0] * self._w_h_pipe[1]
        self._V_dot = self._A * self.v()
        rho = self.fluid.rho(self.T(), self.p(), 0.)
        self._m_dot = self._V_dot * rho

    @property
    def A(self) -> float:
        """
        Returns:
            cross-sectional area [m2]
        """
        return self._A

    @property
    def m_dot(self) -> float:
        """
        Returns:
            mass flow rate [kg/s]
        """
        return self._m_dot

    @m_dot.setter
    def m_dot(self, value: float) -> None:
        """
        Sets mass flow rate and updates volume flow rate and speed

        Args:
            value: 
                mass flow rate [kg/s]
        """
        self._m_dot = value
        self._V_dot = self.m_dot / self.fluid.rho(self.T(), self.p())
        self._v = self.V_dot / self.A

    @property
    def V_dot(self) -> float:
        """
        Returns:
            volume flow rate [m3/s]
        """
        return self._V_dot

    @V_dot.setter
    def V_dot(self, value: float) -> None:
        """
        Sets volume flow rate and updates mass flow rate and speed

        Args:
            value: 
                volume flow rate [m3/s]
        """
        self._V_dot = value
        self._m_dot = self.V_dot * self.fluid.rho(self.T(), self.p())
        self._v = self.V_dot / self._A

    @property
    def Re(self) -> float:
        """
        Returns:
            Reynolds number
        """
        if self.d_pipe is not None:
            d_eqivalent = self.d_pipe
        else:
            a, b = self.w_h_pipe
            d_eqivalent = 2 * a * b / (a + b)
        return d_eqivalent * self.v / self.fluid.nu(self.T(), self.p())

    @property
    def is_laminar(self):
        """
        Returns:
            True if flow is laminar
        """
        return self.Re <= 2100.

    @property
    def is_transition(self) -> bool:
        """
        Returns:
            True if flow is in transition from laminar to turbulent
        """
        return not self.is_laminar() and not self.is_turbulent()

    @property
    def is_turbulent(self) -> bool:
        """
        Returns:
            True if flow is turbulent
        """
        return self.Re >= 4000.

    @property
    def is_ultra_sonic(self) -> float:
        """
        Returns:
            True if flow is ultra sonic (v > v_sound)
        """
        return self.v() < self.fluid.c_sound(self.T(), self.p())
    
    def __str__(self):
        s = self._fluid.identifier                        + '\n' + \
            '             A: ' + str(self.A)              + '\n' + \
            '        d_pipe: ' + str(self._d_pipe)        + '\n' + \
            '    is_laminar: ' + str(self.is_laminar)     + '\n' + \
            '  is_turbulent: ' + str(self.is_turbulent)   + '\n' + \
            'is_ultra_sonic: ' + str(self.is_ultra_sonic) + '\n' + \
            '         m_dot: ' + str(self._m_dot)         + '\n' + \
            '             p: ' + str(self.p.val)          + '\n' + \
            '            Re: ' + str(self.Re)             + '\n' + \
            '             T: ' + str(self.T.val)          + '\n' + \
            '         V_dot: ' + str(self._V_dot)         + '\n' + \
            '             v: ' + str(self._v)             + '\n' + \
            '      w_h_pipe: ' + str(self._w_h_pipe)
        return s
