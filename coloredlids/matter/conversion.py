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
      2022-04-06  DWW
"""

__all__ = ['arr',
           'nano', 'micro', 'milli', 'centi', 'deci', 
           'one',
           'deka', 'hecto', 'kilo', 'mega', 'giga',
           'deg2rad', 'rad2deg', 
           'Pa2bar', 'bar2Pa', 'ksi2Pa', 'msi2Pa', 'air_pressure', 'atm', 
           'C2K', 'K2C', 'F2C', 'C2F', 'F2K', 'K2F', 'is_probably_celsius',
           'min2s', 's2min', 'cal2J', 'cal_g2J_kg',]
           
import numpy as np
from typing import Iterable, Tuple


def arr(
    x1: float | int | bool | Iterable[float] | Iterable[int] | Iterable[bool],
    x2: float | int | bool | Iterable[float] | Iterable[int] | Iterable[bool] | None = None,
    x3: float | int | bool | Iterable[float] | Iterable[int] | Iterable[bool] | None = None,
    x4: float | int | bool | Iterable[float] | Iterable[int] | Iterable[bool] | None = None,
    x5: float | int | bool | Iterable[float] | Iterable[int] | Iterable[bool] | None = None
) -> Union[np.ndarray,
           Tuple[np.ndarray, np.ndarray], 
           Tuple[np.ndarray, np.ndarray, np.ndarray],
           Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
           Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]
]:
    """
    Converts scalars or arrays to numpy arrays of float 
    """
    x1 = np.asfarray(x1)
    if x2 is None: 
        return x1

    x2 = np.asfarray(x2)
    if x3 is None: 
        return x1, x2

    x3 = np.asfarray(x3)
    if x4 is None: 
        return x1, x2, x3

    x4 = np.asfarray(x4)
    if x5 is None: 
        return x1, x2, x3, x4

    x5 = np.asfarray(x5)
    return x1, x2, x3, x4, x5


def pico(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'pico' : multiply with 1e12
    eg: L_in_meter = 1. -> pico(L_in_meter) = 1e12
    """
    return np.asfarray(x) * 1e12

