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
      2018-01-31 DWW
"""


def grayLevel(x, xMin=None, xMax=None, singleChar=False):
    """
    Args:
        x (int or float):
            dimensionless value if xMin and xMax is None. Otherwise, x is a
            value out of the range of [xMin, xMax]

        xMin (int or float or None, optional):
            minimum x

        xMax (int or float or None, optional):
            maximum x

        singleChar (bool, optional):
            Controls the length of the returned string. if True, a string of
            length round(x*len(gl)). Otherwise, the last character of this
            string is returned.

    Returns:
        (string):
            single character if singleChar is True. Otherwise, string from
            gl[0] to gl[i-1] with size (i-1). i equals round(x * len(gl))

    Note:
        The string length for x==0 is zero
    """
    if xMin is not None and xMax is not None:
        x = (x - xMin) / (xMax - xMin)
    gl = '.:-=+*#%@'
    i = int(min(max(0., x), 1.) * len(gl) + 0.5)
    if not singleChar:
        s = gl[:i]
    else:
        s = gl[i-1] if i > 0 else ''
    return s


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    import numpy as np

    if 0 or ALL:
        X = np.linspace(0, 9, 12)
        for x in X:
            print('x:', str(round(x, 1)),
                  " glc:'" + grayLevel(x, X.min(), X.max(), singleChar=True) +
                  "'  gl: '" + grayLevel(x, X.min(), X.max()) + "'")
