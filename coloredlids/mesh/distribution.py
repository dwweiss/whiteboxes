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

from enum import Enum
from numpy import log, clip, sqrt
from random import random


class Distribution(Enum):
    """
    Defines mesh density fro different distributions
    """
    LIN            = ( 1, 'lin')    #  ----------------
                                    #  |  |  |  |  |  |  --> x
                                    #  ----------------

    LOG_PLUS       = ( 2, 'log+')   #  ----------------
                                    #  |    |   |  | ||  --> x
                                    #  ----------------

    LOG_MINUS      = (-2, 'log-')   #  ----------------
                                    #  || |  |   |    |  --> x
                                    #  ----------------

    LOG_PLUS_MINUS = ( 4, 'log+-')  #  -------------------------------
                                    #  |    |   |  | ||| |  |   |    |  --> x
                                    #  -------------------------------

    LOG_MINUS_PLUS = (-4, 'log-+')  #  -------------------------------
                                    #  || |  |   |         |   |  | ||  --> x
                                    #  -------------------------------
    RANDOM         = ( 5, 'rand')
    USER           = ( 0, 'user')

    def value(distribution):
        """
        Gets value connected to Distribution

        Args:
            distribution (Distribution):
                Distribution

        Returns:
            (int):
                value indicating Distribution
        """
        return distribution.value[0]

    def identifier(distribution):
        """
        Gets identifier connected to Distribution

        Args:
            distribution (Distribution):
                Distribution

        Returns:
            (string):
                identifier string
        """
        return distribution.value[1]

    def Name(identifier):
        """
        Gets identifier of Distribution name

        Args:
            identifier (string):
                identifier indicating Distribution

        Returns:
            (Distribution):
                name of distribution. If identifier is unknown, 'None' is
                returned

        Note:
            Do not rename to 'name()'.  'name' is first element of attributes
        """
        for x in Distribution:
            if x.value[0] == identifier:
                return x.name
        return None

    def density(i, distribution, iBegin, iEnd, left_OVER_all=0.5):
        """
        Computes dimensionless mesh density function for partly regular meshes

        Args:
            i (int):
                cell index

            distribution (Distribution):
                Distribution of mesh density [/]

            iBegin (int):
                minimum cell index

            iEnd (int):
                maximum cell index
                                                 +------------+---------------+
            left_OVER_all (float):               |<--L_left-->:<---L_right--->|
                                                 +------------+---------------+
                ratio: L_left / (L_left + L_right)
                (only relevant for LOG_PLUS_MINUS and LOG_MINUS_PLUS)

        Returns:
            dimensionless mesh density
        """

        assert all([x is not None for x in (i, iBegin, iEnd)])
        assert iBegin <= i and i <= iEnd

        if distribution == Distribution.LIN:
            D = (i - iBegin) / (iEnd - iBegin)
        elif distribution == Distribution.LOG_PLUS:
            D = log(i - iBegin + 1.0) / log(iEnd - iBegin + 1.0)
        elif distribution == Distribution.LOG_MINUS:
            D = 1.0 - log(iEnd - i + 1.0) / log(iEnd - iBegin + 1.0)
        elif distribution == Distribution.LOG_PLUS_MINUS:
            if 0.25 <= left_OVER_all and left_OVER_all <= 0.75:
                iCenter = iBegin + round(left_OVER_all * (iEnd - iBegin))
            else:
                if left_OVER_all < 0.5:
                    xi = 0.25 * sqrt(left_OVER_all * 4)
                else:
                    tmp = (left_OVER_all - 0.75) * 4
                    xi = 0.25 * tmp**2 + 0.75
                iCenter = iBegin + round(xi * (iEnd - iBegin))
            if i <= iCenter:
                D = left_OVER_all * \
                    Distribution.density(i, Distribution.LOG_PLUS, iBegin,
                                         iCenter)
            else:
                D = left_OVER_all + (1.0 - left_OVER_all) * \
                    Distribution.density(i, Distribution.LOG_MINUS, iCenter,
                                         iEnd)
        elif distribution == Distribution.LOG_MINUS_PLUS:
            iCenter = iBegin + round(left_OVER_all * (iEnd - iBegin))
            if i <= iCenter:
                D = left_OVER_all * \
                    Distribution.density(i, Distribution.LOG_MINUS, iBegin,
                                         iCenter)
            else:
                D = left_OVER_all + (1.0 - left_OVER_all) * \
                    Distribution.density(i, Distribution.LOG_PLUS,  iCenter,
                                         iEnd)
        elif distribution == Distribution.RANDOM:
            D = random()
        elif distribution == Distribution.USER:
            D = 0.0
        else:
            assert 0, '??? unknown mesh distribution function'

        return clip(D, 0., 1.)


# Examples ####################################################################

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from numpy import isclose

    if 1:
        xi = Distribution.density(3, Distribution.LIN, 0, 6)  # ==> 0.5
        print('xi:', xi)

    if 1:
        I = range(100)
        for distr in Distribution:
            D = [Distribution.density(i, distr, 0, len(I)-1, 0.25) for i in I]
            plt.plot(I, D, label=distr.name, lw=1)

        plt.title('Mesh density distribution function')
        plt.xlabel('index [/]')
        plt.ylabel('density [/]')
        plt.legend(bbox_to_anchor=(1.1, 1.025), loc='upper left')
        plt.grid()
        plt.show()

    if 1:
        I = range(10)
        xMin, xMax = 0., 1.
        for i, distr in enumerate(Distribution):
            D = [Distribution.density(i, distr, 0, len(I)-1, 0.25) for i in I]
            X = [xMin + d * (xMax - xMin) for d in D]
            Y = [-i] * len(X)

            if not isclose(min(X), xMin):
                print('!!! corr.', distr.name + ', xMin:', min(X), '=>', xMin)
                X[X.index(min(X))] = xMin
            if not isclose(max(X), xMax):
                print('!!! corr.', distr.name + ', xMax:', min(X), '=>', xMax)
                X[X.index(max(X))] = xMax

            plt.scatter(X, Y, c=plt.cm.rainbow(i/(len(Distribution)-1)), s=100,
                        marker=i, label=distr.name)

        plt.title('1D meshes for different distributions')
        plt.xlabel('x [/]')
        plt.ylabel('distribution [/]')
        plt.legend(bbox_to_anchor=(1.1, 1.025), loc='upper left')
        plt.grid()
        plt.show()
