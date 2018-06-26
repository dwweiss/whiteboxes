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

from math import pi
from coloredlids.matter.property import Parameter, Property, C2K
from coloredlids.matter.water import Water


class FlowIncompressible(Property):
    """
    Properties of mass or volume flow in pipework
    """

    def __init__(self, identifier='Flow', dPipe=15e-3, v=1.):
        """
        Args:
            identifier (string, optional):
                indentifier of flow
            dPipe (float, optional):
                Equivalent inner pipe diameter [m]
            v (float, optional):
                Speed (mean velocity) [m/s]
        """
        super().__init__(identifier=identifier)

        self._fluid = Water()

        self.T.val = C2K(20)
        self.p.val = self.p.ref

        self._mDot = 0.
        self._VDot = 0.
        self._dPipe = dPipe
        self._A = pi * 0.25 * self.dPipe**2
        self._v = Parameter(identifier='v', unit='m/s', val=v)

    @property
    def fluid(self):
        """
        Returns:
            (Fluid): fluid object
        """
        return self._fluid

    @fluid.setter
    def fluid(self, value):
        """
        Sets fluid

        Args:
            value (Fluid): fluid
        """
        del self._fluid
        self._fluid = value

    def hDot(self):
        """
        Returns:
            (float): enthalpy flow rate [W/kg]
        """
        return self.T() * self.fluid.c_p(self.T()) * self.mDot

    @property
    def v(self):
        """
        Returns:
            (float): speed [m/s]
        """
        return self._v

    @v.setter
    def v(self, value):
        """
        Sets speed and updates volume and mass flow rate

        Args:
            value (float): speed [m/s]
        """
        self._v = value
        self._VDot = self._A * self._v
        self._mDot = self._VDot * self.fluid.rho(self.T(), self.p(), 0.)

    @property
    def dPipe(self):
        """
        Returns:
            (float): pipe diameter [m]
        """
        return self._dPipe

    @dPipe.setter
    def dPipe(self, value):
        """
        Sets pipe diameter and updates area, volume and mass flow rate

        Args:
            value (float): pipe diameter [m]
        """
        self._dPipe = value
        self._A = pi * 0.25 * self.dPipe**2
        self._VDot = self._A * self.v
        self._mDot = self._VDot * self.fluid.rho(self.T(), self.p(), 0.)

    @property
    def mDot(self):
        """
        Returns:
            (float): mass flow rate [kg/s]
        """
        return self._mDot

    @mDot.setter
    def mDot(self, value):
        """
        Sets mass flow rate and updates volume flow rate and speed

        Args:
            value (float): mass flow rate [kg/s]
        """
        self._mDot = value
        self._VDot = self.mDot / self.fluid.rho(self.T(), self.p())
        self._v = self.VDot / self._A

    @property
    def VDot(self):
        """
        Returns:
            (float): volume flow rate [m3/s]
        """
        return self._VDot

    @VDot.setter
    def VDot(self, value):
        """
        Args:
            value (float): volume flow rate [m3/s]
        """
        self._VDot = value
        self._mDot = self.VDot * self.fluid.rho(self.T(), self.p())
        self._v = self.VDot / self._A

    def Re(self):
        return self.dPipe * self.v / self.fluid.nu(self.T(), self.p())

    def laminar(self):
        """
        Returns:
            (bool): True if flow is laminar
        """
        return self.Re() <= 2100.

    def transition(self):
        """
        Returns:
            (bool): True if flow is in transition from laminar to turbulent
        """
        return not self.laminar() and not self.turbulent()

    def turbulent(self):
        """
        Returns:
            (bool): True if flow is turbulent
        """
        return self.Re() >= 4000.

    def ultraSonic(self):
        """
        Returns:
            (bool): True if flow is ultra sonic (v > v_sound)
        """
        return self.v() < self.fluid.c_sound(self.T(), self.p())


# Examples ####################################################################

if __name__ == '__main__':
    if 1:
        foo = FlowIncompressible()
        foo.T.val = C2K(50)
        foo.v = 2.0
        print(foo)
        print('foo.T:', foo.T())
