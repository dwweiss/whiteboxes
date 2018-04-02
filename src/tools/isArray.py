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


import collections
import numpy as np


def isArray(x):
    """
    Checks if argument x is of array_like type

    Args:
        x (any type):
            variable to be checked

    Returns:
        (bool):
            True if x is of array_like type (list, tuple, set, np.array)
    """
    return isinstance(x, (collections.Sequence, np.ndarray))


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 0 or ALL:
        l = [1., 2., 3.]
        a = np.array(l)
        t = tuple(l)
        b = np.asfarray(l)
        i = 2
        f = 3.3

        for x in [l, a, t, b, i, f]:
            print('x:', x, '-> isArray:', isArray(x))
