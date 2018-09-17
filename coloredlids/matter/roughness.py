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
      2018-09-17 DWW
"""

from collections import OrderedDict
from typing import Optional


roughness_list = OrderedDict({"al_new":           1.4e-6,
                              "brass_new":        1.4e-6,
                              "brass_used":        30e-6,
                              "cu_new":           1.4e-6,
                              "cu_used":           30e-6,
                              "st_seamless_new":   40e-6,
                              "st_seamless_rust": 150e-6,
                              "st_weld_galv":       8e-6,
                              })


def roughness(matter: Optional[str]=None) -> Optional[float]:
    """
    Args:
        matter:
            identifier of matter

    Returns:
        Ra roughness of the metal surface [m]

    Note:
        if matter is None or not contained in _roughnessList, then a
        list of available materials is printed
    """

    key = str(matter).lower()
    if key in roughness_list:
        return roughness_list[key]

    print("??? invalid matter: '" + str(matter) + "'\n    valid keys:'",
          list(roughness_list.keys()), "'\n")
    return None
