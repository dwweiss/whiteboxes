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

import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, Iterable, List, Optional, Tuple, Union

try:
    from conversion import atm, C2K
    from parameter import Parameter
    from range import Range
except:
    from coloredlids.property.conversion import atm, C2K
    from coloredlids.property.parameter import Parameter
    from coloredlids.property.range import Range


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
        property of temperature T, pressure p or spare parameter x

      - Function self.__call__() must NOT be overwritten
    """

    def __init__(self, 
                 identifier: str = 'Property',
                 unit: str = '/',
                 absolute: bool = True,
                 latex: Optional[str] = None,
                 val: Optional[Union[float, Iterable[float]]] = None,
                 ref: Optional[Union[float, Iterable[float]]] = None,
                 comment: Optional[str] = None,
                 calc: Optional[Callable[..., float]] = None) -> None:
        
        super().__init__(identifier=identifier, unit=unit, absolute=absolute,
                         latex=latex, val=val, ref=ref, comment=comment)
        
        # reference temperature gases: 15C, solids: 20C or 25C, liquids: 20C
        T_Celsius = 20.
        
        self.T = Parameter(identifier='T', unit='K', absolute=True)
        self.T.ref = C2K(T_Celsius)
        self.T['operational'] = Range(C2K(-40.), C2K(200.))
        self.T.accuracy = Range('-1', '+1')

        self.p = Parameter(identifier='p', unit='Pa', absolute=True)
        self.p.ref = atm()
        self.p['operational'] = Range(0. + self.p.ref, 100e5 + self.p.ref)
        self.p.accuracy = Range('-1%FS', '+1%FS')

        self.x = Parameter(identifier='x', unit='/', absolute=True)
        self.x['operational'] = Range(0., 1.)
        self.x.ref = 0.
        
        self.accuracy = Range('-1%', '1%')
        self.repeatability = Range('-0.1', '+0.1', '95%')
        
        if calc is None:
            calc = lambda T, p, x: 1.
        self.calc = calc

        self.regression_coefficients: Optional[Iterable[float]] = None

    def plot(self, title: str = '') -> None:
        if isinstance(self.T, Parameter):
            if self.T['operational'].lo != self.T['operational'].up:
                plt.title(f'{title} p={self.p.ref}, x={self.x.ref}')
                plt.xlabel(self.T.latex + ' ' + self.T.unit)
                plt.ylabel(self.latex + ' ' + self.unit)
                T = np.linspace(self.T['operational'].lo, 
                                self.T['operational'].up)
                plt.plot(T, [self.__call__(_T, self.p.ref, 
                                           self.x.ref) for _T in T])
                plt.grid()
                plt.show()
        if isinstance(self.p, Parameter):
            if self.p['operational'].lo != self.p['operational'].up:
                plt.title(f'{title} T={self.T.ref}, x={self.x.ref}')
                plt.xlabel(self.p.latex + ' ' + self.p.unit)
                plt.ylabel(self.latex + ' ' + self.unit)
                p = np.linspace(self.p['operational'].lo, 
                                self.p['operational'].up)
                plt.plot(p, [self.__call__(self.T.ref, _p, 
                                           self.x.ref) for _p in p])
                plt.grid()
                plt.show()
        if isinstance(self.x, Parameter):
            if self.x['operational'].lo != self.x['operational'].up:
                plt.title(f'{title} T={self.T.ref}, p={self.p.ref}')
                plt.xlabel(self.x.latex + ' ' + self.x.unit)
                plt.ylabel(self.latex + ' ' + self.unit)
                x = np.linspace(self.x['operational'].lo, 
                                self.x['operational'].up)
                plt.plot(x, [self.__call__(self.T.ref, 
                                           self.p.ref, _x) for _x in x])
                plt.grid()
                plt.show()

    def calc(self, 
             T: Optional[Union[float, Iterable[float]]] = 0., 
             p: Optional[Union[float, Iterable[float]]] = 0., 
             x: Optional[Union[float, Iterable[float]]] = 0.
    ) -> Optional[Union[float, Iterable[float]]]:
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

    def regression_fit(self, 
            T_range: Optional[Tuple[float, float]] = None,
            p_range: Optional[Tuple[float, float]] = None,
            x_range: Optional[Tuple[float, float]] = None,
            order: Union[int, str] = 1,
    ) -> List[float]:
        """
        Calculates regression coefficients:
            Order 1:
                y = c0 + c1 * T   for T in [T0, T1]
                
            Order 2:
                y = c0 + c1 * T + c2 * T^2   for T in [T0, T1]
            ...
            
        Args:
            T_range:
                temperature range
                If None, the range [T.ref, T.ref + dT] will be used
                
            p_range
                pressure range
                If None, the value of [p.ref, p.ref + dp] will be used
            
            x_range:
                spare variable
                If None, the value of [x.ref, x.ref + dx] will be used
                
            order:
                Order of approximation, 
                    linear    if 1 or string starting with 'lin',
                    quadratic if 2 or string starting with 'quad'
                    cubic     if 3 or string starting with 'cub'
                    ...
                
        Returns:
            regression coefficients, length of list is: order+1
            OR
            None if desired 'order' is invalid 
        """
        dT, dp, dx = 100., 1e5, 1.  # default span of ranges
        
        if T_range is None:
            T_range = [self.T.ref, self.T_ref + dT]
        if p_range is None:
            p_range = [self.p.ref, self.p.ref + dp]
        if x_range is None:
            if self.x is not None and self.x.ref is not None:
                x_range = [self.x.ref, self.x.ref + dx]
            else:
                x_range = [0., 1.]
        if isinstance(order, str):
            order = order.lower()
            if order.startswith('lin'):
                order = 1
            elif order.startswith('qua'):
                order = 2
            else:
                order = 1
        assert T_range[1] - T_range[0] > 1e-20, str(T_range)
        assert p_range[1] - p_range[0] > 1e-20, str(p_range)
        assert x_range[1] - x_range[0] > 1e-20, str(x_range)

        self.regression_coefficients = None
        if order == 1:
            y0 = self.calc(T_range[0], p_range[0], x_range[0])
            y1 = self.calc(T_range[1], p_range[0], x_range[0])  # !!! [0]
            c1 = (y1 - y0) / (T_range[1] - T_range[0])           
            c0 = y0 - c1 * T_range[0]
            self.regression_coefficients = [c0, c1]
        else:
            # TODO add regression for higher orders 
            assert order < 2, str(order)
        
        return self.regression_coefficients

    def regression_prediction(self, 
                              T: Optional[float] = None, 
                              p: Optional[float] = None,
                              x: Optional[float] = None) -> float:
        """
        Linear approximation:
            y = c0 + c1*T                     for T in [T0, T1]
            y = c0 + c1*T + c2*T^2            for T in [T0, T1]
            y = c0 + c1*T + c2*T^2 + c3*T^3   for T in [T0, T1]
            
        Args:
            T:
                Temperature
                If None, the value of T.ref will be used
 
        Returns:
            approximation of property
        """        
        assert self.regression_coefficients is not None, \
            'call self.regression_coeffients() before linear_approximation()'

        if T is None:
            T = self.T.ref
        if p is None:
            p = self.p.ref
        if x is None:
            x = self.x.ref
                        
        y = self.regression_coefficients[0]   
        
        if len(self.regression_coefficients) > 1:
            return y + self.regression_coefficients[1] * T
        if len(self.regression_coefficients) > 2:
            return y + self.regression_coefficients[2] * T*T
        if len(self.regression_coefficients) > 3:
            return y + self.regression_coefficients[3] * T*T*T

        return y

    def __call__(self, 
                 T: Optional[Union[float, Iterable[float]]] = None, 
                 p: Optional[Union[float, Iterable[float]]] = None, 
                 x: Optional[Union[float, Iterable[float]]] = None
    ) -> Optional[Union[float, Iterable[float]]]:
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
            s = f"property('{self.identifier}')"
            print(rf'\n+++ Simulate {s}:')
        self.val = Parameter.simulate(self, range_key=range_key, size=size, 
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


    def __str__(self):
        s = ''
        if self.identifier is not None:
            s += str(self.identifier)
        if self.val is not None:
            s += 'val: ' + str(self.val)
        if self.ref is not None:
            s += 'ref: ' + str(self.ref)
        if self.T is not None and self.T.val is not None:
            s += ', T: ' + str(self.T.val)
        if self.p is not None and self.p.val is not None:
            s += ', p: ' + str(self.p.val)
        if self.x is not None and self.x.val is not None:
            s += ', x: ' + str(self.x.val)
        return s
            