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
      2019-11-29 DWW
"""

__all__ = ['deg2rad', 'rad2deg', 'C2K', 'K2C', 'F2C', 'C2F', 'F2K', 'K2F',
           'Pa2bar', 'ksi2Pa', 'msi2Pa', 'is_probably_celsius']
           
import numpy as np
from typing import Sequence, Union


def deg2rad(deg: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts angles from degrees to radians
    """
    return np.radians(deg)


def rad2deg(rad: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts angles from degrees to radians
    """
    return np.degrees(rad)


def C2K(C: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts temperature from Celsius to Kelvin
    """
    return np.asanyarray(C) + 273.15


def K2C(K: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts temperature from Kelvin to Celsius
    """
    return np.asanyarray(K) - 273.15


def F2C(F: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts temperature from Fahrenheit to Celsius
    """
    return (np.asanyarray(F) - 32) / 1.8


def C2F(C: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts temperature from Celsius to Fahrenheit
    """
    return 1.8 * np.asanyarray(C) + 32


def F2K(F: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts temperature from Fahrenheit to Kelvin
    """
    return C2K(F2C(np.asanyarray(F)))


def K2F(K: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts temperature from Kelvin to Fahrenheit
    """
    return C2F(K2C(np.asanyarray(K)))


def Pa2bar(pa: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts pressure from [Pascal] to [bar]
    """
    return np.asanyarray(pa) * 1e-5


def ksi2Pa(ksi: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts pressure from [ksi] (pounds per square inch) to [Pascal]
    """
    return np.asanyarray(ksi) * 6.894745e+6


def msi2Pa(msi: Union[float, Sequence[float], np.ndarray]) -> np.ndarray:
    """
    Converts pressure from [msi] (megapounds per square inch) to [Pascal]
    """
    return np.asanyarray(msi) * 6.894745e+9


def is_probably_celsius(T: Union[float, Sequence[float], np.ndarray], 
                        lo: float = 200.) -> bool:
    """ 
    Checks the assumption that a temperature less than 'lo' has probably 
    the unit 'degrees Celsius' 
    
    Args:
        T:
            temperature, unit is unknown
            
        lo: 
            lower bound of assumed Celsius temperature range
            
    Returns:
        False if T is less lower bound 'lo'
    """
    return np.less(T, lo)
