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
      2019-11-07 DWW
"""

import __init__
__init__.init_path()

import unittest

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes._subplots import Axes
from typing import Any, Dict, List
import random
import time

from coloredlids.gui.guibase1 import GuiBase1


def model(data: Dict[str, Any], 
          canvas: FigureCanvasTkAgg,
          axes: List[Axes]) -> float:
    """
    Implements user-defined model 
    
    Args:
        data:
            parameter and results of model
            
        canvas:
            plotting canvas
            
        axes:
            subplot of matplotlib figure
            
    Returns:
        result of analyis
    """
    res = 0.123456

    n = int(data['time [days]'])
    ax1, ax2 = axes
    
    ax1.set_xlim(0, n)   
    ax1.set_ylim(-2, 2)
    ax1.plot(0., 0., color='red', marker='x', linestyle='')
    canvas.draw()
    
    start = time.time()
    prev = start
    for it in range(n):

        ###############################
        y1 = random.uniform(-1, 1)
        y2 = random.uniform(-1, 1)
        ###############################
        
        x = it+1
        ax1.plot(x, y1, marker='o', markersize=3, color='red')
        ax2.plot(x, y2, marker='o', markersize=3, color='blue')

        now = time.time()
        dt = now - prev
        if dt > 2.:
            if not data['silent']:
                print('wall clock time:', now - start)
            prev = now
            canvas.draw()
            
        time.sleep(0.1)
        
    canvas.draw()
    
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

    def test1(self):
        gui = GuiBase1(
            identifier='Test 1', 
            model=model, 
            labels=['$t$ [days]', '$y_1$ [/]', '$y_2$ [/]', ],
            param_list = (
                ('spin',   ['mode', 0, 4, 'ref'], 
                           ['boxcar']),
                ('slider', ['iterations', 0, 500, 50], 
                           ['time [days]', 0, 1000, 100], 
                           ['n3']),
                ('entry',  ['relaxation', 0., 1., '0.66'], 
                           ['limit', 0., 1., 8.9]),
                ('slider', ['n5']),
                ('slider', ['sl2', 0, 500, 33]),
                ('check',  ['calibrate', None, None, False], 
                           ['silent', None, None, True]),
                ('label',  ['result', None, None, '?']), 
            )
)
        gui()
        
        self.assertTrue(True)

   
if __name__ == '__main__':
    unittest.main()
