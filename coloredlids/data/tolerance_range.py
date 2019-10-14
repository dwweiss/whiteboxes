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
      2018-10-15 DWW
"""

import numpy as np
from coloredlids.data.status import Status
from coloredlids.data.inrange import in_range


class ToleranceRange(object):
    """
    Ranges of tolerances around data points

    This class stores ranges around a point in multi-dimensional space. 
    It can check if the values are within the expected(), tolerated(), 
    local() and global() windows. 
    It stores the statuses of the data points.

    Note:
        The reference() point can be located outside the
        expected(), tolerated(), local() and global() windows.

        y ^     global()
          |     ------------------------------------o
          |    |                                    |
          |    |   local()                          |
          |    |   ------------------------o        |
          |    |  |                 V      |        |
          |    |  |  tolerated()           |        |
          |    |  |   ---------------o     |        |
          |    |  |  |               |     |        |
          |    |  |  |  expected()   |     |        |
          |    |  |  |   --------o   | V   |        |
          |    |  |  |  | V      |   |     |        |
          |    |  |  |  |   o    | V |     |        |
          |    |  |  |  | refer- |   |     |        |
          |    |  |  |  | ence() |   |   V |        |   V ... values()
          |    |  |  |  |        |   |     |        |
          |    |  |  |  | V   V  |   |     |        |
          |    |  |  |  o--------    |     |        |
          |    |  |  |         V     |     |        |
          |    |  |  o---------------      |        |
          |    |  o------------------------         |
          |    o------------------------------------
          |
          +----------------------------------------------> x
    """

    def __init__(self):
        self._axes = ['x0', 'x1']      # real-world name of axes
        self._reference = None         # reference point
        self._values = None            # 2D array of values
        self._statuses = None          # 1D array of statuses
        self.expected = None
        self.tolerated = None
        self.local = None
        self.Global = None

    @property
    def axes(self):
        return self._axes

    @axes.setter
    def axes(self, value):
        if value is None:
            self._axes = None
            return
        self._axes = np.atleast_1d(value)
        assert self._values is None or self._axes.size <= self._values.shape[1]

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, value):
        if value is None:
            self._reference = None
            return
        self._reference = np.atleast_1d(value)
        assert self._values is None or \
            self._reference.size <= self._values.shape[1]

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, X):
        if X is None:
            self._values = None
            return
        self._values = np.atleast_2d(X)
        assert self._axes is None or self._axes.size <= self._values.shape[1]
        assert self._statuses is None or \
            self._statuses.size == self._values.shape[0]

    @property
    def statuses(self):
        return self._statuses

    @statuses.setter
    def statuses(self, value):
        """
        Sets status array

        Args:
            value (Status or array of Status):
                single Status or array of statuses. If single array, status
                array will be extended to numer of rows of values array
        """
        if value is None:
            self._statuses = None
            return
        self._statuses = np.atleast_1d(value)
        if self._values is None and \
           self._statuses.size == 1 and self.values.shape[0] > 1:
            self._statuses = np.full(shape=self.values.shape[0],
                                     fill_value=value, dtype=Status)

        assert self._values is None or \
            self._statuses.size == self.values.shape[0]

    def evaluate(self, P=None, tolerance=1e-10):
        """
        Checks that point P or all points are within "expected" or 
        "tolerated" ranges

        Args:
            P (tuple of float, optional):
                data point. If None, all 'self._values' will be checked

            tolerance (float);
                tolerance for checking

        Returns:
            status over all points (expected, tolerated, failed)
        """
        if self._statuses is None:
            self._statuses = np.full(shape=self.values.shape[0],
                                     fill_value=Status.FAIL, dtype=Status)
        if P is None:
            b = True
            for i in range(self._values.shape[0]):
                self._statuses[i] = Status.FAIL
                b = True
                for j in range(self._axes.size):
                    b = b and in_range(self._values[i][j], self.expected[j],
                                       tolerance)
                if b:
                    self._statuses[i] = Status.SUCCESS
                else:
                    b = True
                    for j in range(self._axes.size):
                        b = b and in_range(self._values[i][j],
                                           self.tolerated[j], tolerance)
                    if b:
                        self._statuses[i] = Status.TOLERATE

            for stat in [Status.FAIL, Status.TOLERATE, Status.SUCCESS]:
                if stat in self._statuses:
                    return stat
            assert 0
        else:
            b = True
            for j in range(self._axes.size):
                b = b and in_range(P, self.expected, tolerance)
            if b:
                return Status.SUCCESS
            b = True
            for j in range(self._axes.size):
                b = b and in_range(P, self.tolerated, tolerance)
            if b:
                return Status.TOLERATE
            return Status.FAIL
