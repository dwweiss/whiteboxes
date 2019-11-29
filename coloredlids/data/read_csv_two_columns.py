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
      2019-11-19 DWW
"""

__all__ = ['read_csv_two_columns']

import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from nptyping import Array
from typing import Tuple


def read_csv_two_columns(path: str, 
                         file: str, 
                         skip: int = 0,
                         delimiter: str = ',',
                         plot: bool = True) \
                         -> Tuple[Array[float], Array[float]]:
    """
    Reads two colums with floating point numbers from comma separated file
    
        # optional header lines 
        1.2, 3.4
        5.6, 7.8
          ...
        9.0, 1.2

    Args:
        path:
            path to file

        file:
            file name incl. extension
            
        skip:
            number of header rows to be skipped
            
        delimiter:
            delimiter between first and second column
            
        plot:
            if True, loaded data will be plotted
            
    Returns:
        X and Y as 1D arrays 
        The returned arrays are empty if file not found
    """
    path.replace('\\', '/')
    full_path = os.path.join(path, file)
    X, Y = [], []
    if os.path.isfile(full_path):
        with open(full_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for i_skip in range(skip):
                next(reader)
            for row in reader:
                X.append(float(row[0]))
                Y.append(float(row[1]))
        csv_file.close()
        if plot:
            print('+++ plot:', full_path)
            plt.plot(X, Y)
            plt.show()
    else:
        print('??? file not found:', full_path)
        
    return np.asfarray(X), np.asfarray(Y)
