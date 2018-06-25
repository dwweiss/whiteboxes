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
      2018-06-25 DWW
"""


from collections import OrderedDict
from io import StringIO
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from inspect import getsourcelines

from grayboxes.base import Base
from coloredlids.numerics.norm import L2_norm, SSE


class Regression1D(Base):
    """
    Example for deriving a class from Base. The methods overloaded are:
        load()
        pre()
        task()
        post()

    The example approximates data from an observations employing
    scipy.optimize.curve_fit. The best function is selected from a pool of
    candidate functions.
    """
    def __init__(self, identifier='Regression1D'):
        super().__init__(identifier)
        self.version = '11.17_dww'

        self.functionPool = OrderedDict({
          'f2a': self.f2a,
          'f3a': self.f3a, 'f3b': self.f3b, 'f3c': self.f3c,
          'f3d': self.f3d, 'f3e': self.f3e,
          'f4a': self.f4a, 'f4l': self.f4l,
          'f5l': self.f5l})

        # ranges for data selection (no selection if default bounds)
        self.xRange = (0, 0)
        self.yRange = (0, 0)

        # key, norm and coefficients of best candidate from function pool
        self.best = {'key': None, 'L2_norm': float('inf'),
                     'coefficients': None}

        # input/target arrays extracted from self.data
        self.X, self.Y = None, None

    # pool of candidate functions
    def f2a(self, x, a, b, c, d, e, f, g):
        return                 c + d*x

    def f3a(self, x, a, b, c, d, e, f, g):
        return           b/x + c + d*x

    def f3b(self, x, a, b, c, d, e, f, g):
        return a/(x*x)       + c + d*x

    def f3c(self, x, a, b, c, d, e, f, g):
        return a/(x*x) + b/x     + d*x

    def f3d(self, x, a, b, c, d, e, f, g):
        return a/(x*x) + b/x + c

    def f3e(self, x, a, b, c, d, e, f, g):
        return a*(x*x) + b*x + c

    def f4l(self, x, a, b, c, d, e, f, g):
        return a * np.exp(-b * x) + c + d * x

    def f4a(self, x, a, b, c, d, e, f, g):
        return a/(x*x) + b/x + c + d*x

    def f5l(self, x, a, b, c, d, e, f, g):
        return a * np.exp(-b * x) + c + d * x + e * x*x

    def functionCall(self, key, x, C):
        return self.functionPool[key](x,
                                      C[0], C[1], C[2], C[3], C[4], C[5], C[6])

    def load(self):
        """
        Loads self.data

        Note:
            This method is called by method pre()
        """
        self.csvSeparator = ';'
        s = StringIO("""t;y1;y2;y3;y4
            1.00E-03; 20;      20;      20
            5.00E-03; 20;      20;      20
            9.95E-03; 20;      20;      20
            2.56E-02; 20;      20;      20
            5.07E-02; 20;      20;      20
            0.10073;  20;      20;      20
            0.20872;  20;      20;      20
            0.4062;   20;      20;      19.998
            0.87059;  19.999;  19.999;  19.978
            1.2624;   20.001;  20.001;  20.007
            2.4379;   20.339;  20.345;  20.722
            5.9644;   24.824;  24.847;  26.292
            8.1901;   28.469;  28.498;  30.196
            10.706;   32.925;  32.956;  34.544
            14.48;    39.417;  39.448;  40.403
            20.77;    48.458;  48.487;  48.503
            29.576;   57.873;  57.899;  57.295
            39.64;    65.564;  65.588;  64.715
            59.767;   75.087;  75.107;  74.043
            79.895;   80.128;  80.146;  79.002
            100.02;   82.809;  82.826;  81.641
            150.34;   85.208;  85.224;  84.001
            200;      85.7;    85.717;  84.486
            """)

        df = pd.read_csv(s, sep=self.csvSeparator, comment='#')
        df.rename(columns=df.iloc[0])
        df = df.apply(pd.to_numeric, errors='coerce')
        xlabel = df.keys()[0]
        ylabel = df.keys()[1]

        if self.xRange[0] != self.xRange[1]:
            df = df[[self.xRange[0] <= x and x <= self.xRange[1]
                    for x in df[xlabel]]]
        if self.yRange[0] != self.yRange[1]:
            df = df[[self.yRange[0] <= y and y <= self.yRange[1]
                    for y in df[ylabel]]]
        self.data = df.reset_index(drop=True)

    def pre(self):
        super().pre()

        self.write('+++ Data loaded')
        self.write(self.data)

        self.data.plot(x='t', y=['y1', 'y2', 'y3'])
        plt.show()

        self.best['key'] = None
        self.best['L2_norm'] = float('inf')
        self.best['coefficients'] = None

    def task(self):
        super().task()

        # X is data point index
        self.X = self.data.ix[:, 0]

        # Y is mean of y1..4
        self.Y = (self.data['y1'] + self.data['y2'] + self.data['y3']) / 3

        keys = list(self.functionPool.keys())
        # keys = ['f5l', 'f4l']

        plt.title('f = (' + str(keys)[1:-1] + ')')
        plt.xlabel(self.data.keys()[0])
        plt.ylabel(self.data.keys()[1][:1])  # first letter of key of first y
        plt.plot(self.X, self.Y, label='observation', linestyle='--')

        for key in keys:
            self.write("+++ key: '", key, "'", None)
            coeff, co = curve_fit(self.functionPool[key], self.X, self.Y)
            y = self.functionCall(key, x=self.X, C=coeff)

            L2 = L2_norm(y, self.Y)
            if self.best['L2_norm'] > L2:
                self.best['L2_norm'] = L2
                self.best['coefficients'] = coeff
                self.best['key'] = key

            coeff = [str(round(x, 3)) for x in coeff if x != 1.0]
            plt.plot(self.X, y, label='approximation ('+key[1:]+')')
            self.write(', L2: ', round(L2_norm(y, self.Y), 2), None)
            self.write(', SSE: ', round(SSE(y, self.Y), 1), None)
            self.write(', C: ', coeff)

        plt.legend(bbox_to_anchor=(1.1, 1.01), loc='upper left')
        plt.show()

    def post(self):
        super().post()

        C = [str(round(x, 3)) for x in self.best['coefficients'] if x != 1.0]
        key = self.best['key']
        self.write("\n+++ Best, key:'", key, ', C: ', C)
        f = getsourcelines(self.__dict__['functionPool'][key])[0]
        sourceCode = [' '.join(x.split()) for x in f]
        for line in sourceCode:
            self.write('    ', line)

        plt.title('Absolute error of best approximation')
        y = self.functionCall(self.best['key'], x=self.X,
                              C=self.best['coefficients'])
        plt.plot(self.X, y-self.Y, label=r"$\Delta y$ for best: " +
                 self.best['key'] + "'")
        plt.legend(bbox_to_anchor=(1.1, 1.01), loc='upper left')
        plt.show()


# Examples ####################################################################

if __name__ == '__main__':
    test = Regression1D()
    test()
