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
      2019-11-19 DWW
"""

__all__ = ['scale', 'batch_normalize', 'batch_denormalize'] 

import numpy as np
from nptyping import Array
from typing import Dict, Optional, Union

           
def scale(X: Array[float], 
          lo: float = 0., 
          hi: float = 1., 
          axis: Optional[int] = None) -> Array[float]:
    """
    Normalizes elements of array to [lo, hi] interval (linear)

    Args:
        X:
            array of data to be normalised

        lo:
            minimum of returned array

        hi:
            maximum of returned array

        axis:
            if not None, minimum and maximum are taken from axis given 
            by axis index (for 2D array: column=0, row=1)

    Returns:
        normalized 1D array
    """
    np.asarray(X)
    max_ = np.max(X, axis=axis)
    delta = max_ - np.min(X, axis=axis)
    assert not np.isclose(delta, 0), str(delta)

    return hi - (((hi - lo) * (max_ - X)) / delta)


def batch_normalize(X: Array[float], 
                    eps: float = 0) -> Dict[str, Array[float]]:
    """ 
    Normalizes elements of array, shifted by mean of X and scaled 
    by variance

    Args:
        X:
            array to be normalised

        eps:
            add-on to variance, usually around one percent of variance

    Returns:
        dictionary of: (val, mean, var, eps) of normalized array

    Note:
        variance: var = mean( (x - mean(x))**2 )
    """
    X = np.asfarray(X)
    mean = np.mean(X)
    var = np.var(X)
    if np.abs(var + eps) > 1e-20:
        X = (X - mean) / np.sqrt(var + eps)

    return {'val': X, 'mean': mean, 'var': var, 'eps': eps}


def batch_denormalize(X: Union[Array[float], Dict[str, Array[float]]], 
                      mean: float = 0., 
                      var: float = 0.1, 
                      eps: float = 0.) -> Array[float]:
    """
    Denormalizes elements of array, shifted by mean of X and scaled 
    by variance

    Args:
        X:
            array to be denormalised or dictionary with the 
            members: 'val', 'mean', 'var'

        mean:
            mean value of input X

        var:
            variance of input X

        eps:
            add-on to variance, usually around one percent of variance

    Returns:
        denormalized array

    Note:
        X is returned unchanged if mean==0 and var==1 and eps==0
    """
    if isinstance(X, dict):
        keys = ['val', 'mean', 'var', 'eps']
        assert all([key in X for key in keys])
        val, mean, var, eps = (X[key] for key in keys)
    else:
        val = np.asfarray(X)

    return val * np.sqrt(var + eps) + mean
