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
      2018-09-13 DWW
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
from parameter import Parameter, C2K


class Property(Parameter):
    """
    Adds temperature and pressure Parameter to a Parameter and provides
    call of Property value as function of temperature, pressure and
    spare parameter 'x'

    Note:
      - calc(T, p, x) is the implementation of the dependency on
        temperature T, pressure p or spare parameter x

      - Function self.__call__() must NOT be overwritten
    """

    def __init__(self, identifier: str='Property',
                 unit: str='/',
                 absolute: bool=True,
                 latex: Optional[str]=None,
                 val: Optional[str]=None,
                 ref: Optional[float]=None,
                 comment: str=None) -> None:
        super().__init__(identifier=identifier, unit=unit, absolute=absolute,
                         latex=latex, val=val, ref=ref, comment=comment)

        self.T = Parameter(identifier='T', unit='K', absolute=True)
        self.T.operational = [C2K(T_C) for T_C in (-40, 200)]
        self.T.ref = C2K(15)
        self.T.accuracy = ['-1', '+1']

        self.p = Parameter(identifier='p', unit='Pa', absolute=True)
        self.p.ref = 101.325e3
        self.p.operational = [(p_rel + self.p.ref) for p_rel in (0, 100e5)]
        self.p.accuracy = ['-1%FS', '+1%FS']

        self.x = None

        self.accuracy = ['-1%', '1%']
        self.repeatability = ['-0.1', '+0.1', '95%']

    def plot(self, title: str='') -> None:
        if isinstance(self.T, Parameter):
            if self.T.operational[0] != self.T.operational[1]:
                plt.title(title)
                plt.xlabel(self.T.latex + ' ' + self.T.unit)
                plt.ylabel(self.latex + ' ' + self.unit)
                T = np.linspace(self.T.operational[0], self.T.operational[1])
                plt.plot(T, [self.__call__(_T, self.p.ref, 0) for _T in T])
                plt.grid()
                plt.show()
        if isinstance(self.p, Parameter):
            if self.p.operational[0] != self.p.operational[1]:
                plt.title(title)
                plt.xlabel(self.p.latex + ' ' + self.p.unit)
                plt.ylabel(self.latex + ' ' + self.unit)
                p = np.linspace(self.p.operational[0], self.p.operational[1])
                plt.plot(p, [self.__call__(self.T.ref, _p, 0) for _p in p])
                plt.grid()
                plt.show()
        if isinstance(self.x, Parameter):
            if self.x.operational[0] != self.x.operational[1]:
                plt.title(title)
                plt.xlabel(self.x.latex + ' ' + self.x.unit)
                plt.ylabel(self.latex + ' ' + self.unit)
                x = np.linspace(self.x.operational[0], self.x.operational[1])
                plt.plot(x, [self.__call__(self.T.ref, self.p.ref, _x)
                             for _x in x])
                plt.grid()
                plt.show()

    def calc(self, T: float=0.,
             p: float=0.,
             x: float=0.) -> float:
        """
        This function shall be overwritten in derived classes

        Example:
            class X():
                def __init__(self):
                    self.abc = Property('abc', 'kg/m3')
                    self.abc.calc = lambda T, p, x=0: 2 + 3 * T - 2 * p
        """
        return self.val

    def __call__(self, T: Optional[float]=None,
                 p: Optional[float]=None,
                 x: Optional[float]=None) -> float:
        """
        This function must NOT be overwritten
        """
        if T is None:
            T = self.T.ref
        if p is None:
            p = self.p.ref
        if x is None and self.x is not None:
            x = self.x.ref
        return self.calc(T, p, x)
