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


def startsWithIgnoreCase(string, substring):
    """
    Checks if 'string' starts with 'substring' ignoring case

    Args:
        string (string):
            full string

        substring (string):
            sub string

    Returns:
        (bool):
            True if 'string' starts with 'substring' ignoring case
    """
    return re.match(substring, string, re.I)


def clean(s):
    """
    Removes space, tab, end of line etc from string
    """
    return re.sub("[ \t\n\v\f\r]", "", s)


def reverse(s):
    """
    Reverses string
    """
    return s[::-1]


def ensureHexFormat(hexFormat="#06x"):
    """
    Sets format string for hex numbers according to specification of 'format()'
    Corrects format if leading '#' or tailing 'x' are missing.
    """
    s = str(hexFormat)
    if s.startswith("#") and len(s) > 1:
        s = s[1:]
    if s.endswith("x") and len(s) > 1:
        s = s[:-1]
    try:
        i = int(s, 16)
    except ValueError:
        i = 2+4
        hexFormat = "#06x"
        print("??? setHexFormat(): invalid hex format:'#" + s +
              "x', corrected to:'" + hexFormat + "'")
    if i < 2+1:
        hexFormat = "#03x"
        print("??? setHexFormat(): length of hex string:'" + str(i) +
              "', increased to:'" + hexFormat + "'")
    elif i > 2+16:
        hexFormat = "#018x"
        print("??? setHexFormat(): length of hex string:'" + str(i) +
              "', reduced to:'" + hexFormat + "'")
    if not hexFormat.startswith("#"):
        hexFormat = '#' + hexFormat
    if not hexFormat[1] == "0":
        hexFormat = "#0" + hexFormat[1:]
    if not hexFormat.endswith('x'):
        hexFormat += "x"
    return hexFormat


def scientificToStandard_if_greater_1(s):
    """
    Converts scientic notation of numbers greater one to standard format

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


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 0 or ALL:
        def f():
            s = 'abc dde'
            length        = len(s)                # ==> 7
            repetitions   = s.count('d')          # ==> 2
            if 'dde' in s:
                index     = s.index('dde')        # ==> 4
            split         = s.split('c')          # ==> ['ab', ' dde']
            rev           = s[::-1]               # ==> 'edd cba'
            replaced      = s.replace('d', 'x')   # ==> 'abc xxe'
            capitilised   = ' '.join([x.capitalize() for x in s.split()])
                                                  # ==> 'Abc Dde'
            for key in sorted(locals()):
                print('{:>15}: {}'.format(key, locals()[key]))
        f()

    if 0 or ALL:
        f = ensureHexFormat("#06x ")      # "06" is total string length
        x = 14
        s = format(x, f)                  # returns "0x000e"
        print('1 x:', x, ' f:', f, ' s:', s)

        f = ensureHexFormat("#11x")       # "06" is total string length
        x = -155
        s = format(x, f)                  # returns "0x000e"
        print('2 x:', x, ' f:', f, ' s:', s)
        print()

    if 0 or ALL:
        S = ['1e3', '-.1e2', '1.2.34e3', '1.2.34D3', '1e-20', '1e-3', '1e20']
        for s in S:
            print('3 s:', s, 'replaced:', scientificToStandard_if_greater_1(s))
        print()

    if 0 or ALL:
        s = 'abcdef'
        print('4 s:', s, ' reverse:', reverse(s))
        print()
