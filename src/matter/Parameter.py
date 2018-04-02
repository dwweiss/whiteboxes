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
      2018-02-26 DWW
"""

import types
import inspect
from collections import OrderedDict
import numpy as np


def deg2rad(deg):
    """
    Convert angles from degrees to radians
    """
    return np.radians(deg)


def rad2deg(rad):
    """
    Convert angles from degrees to radians
    """
    return np.degrees(rad)


def C2K(C):
    """
    Converts temperature from Celsius to Kelvin
    """
    return np.asanyarray(C) + 273.15


def K2C(K):
    """
    Converts temperature from Kelvin to Celsius
    """
    return np.asanyarray(K) - 273.15


def F2C(F):
    """
    Converts temperature from Fahrenheit to Celsius
    """
    return (np.asanyarray(F) - 32) / 1.8


def C2F(C):
    """
    Converts temperature from Celsius to Fahrenheit
    """
    return 1.8 * np.asanyarray(C) + 32


def F2K(F):
    """
    Converts temperature from Fahrenheit to Kelvin
    """
    return C2K(F2C(np.asanyarray(F)))


def K2F(K):
    """
    Converts temperature from Kelvin to Fahrenheit
    """
    return C2F(K2C(np.asanyarray(K)))


def Pa2bar(pa):
    """
    Converts pressure from [Pascal] to [bar]
    """
    return np.asanyarray(pa) * 1e-5


def ksi2Pa(ksi):
    """
    Converts pressure from [ksi] (pounds per square inch) to [Pascal]
    """
    return np.asanyarray(ksi) * 6.894745e+6


def msi2Pa(msi):
    """
    Converts pressure from [msi] (megapounds per square inch) to [Pascal]
    """
    return np.asanyarray(msi) * 6.894745e+9


class Parameter(object):
    """
    Defines a parameter with:
      - actual value,
      - reference value,
      - absolute/relative flag,
      - unit,
      - range (operational and certified values),
      - identifiers (raw string and and latex version),
      - accuracy (absolute, relative to reading '%', rel. to full scale '%FS'),
      - repeatability,
      - sampling rate,
      - rate-of-change (d(Parameter)/dt)

    Note:
      - val (float):     actual value of parameter with unit 'self.unit'
      - ref (float):     reference value of parameter with unit 'self.unit'
      - absolute (bool): if True, temperatures are in Kelvin and pressure
                         is not relative (not gauge pressure)
      - member function __call__() returns self.val
    """

    def __init__(self, identifier='Parameter', unit='/', absolute=True,
                 latex=None, val=None, ref=None, comment=None):
        self.comment = comment if comment is not None else ''
        self.identifier = str(identifier)
        self.unit = str(unit)
        if self.unit[0] != '[':
            self.unit = '[' + self.unit
        if self.unit[-1] != ']':
            self.unit = self.unit + ']'
        self.absolute = bool(absolute)

        self.val = val if val is not None else 0.
        self.ref = ref if ref is not None else self.val
        self._operational = [min(0., self.val), max(0., self.val)]
        self._certified = list(self._operational)

        # Latex symbol, e.g. '$\varrho$'
        if latex:
            self.latex = str(latex)
        else:
            self.latex = self.identifier
        if len(self.latex) > 0:
            if self.latex[0] != '$':
                self.latex = '$' + self.latex
            if self.latex[-1] != '$':
                self.latex = self.latex + '$'

        # accuracy and repeatablity can be:
        # 1) absolute (e.g. '1.2'),
        # 2) relative to reading (e.g. '1.2%') or
        # 3) relative to full scale (e.g. '1.2%FS')
        self._accuracy = ['-1%', '+1%']
        self._repeatability = ['-0.1%', '0.1%', '95%']
        self.sampling = 100.0           # [1/s]
        self.rateOfChange = 0.0         # [(self.unit)/s]

        self.trustScore = 10            # confidence (10: excellent, 0: poor)

    def __call__(self):
        return self.val

    @property
    def accuracy(self):
        return self._accuracy

    @accuracy.setter
    def accuracy(self, value):
        """
        Note:
            accuracy is stored as string
        """
        value = np.atleast_1d(value)
        if len(value) >= 1:
            x0 = str(value[0]).upper()
        else:
            x0 = '0'
        if len(value) >= 2:
            self._accuracy = [x0, str(value[1]).upper()]
        elif len(value) == 1:
            self._accuracy = ['-' + x0, x0]
        else:
            assert 0

    @property
    def repeatability(self):
        return self._repeatability

    @repeatability.setter
    def repeatability(self, value):
        """
        Note:
            repeatability is stored as string
        """
        value = np.atleast_1d(value)
        if len(value) >= 1:
            x0 = str(value[0]).upper()
        else:
            x0 = '0'
        if len(value) == 3:
            self._repeatability = value
            p = str(value[2])
            if p[-1] != '%':
                p += '%'
            if p[0] == '-':
                p = p[1:]
            self._repeatability = [x0, str(value[1]).upper(), p]
        elif len(value) == 2:
            self._repeatability = [x0, str(value[1]).upper(), '95%']
        elif len(value) == 1:
            self._repeatability = ['-' + x0, x0, '95%']
        else:
            assert 0

    @property
    def operational(self):
        return self._operational

    @operational.setter
    def operational(self, value):
        value = np.atleast_1d(value)
        if len(value) >= 1:
            x0 = float(value[0])
        else:
            x0 = 0.
        if len(value) >= 2:
            x1 = float(value[1])
            if x0 < x1:
                self._operational = [x0, x1]
            else:
                self._operational = [x1, x0]
        else:
            if 0. < x0:
                self._operational = [0., x0]
            else:
                self._operational = [x0, 0.]

    @property
    def certified(self):
        return self._certified

    @certified.setter
    def certified(self, value):
        value = np.atleast_1d(value)
        if len(value) >= 1:
            x0 = float(value[0])
        else:
            x0 = 0.
        if len(value) >= 2:
            x1 = float(value[1])
            if x0 < x1:
                self._certified = [x0, x1]
            else:
                self._certified = [x1, x0]
        else:
            if 0. < x0:
                self._certified = [0., x0]
            else:
                self._certified = [x0, 0.]

    def __str__(self):
        s = '\n{'
        d = OrderedDict(sorted(self.__dict__.items()))
        for key, val in d.items():
            s += "  '" + key + "': "
            if isinstance(val, str):
                s += "'" + str(val) + "'"
            elif isinstance(val, types.FunctionType):
                c = ''
                for x in inspect.getsourcelines(val)[0]:
                    c += str(x).strip()
                c = c[c.index('=')+2:]
                c = c.replace('\\', '')
                c = c.replace('+ ', '+').replace(' +', '+')
                c = c.replace('- ', '-').replace(' -', '-')
                c = c.replace('* ', '*').replace(' *', '*')
                c = c.replace('/ ', '/').replace(' /', '/')
                s += c
            else:
                s += str(val)
            s += ',\n '
        s += '}'
        return s


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 0

    if 1 or ALL:
        print('deg2rad(90):', deg2rad(90))
        print('rad2deg(pi*0.5):', rad2deg(np.pi*0.5))

    if 0 or ALL:
        foo = Parameter(identifier='rhoLiq', latex=r'$\varrho_{liq}$',
                        unit='kg/m3')
        print(foo)
        print('-' * 40)

        foo.val = 3.3
        print(foo)
        print('-' * 40)

        print('foo.val, foo(), foo.ref:', (foo.val, foo(), foo.ref))
        foo.accuracy = ['1%FS']
        foo.repeatability = ['-4ac', 11, 5]  # '-4ac' is technically wrong
        foo.certified = [0, 11]
        foo.operational = [-8.8]
        print(foo)
        print('-' * 40)
