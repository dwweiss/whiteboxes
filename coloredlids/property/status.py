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
      2019-11-19 DWW
"""

from typing import Optional
from enum import Enum


class Status(Enum):
    """
    Defines status of data. 
    A symbol and a color is connected to a status name.
    """
    BLOCK    = ('#', 'black')       # data is blocked for processing
    FAIL     = ('-', 'red')         # failure
    OUT      = ('!', 'gray')        # out of range
    PLAN     = ('%', 'blue')        # planned for processing
    SKIP     = ('^', 'brown')       # skip further processing aka 'continue'
    SUCCESS  = ('+', 'green')       # data is within expected ranges
    TOLERATE = ('~', 'yellow')      # data is within tolerated ranges
    UNDEF    = ('?', 'lightgray')   # undefined

    def symbol(status: 'Status') -> str:
        """
        Gets symbol connected to status

        Args:
            status:
                status of data

        Returns:
            symbol indicating status
        """
        return status.value[0]

    def color(status: 'Status') -> str:
        """
        Gets color connected to status

        Args:
            status:
                status of data

        Returns:
            string with status color
        """
        return status.value[1]

    def name_(symbol: str) -> Optional['Status']:
        """
        Gets symbol from status name

        Args:
            symbol:
                symbol indicating status

        Returns:
            name of status. If symbol is unknown, 'None' is returned

        Note:
            Do not rename to 'name()'.  'name' is first element of attributes
        """
        for x in Status:
            if x.value[0] == symbol:
                return x.name
        return None
