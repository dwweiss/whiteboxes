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

      2019-04-01 DWW
"""

import re


"""
    Collection of basic string manipulation functions

    Existing String methods:
        s = 'abc dde'
        length      = len(s)               # ==> 7
        repetitions = s.count('d')         # ==> 2
        index       = s.index('Dde')       # ==> 4
        split       = s.split('c')         # ==> ['ab', ' dde']
        reverse     = s[::-1]              # ==> 'edd cba'
        replaced    = s.replace('d', 'x')  # ==> 'abc xxe'
        capitilised = s.capitilize()       # ==> 'Abc Dde'
"""


def starts_with_ignore_case(string: str, substring: str) -> bool:
    """
    Checks if 'string' starts with 'substring' ignoring case

    Args:
        string:
            full string

        substring:
            sub string

    Returns:
        True if 'string' starts with 'substring' ignoring case
    """
    return re.match(substring, string, re.I)


def clean(s: str) -> str:
    """
    Removes space, tab, end of line etc from string

    Args:
        string:
            original string

    Returns:
        copy of original string exclusive removed characters 
    """
    return re.sub("[ \t\n\v\f\r]", "", s)


def reverse(s: str) -> str:
    """
    Reverses string

    Args:
        string:
            original string

    Returns:
        copy of original string reversed
    """
    return s[::-1]


def ensure_hex_format(hex_format: str="#06x") -> str:
    """
    Sets format string for hex numbers according to specification of 'format()'

    Args:
        hex_format:
            original string

    Returns:
        corrected hex_format
    """
    s = str(hex_format)
    if s.startswith("#") and len(s) > 1:
        s = s[1:]
    if s.endswith("x") and len(s) > 1:
        s = s[:-1]
    try:
        i = int(s, 16)
    except ValueError:
        i = 2+4
        hex_format = "#06x"
        print("??? sethex_format(): invalid hex format:'#" + s +
              "x', corrected to:'" + hex_format + "'")
    if i < 2+1:
        hex_format = "#03x"
        print("??? sethex_format(): length of hex string:'" + str(i) +
              "', increased to:'" + hex_format + "'")
    elif i > 2+16:
        hex_format = "#018x"
        print("??? sethex_format(): length of hex string:'" + str(i) +
              "', reduced to:'" + hex_format + "'")
    if not hex_format.startswith("#"):
        hex_format = '#' + hex_format
    if not hex_format[1] == "0":
        hex_format = "#0" + hex_format[1:]
    if not hex_format.endswith('x'):
        hex_format += "x"
    return hex_format


def scientific_to_standard_if_greater_1(s: str) -> str:
    """
    Converts scientic notation of numbers greater one to standard format

    Args:
        s:
            original string

    Returns:
        corrected string

    Note:
        for numbers less then one, the string '0' is returned
    """
    try:
        int(s)
    except:
        try:
            x = float(s)
            if int(x * 10) % 10 == 0:
                s = str(int(x))
            else:
                s = str(x)
        except:
            pass
    return s
