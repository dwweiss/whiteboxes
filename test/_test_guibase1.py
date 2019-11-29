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
      2019-11-13 DWW
"""

import __init__
__init__.init_path()

import unittest

import random
import time
from matplotlib.figure import Figure
from tkinter.ttk import Progressbar
from typing import Any, Dict, Optional

from coloredlids.gui.guibase1 import GuiBase1


def model_random_data(data: Dict[str, Any], 
                      figure: Optional[Figure]=None, 
                      progress: Optional[Progressbar]=None) -> float:
    """
    Implements user-defined model, plots otput on canvas, 
        updates progress bar   
    
    Args:
        data:
            parameter and results of model
            
        figure:
            figure on plotting canvas, contains: .axes and .canvas
            
        progress: 
            progress bar, update with:
                progress['value'] = int/float(percentage)
            
    Returns:
        result indicator of simulation
        
    Note:
        The figure can be updated with: figure.canvas.draw()
    """

    n = int(data.get('time [days]', 1))
    ylo1, yhi1 = data.get('n3', -3), data.get('n4', 7)
    ylo2, yhi2 = data.get('n5', -7), 7

    start = time.time()
    prev = start
    
    res = 0.123456

    if figure is not None:
        ax1 = figure.axes[0]
        ax2 = figure.axes[1] if len(figure.axes) > 1 else None        
        ax1.set_xlim(0, n)   
        ax1.set_ylim(ylo1, yhi1)
        if ax2:
            ax2.set_ylim(ylo2, yhi2)
        ax1.plot(0., 0., color='red', marker='x', linestyle='')
        figure.canvas.draw()
    
    for it in range(n):
        ###############################
        y1 = random.uniform(ylo1, yhi1)
        y2 = random.uniform(ylo2, yhi2)
        ###############################
        
        x = it+1
        if figure is not None:
            ax1.plot(x, y1, marker='o', markersize=3, color='red')
            if ax2:
                ax2.plot(x, y2, marker='o', markersize=3, color='blue')

        now = time.time()
        dt = now - prev
        if dt > 2.:
            prev = now

            if not data.get('silent', True):
                print('wall clock time:', now - start)
            if figure is not None:
                figure.canvas.draw()
            
        if progress is not None:
            progress['value'] = it / n * 100
        time.sleep(0.01)

    if figure is not None:            
        figure.canvas.draw()
    
    return res

           
class TestUM(unittest.TestCase):
    """
    Tests involve user interaction; The name of this file starts with 
    letter '_' in order to avoid execution by test_All.py
    """
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def _test1(self):
        gui = GuiBase1(model=lambda data, figure, progress: 0.0)
        gui()

        self.assertTrue(True)

    def _test2(self):
        gui = GuiBase1()
        gui()

        self.assertTrue(True)

    def test3(self):
        gui = GuiBase1(
            identifier='Test 1',
            path = None,
            model=model_random_data, 
            labels=['$t$ [days]', '$y_1$ [/]', '$y_2$ [/]', ],
            param_list = [
                # widget   name  min max default (widget+name mandatory)
                ('spin',   'mode', 0, 4, 3), 
                ('spin',   'boxcar',-1, 3, 2),
                ('slider', 'iterations', 0, 500, 50), 
                ('slider', 'time [days]', 0, 1000, 100), 
                ('slider', 'n3', -30, 0, -10),
                ('slider', 'n4', 0, 50, 10),
                ('entry',  'relaxation', 0., 1., '0.66'), 
                ('slider', 'n5'),
            ]
        )

        gui()
        
        self.assertTrue(True)

   
if __name__ == '__main__':
    unittest.main()
