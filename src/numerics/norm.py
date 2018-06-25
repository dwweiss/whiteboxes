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
      2017-12-18 DWW
"""

import numpy as np


def L2_norm(y, Y):
    """
    Square root of mean squared difference between arrays y and Y

    Args:
        y (array_like of float):
            indicated values

        Y (array_like of float):
            conventional true values

    Returns:
        (double):
            Error
    """
    return np.sqrt(np.mean(np.square(np.asfarray(y) - np.asfarray(Y))))


def SSE(y, Y):
    """
    Sum of squared difference between arrays y and Y

    Args:
        y (array_like of float):
            indicated values

        Y (array_like of float):
            conventional true values

    Returns:
         (double):
             Error

    Note:
         SSE = 0.5 * np.square(L2_norm(y, Y)) * y.size
    """
    return 0.5 * np.sum(np.square(np.asfarray(y) - np.asfarray(Y)))


def MSE(y, Y):
    """
    Mean squared difference between arrays y and Y

    Args:
        y (array_like of float):
            indicated values

        Y (array_like of float):
            conventional true values

    Returns:
        (double):
            Error
    """
    return np.mean(np.square(np.asfarray(y) - np.asfarray(Y)))
