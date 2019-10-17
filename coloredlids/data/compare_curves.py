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
      2019-10-16 DWW
"""

import os
import numpy as np
import pandas 
import matplotlib.pyplot as plt
from typing import Any, List, Optional

from grayboxes.array import xy_thin_out
from grayboxes.base import Base
from grayboxes.dialog import dialog_load_filenames


class CompareCurves(Base):
    """
    Plots the difference between curves y_j(x_j) with different 
    x_j arrays which can be partly overlap 
    
    1. Loads 1D curves y_j(x_j) from multiple CSV files (j=2..m-1)
    
    2. Approximates all curves at independent variable of first curve
           y_j_tilde(x_1) is derived from y_j(x_j) 
    
    3. Finds areas with greatest deviation between the curves 
       (optionally for bins)
    
    4. Plots curves and bar diagrams of thinned out y_j_tilde(x_1) 
    
    Note: 
        The current implementation is limited to m=2 (two curves) 
    """
    
    def __init__(self, identifier: str='CompareCurves',
                 argv: Optional[List[str]]=None) -> None:
        super().__init__(identifier=identifier, argv=argv)
        
        self.version = '10.19'
        self.dots: int = 5    # number of dots for ranking of difference
        self.bars: int = 32        # number of bars in thinned-out plots
        self.curves: int = 2                          # number of curves
        self.filenames: List[str] = []         # list of data file names
    
    def load(self) -> bool:
        self.data: List[np.ndarray] = []

        if self.gui:
            self.filenames = dialog_load_filenames(min_files=self.curves)
        assert len(self.filenames) == self.curves, \
            str((len(self.filenames), self.curves))

        for name in self.filenames:
            key = os.path.splitext(os.path.basename(name))[0] 
            if key in [frame.key for frame in self.data]:
                self.warn('duplicated files: ' + str(self.filenames))
            self.write("    Load: '" + key + "'")
            frame = pandas.read_csv(name, header=None)
            frame.key = key
            self.data.append(frame)
            
        return len(self.data) > 0

    def pre(self, **kwargs: Any) -> bool:
        super().pre()                                     # calls load()

        plt.title('Loaded values')
        for frame in self.data:
            plt.plot(frame[0], frame[1], label=frame.key)
        plt.legend()
        plt.grid()
        plt.show()
        
        return True

    def task(self, **kwargs: Any) -> float:
        super().task()

        # extract arrays
        first = self.data[0]          # first 2D array [0..1, 0..n1-1]
        second = self.data[1]        # second 2D array [0..1, 0..n2-1]
        x1, y1 = np.asfarray( first[0]), np.asfarray( first[1])
        x2, y2 = np.asfarray(second[0]), np.asfarray(second[1])
        x3, y3, x4, y4 = None, None, None, None
        if self.curves > 2:
            third = self.data[2]      # third 2D array [0..1, 0..n3-1]
            x3, y3 = np.asfarray(third[0]), np.asfarray(third[1])
        if self.curves > 3:
            fourth = self.data[3]    # fourth 2D array [0..1, 0..n4-1]
            x4, y4 = np.asfarray(fourth[0]), np.asfarray(fourth[1])
        
        # interpolate yj_tilde = yj(x1) derived from from yj(xj)
        y2_over_x1 = np.interp(x1, x2, y2, left=np.nan, right=np.nan)
        if y3:
            y3_over_x1 = np.interp(x1, x3, y3, left=np.nan, right=np.nan)
        if y4:
            y4_over_x1 = np.interp(x1, x4, y4, left=np.nan, right=np.nan)
        
        plt.title(r'Interpolated values $\tilde y_j(x_1), j=0..' + 
                  str(self.curves) + '$')
        plt.plot(x1, y1, label='$y_1(x_1)$')
        plt.plot(x2, y2, '.', label='$y_2(x_2)$')
        plt.plot(x1, y2_over_x1, label=r'$\tilde y_2(x_1)$')
        if y3:
            plt.plot(x3, y3, '.', label='$y_3(x_3)$')
            plt.plot(x1, y3_over_x1, label=r'$\tilde y_3(x_1)$')
        if y4:
            plt.plot(x4, y4, '.', label='$y_4(x_4)$')
            plt.plot(x1, y4_over_x1, label=r'$\tilde y_4(x_1)$')
        plt.legend()
        plt.grid()
        plt.show()
 
    
        plt.title(r'Difference between $\tilde y_j(x_1)$ and $y_1(x_1)$')
        dy = y2_over_x1 - y1
        plt.xlim([min(x1.min(), x2.min()), max(x1.max(), x2.max())])
        plt.plot(x1, dy, label=r'$\tilde y_2(x_1) - y_1(x_1)$')
        
        # plot x-y position of the group of greatest y-values
        dy_copy = dy.copy()
        for k_dot in range(self.dots):
            i_max = 0
            for i in range(len(dy_copy)):
                if not np.isnan(dy_copy[i]) and \
                        np.abs(dy_copy[i_max]) < np.abs(dy_copy[i]):
                    i_max = i
            dy_copy[i_max] = np.nan
            plt.plot([x1[i_max]], [dy[i_max]], marker='o', 
                     label='rank: '+ str(k_dot + 1))
        plt.legend()
        plt.grid()
        plt.show()
        
        
        plt.title(r'Bars of difference $\tilde y_j(x_1) - y_1(x_1)$')
        x_thin, dy_thin = xy_thin_out(x1, dy, self.bars)
        plt.bar(x_thin, dy_thin, width=(x_thin[1] - x_thin[0]) * 0.66, 
                align='edge')

        # plot x-y position of the greatest y-values
        dy_copy = dy_thin.copy()
        for k_dot in range(self.dots):
            i_max = 0
            for i in range(len(dy_copy)):
                if not np.isnan(dy_copy[i]) and \
                        np.abs(dy_copy[i_max]) < np.abs(dy_copy[i]):
                    i_max = i
            dy_copy[i_max] = np.nan
            plt.plot([x_thin[i_max]], [dy_thin[i_max]], marker='o', 
                     label='rank: '+ str(k_dot + 1))
        plt.legend()
        plt.show()


        plt.title(r'Relative difference $(\tilde y_2(x_1)-y_1(x_1)) ' +
                  '/ y_1(x_1)$ [%]')
        dy = dy / y1 * 100
        x_thin, dy_thin = xy_thin_out(x1, dy, self.bars)
        plt.bar(x_thin, dy_thin, width=(x_thin[1] - x_thin[0]) * 0.66, 
                align='edge')

        # plot x-y position of the greatest dy-values
        dy_copy = dy_thin.copy()
        for k_dot in range(self.dots):
            i_max = 0
            for i in range(len(dy_copy)):
                if not np.isnan(dy_copy[i]) and \
                        np.abs(dy_copy[i_max]) < np.abs(dy_copy[i]):
                    i_max = i
            dy_copy[i_max] = np.nan
            plt.plot([x_thin[i_max]], [dy_thin[i_max]], marker='o', 
                     label='rank: '+ str(k_dot + 1))
        plt.legend()
        plt.show()

        return 0.