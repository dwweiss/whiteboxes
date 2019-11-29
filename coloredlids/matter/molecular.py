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
      2019-09-18 DWW
"""

from typing import Optional


def molecular_weight(identifier: str) -> Optional[float]:
    """
    Args:
        identifier:
            identifier of chemical element or organic compound

    Returns:
        Molecular weight (molar mass) in [kg/mol]
        or None if identifier is invalid

    Reference:
        https://www.lenntech.com/calculators/molecular/
            molecular-weight-calculator.htm
    """
    if not str or not isinstance(identifier, str):
        return None

    first = identifier[0].upper()
    if first == 'A':
        if   identifier == 'Ar':     return 39.95e-3
    elif first == 'C':
        if   identifier == 'C':      return 12.01e-3
        elif identifier == 'CO2':    return 44.01e-3
        elif identifier == 'CH4':    return 16.04e-3
        elif identifier == 'C2H4':   return 28.05e-3
        elif identifier == 'C2H5OH': return 12.01e-3
        elif identifier == 'C2H6':   return 30.07e-3
        elif identifier == 'C3H6':   return 42.07e-3
        elif identifier == 'C3H8':   return 44.01e-3
        elif identifier == 'C4H10':  return 58.12e-3
    elif first == 'H':
        if   identifier =='H':       return 1.008e-3
        elif identifier =='He':      return 4.003e-3
        elif identifier =='H2O':     return 18.02e-3
        elif identifier =='H2S':     return 34.08e-3
    elif first == 'N':
        if identifier =='N2':        return 28.01e-3
    elif first == 'O':
        if   identifier =='O':       return 16.00e-3
        elif identifier =='O2':      return 32.00e-3
    else:
        return None
