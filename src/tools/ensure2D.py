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
      2017-12-18 DWW
"""

import numpy as np


def ensure2D(x, y=None):
    """
    Ensures that x is valid 2D array
    Ensures that y is valid 2D array if y is not None
    Checks compatibility of x to y if y is not None

    Args:
        x (1D or 2D array_like):
            array

        y (1D or 2D array_like, optional):
            array

    Returns:
        (2D array of float):
            corrected array x if y is None, otherwise corrected arrays x and y
    """
    x = np.asfarray(x)
    if x.ndim == 1:
        x = np.atleast_2d(x).T
    else:
        assert x.ndim == 2, 'x.shape: ' + str(x.shape)
    if y is None:
        return x

    y = np.asfarray(y)
    if y.ndim == 1:
        y = np.atleast_2d(y).T
    else:
        assert y.ndim == 2, 'y.shape: ' + str(y.shape)
    assert x.shape[0] == y.shape[0], \
        'x.shape: ' + str(x.shape) + ', y.shape: ' + str(y.shape)

    return x, y


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 0 or ALL:
        import pandas as pd

        print(ensure2D(np.array([5])))
        print(ensure2D(np.array([2, 3, 4, 5])))
        print(ensure2D(np.array([[2, 3, 4, 5]])))
        print(ensure2D(np.array([[2, 3, 4, 5]]).T))
        print('------')
        print(ensure2D(np.array([2, 3, 4, 5]).T, np.array([2, 3, 4, 5])))
        print('------')
        print(ensure2D(pd.core.series.Series([2, 3, 4, 5])))
        print(ensure2D(pd.core.series.Series([2, 3, 4, 5]).T))
        print('------')
        print(ensure2D(np.atleast_1d([2, 3, 4, 5])))
        print(ensure2D(np.atleast_2d([2, 3, 4, 5])))
        print(ensure2D(np.atleast_2d([[2, 3, 4, 5]])))
        print(ensure2D(np.atleast_1d([2, 3, 4, 5]).T))
        print(ensure2D(np.atleast_2d([2, 3, 4, 5]).T))
        print(ensure2D(np.atleast_2d([[2, 3, 4, 5]]).T))
