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
      2019-09-18 DWW
"""

from typing import Tuple
import numpy as np


def henon_map(a: float=1.4, b: float=0.3, x: float=0.1, y: float=0.3, 
              n: int=10000) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Computes the 3D function u = u(x, y, z) for a Henon map. It is a series of
    u(x, y) solutions and z can be interpreted as a time index.

    Args:
        a:
            tuning parameter of function
        b: 
            tuning parameter of function
        x: 
            initial value of first variable
        y: 
            initial value of second variable
        n:   
            maximum number of time steps

    Returns:
        X, Y (array of float): x- and y-coordinates (size equals 'n')
        Z    (array of float): array of time step indices (size equals 'n')
    """
    X, Y = np.zeros(n), np.zeros(n)
    Z = np.array(range(n))
    for z in Z:
        x, y = y + 1. - a * x * x, b * x
        X[z], Y[z] = x, y
    Z = (Z - min(Z)) / (max(Z) - min(Z))

    return X, Y, Z
