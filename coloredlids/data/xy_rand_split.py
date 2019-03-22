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
      2019-03-22 DWW
"""

__all__ = ['xy_rand_split']

import numpy as np
from typing import Optional, Sequence, Tuple


def xy_rand_split(x: np.ndarray, y: Optional[np.ndarray]=None,
                  fractions: Optional[Sequence[float]]=None) \
        -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Splits randomly one or two 2D arrays into sub-arrays, size of the sub 
    arrays is defined by a list of 'fractions'

    Example:
        from coloredlids.xy_rand_split import xy_rand_split
        x = [1, 2, 3, 4, 5, 6]
        y = [3, 4, 5, 6, 7, 8]
        x = np.atleast_2d(x).T  # 2D array with one column
        y = np.atleast_2d(y).T  # 2D array with one column
        fractions = [0.3, 0.1, 0.2]
        X, Y = xy_rand_split(x=x, y=y, fractions=fractions)
        # sum(fractions) is 0.6, size (shape[0]) of x and y is 6 
        # -> sub-array sizes are 0.3/0.6*6=3, 0.1/0.6*6=1 and 0.2/0.6*6=2
        
        return values:
            X = [[4, 6, 2], [1], [3, 5]] 
            Y = [[6, 8, 4], [3], [5, 7]]
 
    Args:
        x (2D array of float):
            data array, first index is point index

        y (2D array of float):
            data array, first index is point index

        fractions:
            size of sub arrays is defined by ratios of elements of fractions 
            list relative to sum of fractions
            
    Returns:
        Pair of lists of 2D sub-arrays of float
    """
    assert len(x.shape) == 2, str(x.shape)
    if y is not None:
        assert len(y.shape) == 2, str((x.shape, y.shape))
        assert x.shape[0] == y.shape[0], str((x.shape, y.shape))

    if fractions is None:
        fractions = (0.8, 0.2)
    fractions = [f / sum(fractions) for f in fractions]
    subset_sizes = [round(f * x.shape[0]) for f in list(fractions)]
    defect = x.shape[0] - sum(subset_sizes)
    subset_sizes[0] += defect

    all_indices = np.random.permutation(x.shape[0])
    begin = 0
    subset_indices = [] # all_indices[:subset_sizes[0]]
    for i in range(len(subset_sizes)):
        end = begin + subset_sizes[i]
        subset_indices.append(all_indices[begin:end])
        begin += subset_sizes[i]
    x_split = []
    y_split = [] if y is not None else None
    for indices in subset_indices:
        x_split.append(x[indices, :])
        if y is not None:
            y_split.append(y[indices, :])

    return x_split, y_split
