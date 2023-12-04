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
      2018-09-16 DWW
"""

from datetime import datetime
import time
from typing import Optional


def date_to_seconds(date: str, 
                    date_ref: Optional[str]=None, 
                    date_format: Optional[str]=None) -> int:
    """
    Converts one or two date strings into time difference in seconds
    
    Args:
        date
            date string
            
        date_ref
            reference date string

        date_format
            format of date employing %Y, %m, %d, %H, %M and %S,
            usually '%Y-%m-%dT%H:%M:%S' or '%Y-%m-%dT%H.%M.%S'
            
    Returns:
        if date_ref is None: 
            returns time difference between date and 1.1.1970 in seconds
        else: 
            returns time difference between date and date_ref in seconds
    """
    if date_format is None:
        if ':' in date and '.' not in date:
            date_format = '%Y-%m-%dT%H:%M:%S'
        else:
            date_format = '%Y-%m-%dT%H.%M.%S'

    t = datetime.strptime(date, date_format)
    t = time.mktime(t.timetuple())

    if not date_ref:
        return t

    t_ref = datetime.strptime(date_ref, date_format)
    t_ref = time.mktime(t_ref.timetuple())

    return t - t_ref
