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
      2019-10-15 DWW
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
    This class loads 1D curves y(x) from CSV files,
    approximates all curves at the independent variable of the first curve
    finds the areas with the greatest deviation between the curves 
    (optionally for bins)
    
    Note: the current implementation is limited to two curves 
    
    - Loads comma separated files of (x,y) pairs
    - Approximates y_j(x_1) from y_j(x_j) for j=2..m-1
    - Computes difference y_2(x_0) - y_1(x_0)
    - Plots curves and bar diagrams of thinned out y_2_tilde(x_1)
    """
    
    def __init__(self, identifier: str='CompareCurves',
                 argv: Optional[List[str]]=None) -> None:
        super().__init__(identifier=identifier, argv=argv)
        
        self.version = '09.19'
        self.dots: int = 5    # number of dots for ranking of difference
        self.bars: int = 64   # number of bars in thinned-out plots
        self.curves: int = 2
        self.filenames: List[str] = []
    
    def load(self) -> bool:
        self.data = []

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

    def pre(self, **kwargs: Any) -> bool:
        
        super().pre()  # calls method load() of this class

        plt.title('All loaded values')
        for frame in self.data:
            plt.plot(frame[0], frame[1], label=frame.key)
        plt.legend()
        plt.grid()
        plt.show()        
        
        return True

    def task(self, **kwargs: Any) -> float:
        super().task()

        plt.title(r'Interpolated values $\tilde y_2(x_1)$')
        first = self.data[0]
        second = self.data[1]
        x1, y1 = np.asfarray( first[0]), np.asfarray( first[1])
        x2, y2 = np.asfarray(second[0]), np.asfarray(second[1])
        
        # interpolate y2_tilde = y2(x1) from y2(x2)
        y2_over_x1 = np.interp(x1, x2, y2, left=np.nan, right=np.nan)
        
        plt.plot(x1, y1, label='$y_1(x_1)$')
        plt.plot(x2, y2, '.', label='$y_2(x_2)$')
        plt.plot(x1, y2_over_x1, label=r'$\tilde y_2(x_1)$')
        plt.legend()
        plt.grid()
        plt.show()
 
        plt.title(r'Difference between $\tilde y_2(x_1)$ and $y_1(x_1)$')
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
#            print('i_max:', i_max, ', x1 dy:', x1[i_max], dy[i_max])
            plt.plot([x1[i_max]], [dy[i_max]], marker='o', 
                     label='rank: '+ str(k_dot + 1))
        plt.legend()
        plt.grid()
        plt.show()
        
        plt.title(r'Bars of difference $\tilde y_2(x_1) - y_1(x_1)$')
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
#            print('i_max:', i_max, ', x1 dy:', x_thin[i_max], dy_thin[i_max])
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

        # plot x-y position of the greatest y-values
        dy_copy = dy_thin.copy()
        for k_dot in range(self.dots):
            i_max = 0
            for i in range(len(dy_copy)):
                if not np.isnan(dy_copy[i]) and \
                        np.abs(dy_copy[i_max]) < np.abs(dy_copy[i]):
                    i_max = i
            dy_copy[i_max] = np.nan
#            print('i_max:', i_max, ', x1 dy:', x_thin[i_max], dy_thin[i_max])
            plt.plot([x_thin[i_max]], [dy_thin[i_max]], marker='o', 
                     label='rank: '+ str(k_dot + 1))
        plt.legend()
        plt.show()

    def post(self, **kwargs: Any) -> bool:
        super().post()

        return True
