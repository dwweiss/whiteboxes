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
      2018-06-18 DWW
"""

import numpy as np
from numba import jit


@jit
def tdma(C, A, B, D):
    """
    Solves tridiagonal equation system: [C, A, B] = {D}

    | a[0] b[0]               |   | d[0]_out   |     | d[0]_inp   |
    | c[1] a[1] b[1]          |   | d[1]_out   |     | d[1]_inp   |
    |      c[2] a[2]   b[2]   | * | d[2]_out   |  =  | d[2]_inp   |

                 ...    ...          ...

    |           c[N-1] a[N-1] |   | d[N-1]_out |     | d[N-1]_inp |

    Args:
        C, A, B (1D array of float):
            matrix diagonals;  will be modified

        D  (1D array of float):
            right-hand side vector; will contain solution after return

    Returns:
        (1D array of float):
            solution of equation system

    Reference:
        Patankar, S.V.: Numerical Heat Transfer and Fluid Flow.
        Hemisphere Publishing Corporation, Washington, 1980
    """
    n = len(A)
    assert n > 1

    B[0] /= -A[0]
    C[0] = D[0] / A[0]

    for i in range(1, n):
        tmp = C[i] * B[i-1]
        B[i] /= - (A[i] + tmp)
        C[i] = (D[i] - C[i] * C[i-1]) / (A[i] + tmp)

    D[-1] = C[-1]
    for i in range(n-2, -1, -1):
        D[i] = B[i] * D[i+1] + C[i]

    return D


# Examples ####################################################################

if __name__ == '__main__':
    import sys
    from time import clock
    import matplotlib.pyplot as plt

    print('*** Begin test TDMA')
    n = 1 * 64
    n = int(1e9)
    lo = np.random.random(n)
    dg = np.random.random(n)
    up = np.random.random(n)
    rs = np.random.random(n)
    if 0:
        Type = np.float32
        lo, dg = np.float32(lo), np.float32(dg)
        up, rs = np.float32(up), np.float32(rs)
    else:
        Type = np.float64

    if n <= 100:
        plt.plot(lo, label='lo')
        plt.plot(dg, label='dg')
        plt.plot(up, label='up')
        plt.plot(rs, label='rs')
        plt.legend()
        plt.show()

    print('+++ type:', rs.dtype)
    print('+++ lo dg up rs:', rs.dtype, lo.shape, dg.shape, up.shape, rs.shape)

    sys.stdout.flush()
    for i in range(10):
        start = clock()
        x = tdma(lo, dg, up, rs)
        print('+++ t(' + str(i) + '):', (clock() - start)*1e3, 'ms dtype:',
              dg.dtype, x.dtype)

    del lo, dg, up, rs

    print('*** End test TDMA')
