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
      2018-01-11 DWW
"""


def ensurePair(x, y=None, sameType=False):
    """
    Ensures that x and y form a pair (tuple)

    Args:
        x (any type):
            first parameter

        y (any type, optional):
            second type

        sameType (bool, optional):

    Returns:
        (tuple):
            pair of x and y
    """
    if y is None:
        y = x

    if sameType:
        type_x = type(x)
        y = type_x(y)

    return (x, y)


# Examples ####################################################################

if __name__ == '__main__':
    import numpy as np

    ALL = 1

    if 0 or ALL:
        print(ensurePair(np.array([2, 3, 5])))
        print(ensurePair('abc'))
        print(ensurePair('abc', 'def'))
        print(ensurePair(1, 'a'))
        print(ensurePair(1.1, 2))
        print(ensurePair(1.1, 2, sameType=True))
        print('------')
