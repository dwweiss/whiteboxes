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
      2019-09-16 DWW
"""

import os
from math import pi
import sys

sys.path.append(os.path.abspath('../..'))

from coloredlids.matter.property import Parameter, Property, C2K
from coloredlids.matter.genericmatter import Fluid
from coloredlids.matter.liquids import Water


class FlowIncompressible(Property):
    """
    Properties of mass or volume flow in pipework
    """

    def __init__(self, identifier: str='Flow', d_pipe: float=15e-3, 
                 v: float=1.) -> None:
        """
        Args:
            identifier:
                Indentifier of flow
            d_pipe:
                Equivalent inner pipe diameter [m]
            v:
                Speed (mean velocity) [m/s]
        """
        super().__init__(identifier=identifier)

        self._fluid: Fluid = Water()

        self.T.val: float = C2K(20)
        self.p.val: float = self.p.ref

        self._m_dot: float = 0.
        self._V_dot: float = 0.
        self._d_pipe: float = d_pipe
        self._A: float = pi * 0.25 * self.d_pipe**2
        self._v: float = Parameter(identifier='v', unit='m/s', val=v)

    @property
    def fluid(self) -> Fluid:
        """
        Returns:
            (Fluid): fluid object
        """
        return self._fluid

    @fluid.setter
    def fluid(self, value: Fluid) -> None:
        """
        Sets fluid

        Args:
            value: fluid
        """
        del self._fluid
        self._fluid = value

    def h_dot(self) -> float:
        """
        Returns:
            enthalpy flow rate [W/kg]
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
        Sets speed and updates volume and mass flow rate

        Args:
            value: speed [m/s]
        """
        self._v = value
        self._V_dot = self._A * self._v
        self._m_dot = self._V_dot * self.fluid.rho(self.T(), self.p(), 0.)

    @property
    def d_pipe(self) -> float:
        """
        Returns:
            pipe diameter [m]
        """
        return self._d_pipe

    @d_pipe.setter
    def d_pipe(self, value: float) -> None:
        """
        Sets pipe diameter and updates area, volume and mass flow rate

        Args:
            value: pipe diameter [m]
        """
        self._d_pipe = value
        self._A = pi * 0.25 * self.d_pipe**2
        self._V_dot = self._A * self.v
        self._m_dot = self._V_dot * self.fluid.rho(self.T(), self.p(), 0.)

    @property
    def m_dot(self) -> float:
        """
        Returns:
            mass flow rate [kg/s]
        """
        return self._mDot

    @m_dot.setter
    def m_dot(self, value: float) -> None:
        """
        Sets mass flow rate and updates volume flow rate and speed

        Args:
            value: mass flow rate [kg/s]
        """
        self._m_dot = value
        self._V_dot = self.m_dot / self.fluid.rho(self.T(), self.p())
        self._v = self.V_dot / self._A

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
        Args:
            value: volume flow rate [m3/s]
        """
        self._V_dot = value
        self._m_dot = self.V_dot * self.fluid.rho(self.T(), self.p())
        self._v = self.V_dot / self._A

    def Re(self) -> float:
        return self.dPipe * self.v / self.fluid.nu(self.T(), self.p())

    def is_laminar(self):
        """
        Returns:
            True if flow is laminar
        """
        return self.Re() <= 2100.

    def is_transition(self) -> bool:
        """
        Returns:
            True if flow is in transition from laminar to turbulent
        """
        return not self.is_laminar() and not self.is_turbulent()

    def is_turbulent(self) -> bool:
        """
        Returns:
            (bool): True if flow is turbulent
        """
        return self.Re() >= 4000.

    def is_ultra_sonic(self) -> float:
        """
        Returns:
            True if flow is ultra sonic (v > v_sound)
        """
        return self.v() < self.fluid.c_sound(self.T(), self.p())