def nano(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'nano' : multiply with 1e9
    eg: L_in_meter = 1. -> nano(L_in_meter) = 1e9
    """
    return np.asfarray(x) * 1e9

def micro(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'micro' : multiply with 1e6
    eg: L_in_meter = 1. -> micro(L_in_meter) = 1e6
    """
    return np.asfarray(x) * 1e6

def milli(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'milli' : multiply with 1e3
    eg: L_in_meter = 1. -> milli(L_in_meter) = 1e3
    """
    return np.asfarray(x) * 1e3

def centi(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'centi' : multiply with 1e2
    eg: L_in_meter = 1. -> centi(L_in_meter) = 1e2
    """
    return np.asfarray(x) * 1e2

def deci(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'deci' : multiply with 1e1
    eg: L_in_meter = 1. -> deci(L_in_meter) = 1e1
    """
    return np.asfarray(x) * 1e1

def one(x: float | Iterable[float]) -> np.ndarray:
    """
    Does not convert x
    eg: L_in_meter = 1. -> one(L_in_meter) = 1e0
    """
    return np.asfarray(x) * 1e0

def deka(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'deka' : multiply with 1e-1
    eg: L_in_meter = 1. -> deka(L_in_meter) = 1e-1
    """
    return np.asfarray(x) * 1e-1

def hecto(x: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts to prefix 'hecto' : multiply with 1e-2
    eg: L_in_meter = 1. -> hecto(L_in_meter) = 1e-2
    """
    return np.asfyarray(x) * 1e-2

def kilo(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'kilo' : multiply with 1e-3
    eg: L_in_meter = 1. -> kilo(L_in_meter) = 1e-3
    """
    return np.asfarray(x) * 1e-3

def mega(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'mega' : multiply with 1e-6
    eg: L_in_meter = 1. -> mega(L_in_meter) = 1e-6
    """
    return np.asfarray(x) * 1e-6

def giga(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'giga' : multiply with 1e-9
    eg: L_in_meter = 1. -> giga(L_in_meter) = 1e-9
    """
    return np.asfarray(x) * 1e-9

def tera(x: float | Iterable[float]) -> np.ndarray:
    """
    Converts to prefix 'tera' : multiply with 1e-12
    eg: L_in_meter = 1. -> tera(L_in_meter) = 1e-12
    """
    return np.asfarray(x) * 1e-12


def deg2rad(deg: float | Iterable[float]) -> float | np.ndarray:
    """
    Converts angles from degrees to radians
    """
    return np.radians(deg)


def rad2deg(rad: float | Iterable[float]) -> float | np.ndarray:
    """
    Converts angles from degrees to radians
    """
    return np.degrees(rad)


def C2K(C: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts temperature from Celsius to Kelvin
    """
    return np.asfarray(C) + 273.15


def K2C(K: float | Iterable[float]) -> np.ndarray:
    """
    Converts temperature from Kelvin to Celsius
    """
    return np.asfarray(K) - 273.15


def F2C(F: float | Iterable[float]) -> np.ndarray:
    """
    Converts temperature from Fahrenheit to Celsius
    """
    return (np.asfarray(F) - 32.) / 1.8


def C2F(C: float | Iterable[float]) -> np.ndarray:
    """
    Converts temperature from Celsius to Fahrenheit
    """
    return 1.8 * np.asfarray(C) + 32.


def F2K(F: float | Iterable[float]) -> np.ndarray:
    """
    Converts temperature from Fahrenheit to Kelvin
    """
    return C2K(F2C(np.asanyarray(F)))


def ft2m(ft: float | Iterable[float]) -> np.ndarray:
    """
    Converts length from foot to meter
    """
    return np.asfarray(ft) * 0.3048


def m2ft(m: float | Iterable[float]) -> np.ndarray:
    """
    Converts length from meter to foot
    """
    return np.asfarray(m) / 0.3048


def K2F(K: float | Iterable[float]) -> np.ndarray:
    """
    Converts temperature from Kelvin to Fahrenheit
    """
    return C2F(K2C(np.asfarray(K)))


def Pa2bar(Pa: float | Iterable[float]) -> np.ndarray:
    """
    Converts pressure from [Pascal] to [bar]
    """
    return np.asfarray(Pa) * 1e-5


def bar2Pa(bar: Union[float, Iterable[float]]) -> np.ndarray:
    """
    Converts pressure from [bar] to [Pascal]
    """
    return np.asfarray(bar) * 1e5


def ksi2Pa(ksi: float | Iterable[float]) -> np.ndarray:
    """
    Converts pressure from [ksi] (pounds per square inch) to [Pascal]
    """
    return np.asfarray(ksi) * 6.894745e+6


def msi2Pa(msi: float | Iterable[float]) -> np.ndarray:
    """
    Converts pressure from [msi] (megapounds per square inch) to [Pascal]
    """
    return np.asfarray(msi) * 6.894745e+9


def atm() -> float:
    """
    Returns:
        standard atmosphere pressure [Pa]
    """
    return 101.325e3


def air_pressure(altitude: float = 0., T: float = C2K(20)) -> float:
    """
    Calculate air pressure above sea level at given altitude 
    
    Args:
        altitude:
            altitude above sea level[m]
        
        T:
            dummy paramter: temperature [K]
        
    Returns:
        air pressure [Pa]
    
    Literature:
        engineeringtoolbox.com/air-altitude-pressure-d_462.html
        
    Example:
        for h in [3200, ft2m(10500), ft2m(11000), ft2m(11500)]:
            print(f'{h=:.0f}m={m2ft(h):.0f}ft -> p={air_pressure(h):.0f} Pa')
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


def min2s(m: float) -> float:
    """
    Converts time in [min] to [s]
    """
    return m * 60.


def s2min(s: float) -> float:
    """
    Converts time in [s] to [min]
    """
    return s / 60.


def is_probably_celsius(T: float | Iterable[float], 
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
