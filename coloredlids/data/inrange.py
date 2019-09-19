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
      2018-10-15 DWW
"""

from typing import Optional, Tuple


def in_range(x0: float, x0_range: Tuple[float, float], 
             x1: Optional[float]=None, 
             x1_range: Optional[Tuple[float, float]]=None,
             x2: Optional[float]=None, 
             x2_range: Optional[Tuple[float, float]]=None, 
             x3: Optional[float]=None, 
             x3_range: Optional[Tuple[float, float]]=None,
             x4: Optional[float]=None, 
             x4_range: Optional[Tuple[float, float]]=None, 
             x5: Optional[float]=None, 
             x5_range: Optional[Tuple[float, float]]=None,
             x6: Optional[float]=None, 
             x6_range: Optional[Tuple[float, float]]=None, 
             x7: Optional[float]=None, 
             x7_range: Optional[Tuple[float, float]]=None,
             x8: Optional[float]=None, 
             x8_range: Optional[Tuple[float, float]]=None, 
             x9: Optional[float]=None, 
             x9_range: Optional[Tuple[float, float]]=None,
             tolerance: Optional[float]=None) -> Optional[bool]:
    """
    Checks if all x_i is within lower and upper bound of x_i-range

    Args:
        x0..x9:
            x-values. If the value is None, the check against ist lower 
            and upper bound is skipped 

        x0_range..x9_range:
            upper and lower bounds of x-_ranges. If one or both bounds 
            is None, the check against these bounds is skipped

        tolerance:
            geometric tolerance for x-range check

    Returns:
        True if x0_range[0]-tolerance <= x0 <= x0_range[1]+tolerance and
                x1_range[0]-tolerance <= x1 <= x1_range[1]+tolerance and
                ...
                x9_range[0]-tolerance <= x9 <= x9_range[1]+tolerance
    """
    
    if tolerance is None:
        tolerance = 1e-10

    def _is_in(x: Optional[float], 
               x_range: Optional[Tuple[float, float]], 
               tolerance: float) -> Optional[bool]:
        """
        Checks if x is within upper and lower bound of x_range. If the 
        lower and/or upper bound is None, the check against this bound 
        is skipped

        Args:
            x:
                argument

            x_range:
                upper and lower bound of range

            tolerance:
                geometric tolerance for range check

        Returns:
            None if x or x_range is None
            True if (x_range[0] - tolerance) <= x <= (x_range[1] + tolerance)
        """
        if x is None or x_range is None:
            return None
        if x_range[1] is None:
            if x_range[0] is None:
                return True
            return (x_range[0] - tolerance) <= x
        if x_range[0] is None:
            if x_range[1] is None:
                return True
            return x <= (x_range[1] + tolerance)
        return (x_range[0] - tolerance) <= x and x <= (x_range[1] + tolerance)

    arr = (_is_in(x0, x0_range, tolerance), 
           _is_in(x1, x1_range, tolerance),
           _is_in(x2, x2_range, tolerance),
           _is_in(x3, x3_range, tolerance),
           _is_in(x4, x4_range, tolerance),
           _is_in(x5, x5_range, tolerance),
           _is_in(x6, x6_range, tolerance),
           _is_in(x7, x7_range, tolerance),
           _is_in(x8, x8_range, tolerance),
           _is_in(x9, x9_range, tolerance))

    arr = [_ for _ in arr if _ is not None]
    if not len(arr):
        return None
    else:
        return all(arr)
