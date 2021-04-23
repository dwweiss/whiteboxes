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
      2020-12-22 DWW
"""

__all__ = ['deg2rad', 'rad2deg', 
           'Pa2bar', 'bar2Pa', 'ksi2Pa', 'msi2Pa', 'air_pressure', 'atm', 
           'C2K', 'K2C', 'F2C', 'C2F', 'F2K', 'K2F', 'is_probably_celsius',
           'cal2J', 'cal_g2J_kg',]
           
import numpy as np
from typing import Iterable, Union


def deg2rad(deg: Union[float, Iterable[float]]) -> Union[float, np.ndarray]:
    """
    Converts angles from degrees to radians
    """
    return np.radians(deg)


def rad2deg(rad: Union[float, Iterable[float]]) -> Union[float, np.ndarray]:
    """
    Converts angles from degrees to radians
    """
    return np.degrees(rad)


def C2K(C: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts temperature from Celsius to Kelvin
    """
    return np.asanyarray(C) + 273.15


def K2C(K: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts temperature from Kelvin to Celsius
    """
    return np.asanyarray(K) - 273.15


def F2C(F: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts temperature from Fahrenheit to Celsius
    """
    return (np.asanyarray(F) - 32.) / 1.8


def C2F(C: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts temperature from Celsius to Fahrenheit
    """
    return 1.8 * np.asanyarray(C) + 32.


def F2K(F: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts temperature from Fahrenheit to Kelvin
    """
    return C2K(F2C(np.asanyarray(F)))


def K2F(K: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts temperature from Kelvin to Fahrenheit
    """
    return C2F(K2C(np.asanyarray(K)))


def Pa2bar(Pa: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts pressure from [Pascal] to [bar]
    """
    return np.asanyarray(Pa) * 1e-5


def bar2Pa(bar: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts pressure from [bar] to [Pascal]
    """
    return np.asanyarray(bar) * 1e5


def ksi2Pa(ksi: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts pressure from [ksi] (pounds per square inch) to [Pascal]
    """
    return np.asanyarray(ksi) * 6.894745e+6


def msi2Pa(msi: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts pressure from [msi] (megapounds per square inch) to [Pascal]
    """
    return np.asanyarray(msi) * 6.894745e+9

def atm() -> float:
    """
    Returns:
        standard atmosphere pressure [Pa]
    """
    return 101325.

def air_pressure(altitude: float = 0.) -> float:
    """
    Calculate air pressure above sea level at given altitude 
    
    Args:
        altitude [m]
        
    Returns:
        air pressure [Pa]
    """
    return 101325 * (1. - 2.25577e-5 * altitude)**5.25588

def cal2J(cal: float) -> float:
    """
    Converts heat from [cal] to [J]
    """
    return cal * 4186.8


def cal_g2J_kg(cal_per_g: float) -> float:
    """
    Converts specific heat from [cal/g] to [J/kg]
    """
    return cal_per_g * 4186.8


def is_probably_celsius(T: Union[float, Iterable[float]], 
                        low: float = 200.) -> bool:
    """ 
    Checks temperature unit based on the assumption that a temperature
    less than 'low' has probably the unit 'degrees Celsius' 
    
    Args:
        T:
            temperature, unit is unknown
            
        low: 
            lower bound of assumed Celsius temperature range
            
    Returns:
        False if T is less than lower bound 'low'
    """
    return np.less(T, low)
