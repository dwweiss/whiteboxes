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

import sys
import subprocess
import pickle
import numpy as np
import os


"""
Demonstrates passing of a numpy array to a subprocess and receiving numpy
array from subprocess
"""

if __name__ == '__main__':
    function = os.path.basename(__file__)

    if 'worker' in sys.argv:
        x = np.loads(sys.stdin.buffer.read())
        y = x * 1.1 + 2
        sys.stdout.buffer.write(pickle.dumps(y))
    else:
        x = np.arange(6).reshape(2, 3)

        y = pickle.loads(subprocess.check_output(
                  [sys.executable, function, 'worker'], input=pickle.dumps(x)))

        print('x:', x, '\ny:', y)
