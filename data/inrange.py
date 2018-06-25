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
      2018-06-25 DWW
"""


def inRange(x0, x0Range, x1=None, x1Range=None,
            x2=None, x2Range=None, x3=None, x3Range=None,
            x4=None, x4Range=None, x5=None, x5Range=None,
            x6=None, x6Range=None, x7=None, x7Range=None,
            x8=None, x8Range=None, x9=None, x9Range=None,
            tolerance=1e-10):
    """
    Checks if all x_i is within lower and upper bound of x_i-range

    Args:
        x0 (float):
            x-value

        x1..x9 (float, optional):
            x-values

        x0Range (array_like of 2-tuple):
            upper and lower bounds of x_i-range. If the value of one
            or both bounds is None, the check against these values is skipped

        x1Range..x9Range (array_like of 2-tuple, optional):
            upper and lower bounds of x_i-range. If the value of one
            or both bounds is None, the check against these values is skipped

        tolerance (float, opional):
            geometric tolerance for range check

    Returns:
        (bool):
            True if x0Range[0]-tolerance <= x0 <= x0Range[1]+tolerance and
                    x1Range[0]-tolerance <= x1 <= x1Range[1]+tolerance and
                    ...
                    x9Range[0]-tolerance <= x9 <= x9Range[1]+tolerance
    """

    def _is_in(x, xRange, tolerance):
        """
        Checks if x is within upper and lower bound of xRange. If the lower
        and/or upper bound is None, the check against this bound is skipped

        Args:
            x (float or None):
                argument

            xRange (array_like of float or None):
                upper and lower bound of range

            tolerance (float):
                gemeotric tolerance for range check

        Returns:
            (bool):
                None if x or xRange is None
                True if (xRange[0] - tolerance) <= x <= (xRange[1] + tolerance)
        """
        if x is None or xRange is None:
            return None
        if xRange[1] is None:
            if xRange[0] is None:
                return True
            return (xRange[0] - tolerance) <= x
        if xRange[0] is None:
            if xRange[1] is None:
                return True
            return x <= (xRange[1] + tolerance)
        return (xRange[0] - tolerance) <= x and x <= (xRange[1] + tolerance)

    isInX0Range = _is_in(x0, x0Range, tolerance)
    isInX1Range = _is_in(x1, x1Range, tolerance)
    isInX2Range = _is_in(x2, x2Range, tolerance)
    isInX3Range = _is_in(x3, x3Range, tolerance)
    isInX4Range = _is_in(x4, x4Range, tolerance)
    isInX5Range = _is_in(x5, x5Range, tolerance)
    isInX6Range = _is_in(x6, x6Range, tolerance)
    isInX7Range = _is_in(x7, x7Range, tolerance)
    isInX8Range = _is_in(x8, x8Range, tolerance)
    isInX9Range = _is_in(x9, x9Range, tolerance)

    b = True
    if isInX0Range is not None:
        b = b and isInX0Range
    if isInX1Range is not None:
        b = b and isInX1Range
    if isInX2Range is not None:
        b = b and isInX2Range
    if isInX3Range is not None:
        b = b and isInX3Range
    if isInX4Range is not None:
        b = b and isInX4Range
    if isInX5Range is not None:
        b = b and isInX5Range
    if isInX6Range is not None:
        b = b and isInX6Range
    if isInX7Range is not None:
        b = b and isInX7Range
    if isInX8Range is not None:
        b = b and isInX8Range
    if isInX9Range is not None:
        b = b and isInX9Range

    return b


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 0 or ALL:
        print('inRange:', inRange(2, [3, 4]))
        print('inRange:', inRange(None, [1, 4]))
        print('inRange:', inRange(2, [1, 4]))
        print('inRange:', inRange(2, [3, 4], 3, (2, 9)))
        print('inRange:', inRange(2, [1, 4], 3, (None, 9), 3, (None, None)))
        print('inRange:', inRange(None, [1, 4], None, (None, 9), None, (7, 0)))
