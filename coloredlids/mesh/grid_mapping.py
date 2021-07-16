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
      2021-07-01 DWW
"""

__all__ = ['irregular_grid_mapping']


import numpy as np
from scipy.interpolate import (CloughTocher2DInterpolator, 
                               LinearNDInterpolator, NearestNDInterpolator)
from scipy.spatial import Delaunay
from typing import Optional


def irregular_grid_mapping(
        X: np.ndarray, Y: np.ndarray, Z: Optional[np.ndarray], 
        U: np.ndarray, 
        x: np.ndarray, y: np.ndarray, z: Optional[np.ndarray],
        method: str = 'linear',
        ) -> Optional[np.ndarray]:    
    """
    Maps data on irregular source grid to irregular target grid in 2D 
    or 3D space: 
        U(X,Y,Z) -> u(x,y,z) if Z is not None  
        U(X,Y)   -> u(x,y)   if Z is None 
        
    Args:
        X (1D array of float):
            first independent variable on source grid
        Y (1D array of float):
            second independent variable on source grid
        Z (1D array of float):
            third independent variable on source grid
            OR 
            None if grid in 2D space

        U (1D array of float):
            dependent variable on source grid

        x (1D array of float):
            first independent variable on target grid
        y (1D array of float):
            second independent variable on target grid
        z (1D array of float):
            third independent variable on target grid
            OR 
            None if grid in 2D space
            
        method:
            identifier of interpolation method, starts with:
                'l': linear
                'n': nearest neighbor
                'c': CloughTocher algorithm, only if Z is None
            argument is not case sensitive

    Returns:
        u (1D array of float):
            dependent variable u(x,y,z) or u(x,y) on target grid
            OR
            None if mapping fails
        
    """
    return irregular_grid_mapping_single_unknown(X, Y, Z, U, x, y, z, method)    

    
    
def irregular_grid_mapping_single_unknown(
        X: np.ndarray, Y: np.ndarray, Z: Optional[np.ndarray], 
        U: np.ndarray, 
        x: np.ndarray, y: np.ndarray, z: Optional[np.ndarray],
        method: str = 'linear',
        ) -> Optional[np.ndarray]:    
    """
    Maps data on irregular source grid to irregular target grid in 2D 
    or 3D space: 
        U(X,Y,Z) -> u(x,y,z) if Z is not None  
        U(X,Y)   -> u(x,y)   if Z is None 
        
    Args:
        X (1D array of float):
            first independent variable on source grid
        Y (1D array of float):
            second independent variable on source grid
        Z (1D array of float):
            third independent variable on source grid
            OR 
            None if grid in 2D space

        U (1D array of float):
            dependent variable on source grid

        x (1D array of float):
            first independent variable on target grid
        y (1D array of float):
            second independent variable on target grid
        z (1D array of float):
            third independent variable on target grid
            OR 
            None if grid in 2D space
            
        method:
            identifier of interpolation method, starts with:
                'l': linear
                'n': nearest neighbor
                'c': CloughTocher algorithm, only if Z is None
            argument is not case sensitive

    Returns:
        u (1D array of float):
            dependent variable u(x,y,z) or u(x,y) on target grid
            OR
            None if mapping fails
        
    """
    X, Y, U = np.asarray(X), np.asarray(Y), np.asarray(U)
    Z = np.asarray(Z) if Z is not None else None
    x, y = np.asarray(x), np.asarray(y)
    z = np.asarray(z) if z is not None else None
    assert X.shape == Y.shape == U.shape and (Z is None or X.shape == Z.shape)
    assert x.shape == y.shape and (z is None or x.shape == z.shape)
    
    if Z is None:    
        triang = Delaunay(np.array((X, Y)).T)
    else:
        triang = Delaunay(np.array((X, Y, Z)).T)
        
    if method.upper().startswith('n'):
        interpolator = NearestNDInterpolator(triang, U, fill_value=0.)
    elif Z is None and method.upper().startswith('c'):
        interpolator = CloughTocher2DInterpolator(triang, U, fill_value=0.)
    else:
        interpolator = LinearNDInterpolator(triang, U, fill_value=0.)
        
    if Z is None:
        try:
            u = interpolator(np.array((x, y)).T)
        except:
            return None
    else:
        try:
            u = interpolator(np.array((x, y, z)).T)
        except:
            return None

    return u
