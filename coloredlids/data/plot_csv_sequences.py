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
      2019-10-18 DWW
"""

import __init__
__init__.init_path()

import os
import glob
import numpy as np
import pandas 
import matplotlib.pyplot as plt
from typing import List, Tuple

from coloredlids.tools.date_to_seconds import date_to_seconds
from coloredlids.tools.extract_timestamp import extract_timestamp


def plot_csv_sequences(path: str,
                       identifier: str,
                       x_iso: List[float],
                       p1_file: str,
                       p2_file: str,
                       p3_file: str,
                       extension: str = '.data',
                       legend_position: Tuple[float, float] = (1.1, 1.05), ) \
        -> bool:
    """
    1. Plots result curves y(t, x=const) from series of CSV fileds saved 
       at every time step. 

    2. Plots three additional CSV files with parameters p(t) 
    
    Args:
        path:
            path to CSV files series
            
        identifier:
            identifier of CSV files 
            
        x_iso:
            list of x-values for which curves y(t, x=const) are plotted
                        
        p1_file:
            CSV file with p1(t)

        p2_file:
            CSV file with p2(t)

        p3_file:
            CSV file with p3(t)

        extension:
            file extension for time series files 
            
        legend_position:
            position of legend inn matplot curve presentations 
    
    Returns:
        False if no x-values found within the bounds of 'x_iso'
    """
        
    # load x-y-files and find start time
    filenames = []
    os.chdir(path)
    pattern = identifier + '_' + '*' + '_spectrum_device*' + extension
    for file in glob.glob(pattern):
        if extract_timestamp(file):
            filenames.append(file)
    date_ref = extract_timestamp(min(filenames))

    # plot isoquants y(t) for given x
    plt.title('$y(t, x$=const$)$')
    for x_ref in x_iso:
        t_iso, y_iso = [], []
        for file in filenames:
            date = extract_timestamp(file)
            time = date_to_seconds(date, date_ref)
            frame = pandas.read_csv(os.path.join(os.getcwd(), file), 
                                    header=None)
            X, Y = frame[0], frame[1]

            if min(X) < x_ref < max(X):
                y_interp = np.interp(x_ref, X, Y, left=np.nan, 
                                     right=np.nan)
                t_iso.append(time)
                y_iso.append(y_interp)
        if len(t_iso):
            plt.plot(t_iso, y_iso, label=str(x_ref))
    plt.legend(bbox_to_anchor=legend_position, loc='upper left')
    plt.show()

    # plot p1(t), p2(t) and p2(t)
    for file in [p1_file, p2_file, p3_file]:
        full_path = os.path.join(os.getcwd(), file)
        if os.path.isfile(full_path):
            frame = pandas.read_csv(full_path, header=None)
            frame.plot(0, 1)
              
    return len(t_iso)
