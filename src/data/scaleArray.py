"""
  Copyright (c) 2016-17 by Dietmar W Weiss

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
      2017-11-16 DWW
"""


import numpy as np


def scaleList(X, lo=0., hi=1.):
    """
    Normalizes elements of list to [lo, hi] interval

    Args:
        X (list of float):
            list of data to be normalised
        lo (float):
            minimum of returned list
        hi (float):
            maximum of returned list

    Returns:
        normalized list
    """
    xmin = min(X)
    xmax = max(X)
    scale = (hi - lo) / (xmax - xmin)
    return [(x - xmin) * scale + lo for x in X]


def scaleArray(X, lo=0., hi=1., axis=None):
    """
    Normalizes elements of array to [lo, hi] interval

    Args:
        X (array of float):
            array of data to be normalised
        lo (float):
            minimum of returned array
        hi (float):
            maximum of returned array
        axis (string or int or None):
            if not None, max is taken from axis given by axis index

    Returns:
        normalized array
    """
    if axis == 'col':
        axis = 0
    if axis == 'row':
        axis = 1
    np.asarray(X)
    maxs = np.max(X, axis=axis)
    delta = maxs - np.min(X, axis=axis)
    assert np.abs(delta) > 1e-20
    return hi - (((hi - lo) * (maxs - X)) / delta)


# Examples ####################################################################

if __name__ == '__main__':

    l = [3, 5, -11, 100, -90]    
    a = np.array(l)

    ll = scaleList(l, lo=-1, hi=2)
    aa = scaleList(a)

    print('ll:', ll, 'l:', l)
    print('aa:', aa, 'a:', a)
