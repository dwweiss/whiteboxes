"""
  Copyright (c) 2016-17 by Dietmar W Weiss

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
      2017-12-06 DWW
"""


import numpy as np


def vAxial(v_mean=1, D_pipe=1, r=0, nu=1e-6, Lambda=None, n=6):
    """
    Computes axial velocity distribution v_z(r) in a pipe.

    r
    ^
    |------
    |      -----
    |           ----  v_z(r)
    |               ---
    |                  --
    |                    --
    ---------------------------> z

    Args:
        v_mean (float or array of float, optional):
            mean of axial velocity component [m/s]

        D_pipe (float or array of float, optional):
            inner pipe diameter [m]

        r (float or array of float, optional):
            actual radius for which axial velocity is computed [m]

        nu (float or array of float, optional):
            kinematic viscosity [m^2/s]

        Lambda (float or array of float, optional):
            friction coefficient (0.01 <= Lambda <= 0.1) [/]
            (n,lambda) = {(4, .06), (5, .04), ()}

        n (float or array of float, optional):
            parabel coefficient (3 <= n <= 10) [/]
            (smooth pipe surface: n=6..10, rough surface: n=4)

    Returns:
        velocity component in radial direction [m/s]

    Reference:
        Bernd Glueck: Hydrodynamische und gasdynamische Rohstroemung.
            Verlag fuer Bauwesen, Berlin 1988
            (laminar: equ. 1.6 and 1.8, turbulent: equ. 1.02, 1.21, 1.23)
    """
    Re = v_mean * D_pipe / nu
    if Re < 2300:
        v_max = 2 * v_mean
        return v_max * (1.0 - 4 * (r / D_pipe)**2)
    else:
        # smooth pipe surface: n=6..10, rough: n=4
        if Lambda is None:
            if n is None:
                n = 6
            reciprocal_for_n = 1. / n
        else:
            reciprocal_for_n = np.sqrt(Lambda)
        x = (reciprocal_for_n + 2) * (reciprocal_for_n + 1)
        v_max = v_mean * x / 2
        return v_max * (1.0 - 2 * r / D_pipe)**reciprocal_for_n


# Examples ####################################################################

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    D = 50e-3
    v_mean = 1
    r = np.linspace(0, D*0.5, num=100)
    n_seq = [3, 4, 6, 8, 10]
    nu_seq = [1e-6, 1e-2]

    for n in n_seq:
        for nu in nu_seq:
            vz = vAxial(v_mean=v_mean, D_pipe=D, r=r, nu=nu, n=n)
            plt.plot(vz, r, label='$n:'+str(n)+r',\ \nu: '+str(nu)+'$')

    fontsize = 12
    plt.title(r'Axial velocity $v_z(r) = f(n, \nu)$')
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams['legend.fontsize'] = fontsize
    plt.xlim(0, 2.2 * v_mean)
    plt.ylabel('$r$ [m]')
    plt.xlabel('$v_z$ [m/s]')
    plt.grid()
    plt.legend(bbox_to_anchor=(1.1, 1.03), loc='upper left')
    plt.show()
