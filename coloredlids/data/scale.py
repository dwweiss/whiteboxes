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
      2019-09-17 DWW
"""

__all__ = ['scale', 'batch_normalize', 'batch_denormalize'] 

from typing import Optional
import numpy as np

           
def scale(X: np.ndarray, lo: float=0., hi: float=1., 
          axis: Optional[int]=None) -> np.ndarray:
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
            if not None, minimum and maximum are taken from axis given by 
            axis index (for 2D array: column=0, row=1)

    Returns:
        (array of float):
            normalized array
    """
    np.asarray(X)
    _max = np.max(X, axis=axis)
    delta = _max - np.min(X, axis=axis)
    assert not np.isclose(delta, 0), str(delta)

    return hi - (((hi - lo) * (_max - X)) / delta)


def batch_normalize(X, eps=0):
    """
    Normalizes elements of array, shifted by mean of X and scaled by variance

    Args:
        X (array_like of float):
            array to be normalised

        eps (float, optional):
            add-on to variance, usually in the order of a percent of variance

    Returns:
        (dict of {array of float, float, float, float}):
            (val, mean, var, eps) of normalized array

    Note:
        variance: var = mean( (x - mean(x))**2 )
    """
    X = np.asfarray(X)
    mean = np.mean(X)
    var = np.var(X)
    if np.abs(var + eps) > 1e-20:
        X = (X - mean) / np.sqrt(var + eps)

    return {'val': X, 'mean': mean, 'var': var, 'eps': eps}


def batch_denormalize(X, mean=0, var=1, eps=0):
    """
    Denormalizes elements of array, shifted by mean of X and scaled by variance

    Args:
        X (array_like of float or dict of {array_like of float, float, float}):
            array to be denormalised or dict with members: 'val', 'mean', 'var'

        mean (float, optional):
            mean value of input X

        var (float, optional):
            variance of input X

        eps (float, optional):
            add-on to variance, usually in the order of a percent of variance

    Returns:
        (array of float):
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
