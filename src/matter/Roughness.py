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
      2017-12-14 DWW
"""

from collections import OrderedDict


_roughnessList = OrderedDict({"al_new":           0.0014e-3,
                              "brass_new":        0.0014e-3,
                              "brass_used":       0.03e-3,
                              "cu_new":           0.0014e-3,
                              "cu_used":          0.03e-3,
                              "st_seamless_new":  0.04e-3,
                              "st_seamless_rust": 0.15e-3,
                              "st_weld_galv":     0.008e-3,
                              })


def roughness(metal=None):
    """
    Args:
        metal (string, optional):
            identifier of string

    Returns:
        (float):
            Ra roughness of the metal surface [m]

    Note:
        if material is None, empty string or not contained in 'roughnesses',
        a list of available materials is printed
    """

    key = str(metal).lower()
    if key in _roughnessList:
        R = _roughnessList[key]
    else:
        R = None
        print('??? invalid metal:', str(metal) + ', valid keys:',
              _roughnessList.keys(), '\n')
    return R


# Examples ####################################################################

if __name__ == '__main__':
    for m in _roughnessList.keys():
        print('metal:', m, 'R:', roughness(m))
    print()

    for m in [None, '???', 'AL_NEW']:
        print('metal:', m, 'R:', roughness(m), '\n')
    print()
