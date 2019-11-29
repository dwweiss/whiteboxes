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
      2019-11-28 DWW
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Tuple, Union

from coloredlids.property.parameter import Floats
from coloredlids.property.conversion import C2K
from coloredlids.property.parameter import Parameter, Range


class Property(Parameter):
    """
    Adds temperature and pressure Parameter to a Parameter and provides
    call of Property value as function of temperature, pressure and
    spare parameter 'x'
    
    
    Parameter
        ^
        |
    Property  <== Aggregation ==  T: Parameter, 
                                  p: Parameter, 
                                  x: Parameter

    Note:
      - calc(T, p, x) is the implementation of the dependency of a 
        property o temperature T, pressure p or spare parameter x

      - Function self.__call__() must NOT be overwritten
    """

    def __init__(self, 
                 identifier: str = 'Property',
                 unit: str = '/',
                 absolute: bool = True,
                 latex: Optional[str] = None,
                 val: Floats = None,
                 ref: Floats = None,
                 comment: Optional[str] = None) -> None:
        
        super().__init__(identifier=identifier, unit=unit, absolute=absolute,
                         latex=latex, val=val, ref=ref, comment=comment)
        
        # reference temperature gases: 15C, solids: 20C or 25C
        T_Celsius = 15.
        
        self.T = Parameter(identifier='T', unit='K', absolute=True)
        self.T['operational'] = Range(C2K(-40.), C2K(200.))
        self.T.ref = C2K(T_Celsius)
        self.T.accuracy = Range('-1', '+1')

        self.p = Parameter(identifier='p', unit='Pa', absolute=True)
        self.p.ref = 1.01325e5
        self.p['operational'] = Range(0. + self.p.ref, 100e5 + self.p.ref)
        self.p.accuracy = Range('-1%FS', '+1%FS')

        self.x: Optional[Parameter] = None

        self.accuracy = Range('-1%', '1%')
        self.repeatability = Range('-0.1', '+0.1', '95%')

    def plot(self, title: str = '') -> None:
        if isinstance(self.T, Parameter):
            if self.T['operational'].lo != self.T['operational'].up:
                plt.title(title)
                plt.xlabel(self.T.latex + ' ' + self.T.unit)
                plt.ylabel(self.latex + ' ' + self.unit)
                T = np.linspace(self.T['operational'].lo, 
                                self.T['operational'].up)
                plt.plot(T, [self.__call__(_T, self.p.ref, 0.) for _T in T])
                plt.grid()
                plt.show()
        if isinstance(self.p, Parameter):
            if self.p['operational'].lo != self.p['operational'].up:
                plt.title(title)
                plt.xlabel(self.p.latex + ' ' + self.p.unit)
                plt.ylabel(self.latex + ' ' + self.unit)
                p = np.linspace(self.p['operational'].lo, 
                                self.p['operational'].up)
                plt.plot(p, [self.__call__(self.T.ref, _p, 0.) for _p in p])
                plt.grid()
                plt.show()
        if isinstance(self.x, Parameter):
            if self.x['operational'].lo != self.x['operational'].up:
                plt.title(title)
                plt.xlabel(self.x.latex + ' ' + self.x.unit)
                plt.ylabel(self.latex + ' ' + self.unit)
                x = np.linspace(self.x['operational'].lo, 
                                self.x['operational'].up)
                plt.plot(x, [self.__call__(self.T.ref, self.p.ref, _x)
                             for _x in x])
                plt.grid()
                plt.show()

    def calc(self, T: Floats = 0., p: Floats = 0., x: Floats = 0.) -> Floats:
        """
        This function SHOULD be overwritten in derived classes.
        It returns the actual value(s) as a placeholder 

        Args:
            T:
                Temperature as scalar or as 1D array
            p:
                Pressure as scalar or as 1D array
            x:
                Spare variable as scalar or as 1D array

        Returns:
            Approximation of value as function of T, p and x
            if T, p and x are scalars, the method returns a scaler.
            Otherwise a 1D array will be returned

        Example:
            class X():
                def __init__(self):
                    self.abc = Property('abc', 'kg/m3')
                    self.abc.calc = lambda T, p, x=0: 2 + 3*T - 2*p
        """
        return self.val

    def __call__(self, T: Floats = 0., p: Floats = 0., 
                 x: Floats = 0.) -> Floats:
        """
        This function MUST NOT be overwritten

        Args:
            T:
                Temperature as float or as 1D array.
                If None, the value of T.ref will be used
            p:
                Pressure as float or as 1D array
                If None, the value of p.ref will be used
            x:
                Spare variable as float or as 1D array
                If None, the value of x.ref will be used

        Returns:
            Approximation of value as function of T, p and x
            if T, p and x are scalars, then method returns a scalar.
            Otherwise a 1D array will be returned
        """
        if T is None:
            T = self.T.ref
        if p is None:
            p = self.p.ref
        if x is None and self.x is not None:
            x = self.x.ref
        return self.calc(T, p, x)
    
    def simulate(self, range_key: Optional[str] = None, 
                 size: Optional[Union[int, Tuple[int]]] = None, 
                 plot: bool = False) -> bool:   
        if range_key is None:
            range_key = 'calibrated'
        if range_key not in self.ranges:
            return False

        if plot:
            s = r"poperty('" + self.identifier + "')"
            print('\n+++ Simulate', s + ':')
        self.val = super().simulate(range_key=range_key, size=size, 
                                    plot=plot)
        
        if self.T is not None:
            if plot:
                print('\n+++ Simulate', s + '.T:')
            self.T.val = self.T.simulate(range_key=range_key, size=size, 
                                         plot=plot)
        if self.p is not None:
            if plot:
                print('\n+++ Simulate', s + '.p:')
            self.p.val = self.p.simulate(range_key=range_key, size=size, 
                                         plot=plot)
        if self.x is not None:
            if plot:
                print('\n+++ Simulate', s + '.x:')
            self.x.val = self.x.simulate(range_key=range_key, size=size, 
                                         plot=plot)
        
        return (self.val is not None 
                and (self.T is None or self.T.val is not None)  
                and (self.p is None or self.p.val is not None)
                and (self.x is None or self.x.val is not None))
