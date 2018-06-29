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
      2018-06-30 DWW
"""

from time import clock
import numpy as np
import matplotlib.pyplot as plt

from coloredlids.numerics.tdma import tdma


def fvm1d_conductivity(nVol=15, 
         L=1., 
         conductivity=lambda x: 1., 
         source=lambda x: 0.,
         silent=True):
    """
    Example of cell centered finite volume discretization in 1D space

        - Compares two variants for calculating the conductivity:
              1. At cell center: k_w = k_e = k(x_P)
              2. At cell faces: k_w=k(x_w) and k_e=k(x_e)

        - Demonstrates that first variant is wrong

    Args:
        nVol (int, optional):
            number of cells (excl. ghost cells)

        L (float, optional):
            east extension of domain: [0, L]

        conductivity (function, optional):
            function returning conductivity as function of x-ccordinate

        source (function, optional):
            function returning source intensity at cell center

        silent (bool, optional):
            if True, print execution time


            0    1        2                nVol   nVol+1 <-- cell index
           ---------------------- ... --------------
           |+|   +   |    +    |       |    +    |+|
           ---------------------- ... --------------
            |                                     |
            |<------------- L ---- ... --------- >
            
    Note:
        This is only a demonstrator without optimization by pre-compilation
    """

    # mesh generation, cells with index 0 and nVol+1 are ghostcells
    Dx = L / nVol
    xCen = np.arange(-0.5*Dx, L+0.5*Dx, Dx)
    xCen[0], xCen[-1] = 0., L
    xVrt = xCen + .5 * Dx
    xVrt[0], xVrt[-1] = xCen[0], xCen[-1]
    if xCen.size <= 10:
        print('+++ xCen:', xCen)
        print('+++ xVrt:', xVrt)
        plt.plot(xCen, xVrt)
        plt.show()

    Lo, Di = np.zeros(xCen.size), np.zeros(xCen.size)
    Up, Rs = np.zeros(xCen.size), np.zeros(xCen.size)

    for conductivityAt in ['center', 'face']:
        for i in range(1, xCen.size-1):
            """
            assembling of matrix [Lo, Di, Up] and right-hand side vector {Rs}

                    k_west     k_east
                       |         |
                       v         v
               -----------------------------
           ... |   +   |    +    |    +    | ...
               -----------------------------
                            ^
                            | kCenter
            """

            if conductivityAt == 'center':
                # conductivity at cell center
                k_west = conductivity(xCen[i])
                k_east = k_west
            else:
                # conductivity at cell faces
                k_west = conductivity(xVrt[i-1])
                k_east = conductivity(xVrt[i])
            Up[i] = -k_east / (xCen[i+1] - xCen[i])
            Lo[i] = -k_west / (xCen[i] - xCen[i-1])
            Di[i] = - Up[i] - Lo[i]
            Rs[i] = (xVrt[i] - xVrt[i-1]) * source(xCen[i])

        # Dirichlet condition (first kind) at west boundary of domain:
        # u_0 * 1 + 0 * u_1 = u_0
        Di[0] = 1.
        Up[0] = 0.
        Rs[0] = 0.  # u(x=0) = 0

        # Dirichlet condition (first kind) at east boundary of domain:
        # u_nVol * 0 + u_{nVol+1} * 1 = u_{nVol+1}
        Lo[-1] = 0.
        Di[-1] = 1.
        Rs[-1] = 1.  # u(x=1) = 1

        if xCen.size <= 10:
            plt.show()
            plt.plot(range(1, xCen.size), Lo[1:], label='lo')
            plt.plot(range(0, xCen.size), Di, label='diag')
            plt.plot(range(0, xCen.size-1), Up[:-1], label='up')
            plt.plot(range(0, xCen.size), Rs, label='rhs')
            plt.legend()
            plt.show()

        print('+++ Equation system  for:', conductivityAt)
        if xCen.size <= 10:
            for l, d, u, r in zip(Lo, Di, Up, Rs):
                print('{:10.3f} {:10.3f} {:10.3f} {:10.3f}'.format(l, d, u, r))

        # solution of linear equation system, U will contain the solution
        start_time = clock()

        u = tdma(Lo, Di, Up, Rs)

        if not silent:
            print('--- n:', u.size, 't:', (clock() - start_time) * 1e3, 'ms')
        plt.plot(xCen, u, label='$k$ at ' + conductivityAt)

    plt.title('Variant with conductivity at cell center fails')
    plt.xlabel('x')
    plt.ylabel('u(x)')
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == '__main__':
    fvm1d_conductivity(nVol=int(1e6), 
                       conductivity=lambda x: 1. if x <= .5 else 2., 
                       silent=False)
