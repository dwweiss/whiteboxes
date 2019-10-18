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
      2019-10-17 DWW
"""


def extract_timestamp(s: str,
                      timestamp_notation: str='yyyy-mm-ddThh.mm.ss') -> str:
    """
    Extracts a timestamp from a string (e.g. a filename)
    
    Args:
        s:
            string containing a time stamp
        
        timestamp_notation:
            notation of date/time stamp
            
    Returns:
        extracted time stamp
        OR
        empty string if argument 's' does not contain a time stamp 
    """                        
    len_s = len(s)
    len_stamp = len(timestamp_notation)
    T_offset = timestamp_notation.find('T')
    
    i_year = s.find('20')              # first two digits of yyyy (year)
    if i_year == -1 or i_year + len_stamp > len_s:
        return ''
    
    while i_year != -1 and i_year + len_stamp <= len_s:
        i_T = i_year + T_offset
        if s[i_T] == 'T' and s[i_T+3] == '.' and s[i_T+6] == '.':
            return s[i_year:i_year + len_stamp]
        i_year = s.find('20', i_year+1)
    
    return ''
