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


def array2str(x):
    """
    Converts array to string. Removes comma, newline and multiple space

    Args:
        x (array_like of any type):
            input array

    Returns:
        (string):
            compressed string representation of x
    """
    if not isinstance(x, (collections.Sequence, np.ndarray)):
        return str(x)

    s = np.array2string(np.asanyarray(x))
    return s.replace(chr(10), '').replace('  ', ' ')


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 0 or ALL:
        seq = [None,
               1e30,
               [1, 2, 3],
               [[1, 2], [3, 4]],
               np.array([[1, 2], [3, 4]]),
               np.atleast_2d([1, 2, 3]),
               np.atleast_3d([1, 2, 3]),
               [[4, True], ['ab', 'c']],
               [[4, True], [2, 3]],
               ]
    
        for x in seq:
            print('x:', x, 'str:', array2str(x))
