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

  Version
      2018-05-15 DWW

  Reference
      Blevins: Applied fluid dynamics handbook, table 6-5, p. 57
      https://neutrium.net/fluid_flow/
              pressure-drop-from-fittings-expansion-and-reduction-in-pipe-size/
"""

from math import log10, fabs, sqrt, sin, radians
from scipy.optimize import fsolve
import numpy as np

# upper limit of laminar pipe flow range of Reynolds numbers
REYNOLDS_PIPE_LAMINAR = 2300


def pressureDrop(k, v, rho):
    """
    Pressure drop in hydraulic component from given resistance coefficient

    Args:
        k (float):
            resistance coefficient [/], (k=0: no resistance)

        v (float):
            axial component of velocity [m/s]

        rho (float):
            density of fluid [kg/m^3]

    Returns:
        (float):
            pressure drop between outlet and inlet of component [Pa]
    """
    return k * v*v * 0.5 * rho


def poiseulleColebrook(Re, D, eps_rough, biSectionalSearch=False):
    """
    Friction factor of straight pipe

    Args:
        Re (float):
            Reynolds number

        D (float):
            inner pipe diameter [m]

        eps_rough (float):
            inner pipe roughness [m]

        biSectionalSearch (bool, optional):
            if True then bisectional cut for root finding instead of
            Netwon-like method

    Returns:
        f (float):
            friction factor after Poiseulle and Colebrook [/]
    """
    if Re <= REYNOLDS_PIPE_LAMINAR:
        # Laminar: Poiseulle's law
        return 64. / Re
    else:
        # Turbulent: Colebrook approximation
        if biSectionalSearch:
            assert 0, 'not implemented'
        else:
            a = eps_rough / (3.71 * D)
            b = 2.51 / Re

            def equ(f):
                one_over_2sqrt_f = 0.5 / sqrt(f)
                return one_over_2sqrt_f + log10(a + b * one_over_2sqrt_f)

            f = fsolve(equ, 0.02)
            assert fabs(equ(f)) < 1.0e-5

        return f[0]


def resistancePipe(v, D, L=1.0, nu=1e-6, eps_rough=10e-6):
    """
    -----------------
          v
    D   --->

    -----------------
    <- - - L - - - ->

    Resistance coefficient of straight pipe

    Args:
        v (float):
            axial component of velocity at inlet [m/s]

        D (float):
            inner pipe diameter at inlet [m]

        L (float, optional):
            pipe length [m]

        nu (float, optional):
            kinematic viscosity [m^2/s]

        eps_rough (float, optional):
            inner pipe roughness [m]

    Returns:
        (float)
           resistance coefficient  [/]
    """
    return L / D * poiseulleColebrook(Re=v*D/nu, D=D, eps_rough=eps_rough)


def _resistanceModerateBend(v, D, rBend, phiBendDeg, nu, eps_rough):
    """
    Resistance coefficient of moderate pipe bend with: rBend/D >= 1.8

    Args:
        v (float):
            axial component of velocity at inlet [m/s]

        D (float):
            inner pipe diameter at inlet and outlet [m]

        rBend (float):
            bending radius [m]

        phiBendDeg (float):
            bending angle [deg]

        nu (float):
            kinematic viscosity [m^2/s]

        eps_rough (float):
            inner pipe roughness [m]

    Returns:
        (float):
            resistance coefficient  [/]
    """
    ratio = rBend / D
    assert ratio >= 1.8, 'not moderate bend'

    alpha = 1.0
    if ratio < 50.0:
        if phiBendDeg <= 45.0:
            alpha = 1.0 + 5.13 * ratio**-1.47
        elif phiBendDeg <= 90.:
            if ratio < 9.85:
                alpha = 0.95 + 4.42 * ratio**-1.96
        else:
            alpha = 1.0 + 5.06 * ratio**-4.52

    Re = v * D / nu
    if Re / ratio**2 <= 360.:
        fC = 0.336 * (Re * np.sqrt(ratio))**-0.2
        return 0.0175 * alpha * fC * phiBendDeg * ratio
    else:
        return 0.00431 * alpha * phiBendDeg * Re**-0.17 * ratio**0.84


def _resistanceSharpBend(v, D, rBend, phiBendDeg, nu, eps_rough):
    """
    Resistance coefficient of sharp pipe bend with: rBend/DPipe < 1.8

    Args:
        v (float):
            axial component of velocity at inlet [m/s]

        D (float):
            inner pipe diameter at inlet and outlet [m]

        rBend (float):
            bending radius [m]

        phiBendDeg (float):
            bending angle [deg]

        nu (float):
            kinematic viscosity [m^2/s]

        eps_rough (float):
            inner pipe roughness [m]

    Returns:
        (float):
            resistance coefficient  [/]
    """
    Re = v * D / nu
    x = rBend / D         # example: x(D=80mm, rBend=112.5mm) = 2.81

    if x >= 1.8:
        print("??? function called with x: '" + str(x) + "'")

    if phiBendDeg < 20.:
        if   x <= 0.5:  K = 0.053
        elif x <= 0.75: K = 0.038
        elif x <= 1.0:  K = 0.035
        elif x <= 1.5:  K = 0.040
        else:           K = 0.045
    elif phiBendDeg <= 30.:
        if   x <= 0.5:  K = 0.12
        elif x <= 0.75: K = 0.070
        elif x <= 1.0:  K = 0.058
        elif x <= 1.5:  K = 0.060
        else:           K = 0.065
    elif phiBendDeg <= 45.:
        if   x <= 0.5:  K = 0.27
        elif x <= 0.75: K = 0.14
        elif x <= 1.0:  K = 0.10
        elif x <= 1.5:  K = 0.090
        else:           K = 0.089
    elif phiBendDeg <= 75.:
        if   x <= 0.5:  K = 0.80
        elif x <= 0.75: K = 0.31
        elif x <= 1.0:  K = 0.20
        elif x <= 1.5:  K = 0.15
        else:           K = 0.14
    elif phiBendDeg <= 90.:
        if   x <= 0.5:  K = 1.1
        elif x <= 0.75: K = 0.40
        elif x <= 1.0:  K = 0.25
        elif x <= 1.5:  K = 0.18
        else:           K = 0.16
    else:
        assert x > 0.5, 'Invalid configuration'
        # if   x <= 0.75: K = 0.70
        # elif x <= 1.0:  K = 0.28
        # elif x <= 1.5:  K = 0.21

    if Re < 5e5:
        K *= (5e5 / Re)**0.17
    return K


def resistancePipeBend(v, D, rBend, phiBendDeg, nu=1e-6, eps_rough=10e-6):
    """
    Resistance coefficient of pipe bend

    Args:
        v (float):
            axial component of velocity at inlet [m/s]

        D (float):
            inner pipe diameter at inlet and outlet [m]

        rBend (float):
            bending radius [m]

        phiBendDeg (float):
            bending angle [degrees]

        nu (float, optional):
            kinematic viscosity [m^2/s]

        eps_rough (float, optional):
            inner pipe roughness [m]

    Returns:
        (float):
            resistance coefficient  [/]
    """
    if rBend / D >= 1.8:
        return _resistanceModerateBend(v, D, rBend, phiBendDeg, nu, eps_rough)
    else:
        return _resistanceSharpBend(v, D, rBend, phiBendDeg, nu, eps_rough)


def resistanceSquarePipeReduction(v1, D1, D2, nu=1e-6, eps_rough=10e-6):
    """
    Resistance coefficient of squared pipe reduction

    -----------------+
                     |
          v1         +----------
    D1   --->                 D2
                     +----------
                     |
    -----------------+

    Args:
        v1 (float):
            axial component of velocity at inlet [m/s]

        D1 (float):
            inner pipe diameter at inlet [m]

        D2 (float):
            inner pipe diameter of middle section [m]

        nu (float, optional):
            kinematic viscosity [m^2/s]

        eps_rough (float, optional):
            inner pipe roughness [m]

    Returns:
        (float):
            resistance coefficient  [/]

    Note
        Use v1 as velocity in pressure drop calculations
        Switching from laminar to turbulent flow is at REYNOLDS_PIPE_LAMINAR
        Transition range is neglected
    """

    # correction of possibly confused inlet and outlet values
    (d1, d2) = (D1, D2) if D1 > D2 else (D2, D1)
    Re1 = v1 * d1 / nu   # Reynolds number at inlet
    if Re1 < REYNOLDS_PIPE_LAMINAR:
        # laminar
        return (1.2 + 160 / Re1) * ((d1 / d2)**4 - 1)
    else:
        # turbulent
        f1 = poiseulleColebrook(Re=Re1, D=d1, eps_rough=eps_rough)
        x = (d1 / d2)**2
        return (0.6 + 0.48 * f1) * x * (x-1)


def resistanceTaperedPipeReduction(v1, D1, D2, nu=1e-6, eps_rough=10e-6,
                                   alphaDeg=90.):
    """
    Resistance coefficient of tapered pipe reduction

    ---------------+
                    \
         v1       /  +----------
    D1  --->    alpha         D2
                  \  +----------
                    /
    ---------------+

    Args:
        v1 (float):
            axial component of velocity at inlet [m/s]

        D1 (float):
            inner pipe diameter at inlet [m]

        D2 (float):
            inner pipe diameter of middle section [m]

        nu (float, optional):
            kinematic viscosity [m^2/s]

        eps_rough (float, optional):
            inner pipe roughness [m]

        alphaDeg (float, optional):
            opening angle (over both sides) [deg]

    Returns:
        (float):
            resistance coefficient  [/]

    Note:
        1) if alpha=90 deg, function returns 0.7071*squarePipeReduction
        2) use v1 for velocity in pressure drop calculations

    """
    x = sin(0.5*radians(alphaDeg))
    if alphaDeg < 45.:
        x *= 1.6
    else:
        x = np.sqrt(x)
    return x * resistanceSquarePipeReduction(v1, D1, D2, nu, eps_rough)


def resistanceSquarePipeExpansion(v1, D1, D2, nu=1e-6, eps_rough=10e-6):
    """
    Resistance coefficient of squared pipe expansion

    -----------------+
                     |
                     +----------
    D2             <--v1--    D1
                     +----------
                     |
    -----------------+

    Args:
        v1 (float):
            axial component of velocity at inlet [m/s]

        D1 (float):
            inner pipe diameter at inlet [m]

        D2 (float):
            inner pipe diameter of middle section [m]

        nu (float, optional):
            kinematic viscosity [m^2/s]

        eps_rough (float, optional):
            inner pipe roughness [m]

    Returns:
        (float):
            resistance coefficient [/]
    Note
        use v1 as velocity in pressure drop calculations
    """
    # correction of possibly confused inlet and outlet values
    d1, d2 = (D1, D2) if D1 < D2 else (D2, D1)
    Re1 = v1 * d1 / nu   # Reynolds number at inlet
    if Re1 < REYNOLDS_PIPE_LAMINAR:
        # laminar
        return 2 * (1 - (d1 / d2)**4)
    else:
        # turbulent
        f1 = poiseulleColebrook(Re=Re1, D=d1, eps_rough=eps_rough)
        return (1 + 0.8 * f1) * (1 - (d1 / d2)**2)**2


def resistanceTaperedPipeExpansion(v1, D1, D2, nu=1e-6, eps_rough=10e-6,
                                   alphaDeg=90.):
    """
    Resistance coefficient of tapered pipe expansion

    ---------------+
                    \
                  /  +----------
    D2         alpha  <-v1--  D1
                  \  +----------
                    /
    ---------------+

    Args:
        v1 (float):
            axial component of velocity at inlet [m/s]

        D1 (float):
            inner pipe diameter at inlet [m]

        D2 (float):
            inner pipe diameter of middle section [m]

        nu (float, optional):
            kinematic viscosity [m^2/s]

        eps_rough (float, optional):
            inner pipe roughness [m]

        alphaDeg  (float, optional):
            opening angle (over both sides) [deg]

    Returns:
        (float):
            resistance coefficient  [/]
    Note:
        Use v1 as velocity in pressure drop calculations
    """
    if alphaDeg < 45.:
        x = 2.6 * np.sin(0.5 * radians(alphaDeg))
    else:
        x = 1
    return x * resistanceSquarePipeExpansion(v1, D1, D2, nu, eps_rough)


def dp_in_red_mid_exp_out(v1, D1, L1, D2, L2, D3, L3, nu=1e-6, rho=1e3,
                          eps_rough=10e-6, c0=1., c1=1., c2=1., c3=1.):
    """
    Pressure drop of the combination:
        1) straight pipe ==> 1/2) square reduction ==> 2) thin straight pipe
        ==> 2/3) square expansion ==> 3) straight pipe

    Resistance series:

         k1    k12   k2    k23     k3
    ------------+           +------------
                |           |
         v1     +-----------+
    D1   --->        D2            D3
                +-----------+
                |           |
    ------------+           +------------

    Args:
        v1 (float):
            axial component of velocity at inlet [m/s]

        D1 (float):
            inner pipe diameter at inlet [m]

        L1 (float):
            length of inlet section [m]

        D2 (float):
            inner pipe diameter of middle section [m]

        L2 (float):
            length of middle section [m]

        D3 (float):
            inner pipe diameter at outlet [m]

        L3 (float):
            length of outlet section [m]

        nu (float, optional):
            kinematic viscosity [m^2/s]

        rho (float, optional):
            density [kg/m^3]

        eps_rough (float, optional):
            inner pipe roughness [m]

        c0, c1, c2, c3 (multiple float, optional):
            tuning parameters, see '# tuning' comment in source code below

    Returns:
        (6-tuple of float):
            (dp, dp1, dp12, dp2, dp23, dp3)
            total pressure drop and pressure drops over sections in figure [Pa]
    """
    if np.abs(v1) < 1e-20:
        return 0.

    pars = [v1, D1, L1, D2, L2, D3, L3, nu, rho, eps_rough]
    assert all([isinstance(x, (int, float, bool)) for x in pars])
    assert D1 > D2 and D2 < D3

    v2 = v1 * (D1 / D2)**2
    v3 = v2 * (D2 / D3)**2

    k1 = resistancePipe(v=v1, D=D1, L=L1, nu=nu, eps_rough=eps_rough)
    k12 = resistanceSquarePipeReduction(v1=v1, D1=D1, D2=D2, nu=nu,
                                        eps_rough=eps_rough)
    k2 = resistancePipe(v=v2, D=D2, L=L2, nu=nu, eps_rough=eps_rough)
    k23 = resistanceSquarePipeExpansion(v1=v2, D1=D2, D2=D3, nu=nu,
                                        eps_rough=eps_rough)
    k3 = resistancePipe(v=v3, D=D3, L=L3, nu=nu, eps_rough=eps_rough)

    dp1 = pressureDrop(k1,   v1, rho)
    dp12 = pressureDrop(k12, v1, rho) * (c0)  # tuning
    dp2 = pressureDrop(k2,   v2, rho) * (c1)  # tuning
    dp23 = pressureDrop(k23, v2, rho) * (c2)  # tuning
    dp3 = pressureDrop(k3,   v3, rho)
    dpTotal = (dp1 + dp12 + dp2 + dp23 + dp3) * (c3)  # tuning
    return dpTotal, dp1, dp12, dp2, dp23, dp3


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    import matplotlib.pyplot as plt

    fontsize = 10
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams['legend.fontsize'] = fontsize

    if 0 or ALL:
        s = 'Pressure loss in straight pipe'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        def f():
            rho = 1000
            nu = 1e-6
            D = 50e-3
            L = 1
            eps_rough = 10e-6
            v = 1
            Re = v * D / nu

            k = resistancePipe(v=v, D=D, L=L, nu=nu, eps_rough=eps_rough)
            dp = pressureDrop(k=k, v=v, rho=rho)

            maxKey = max(map(len, locals()))
            for key, val in locals().items():
                if key != 'maxKey':
                    s = '{:>' + str(maxKey + 4) + '}: {}'
                    print(s.format(key, val))
        f()

    if 0 or ALL:
        s = 'Pressure loss in straight->reduct->straight->expansion->straight'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        D1, L1 = 20e-3, 20e-3
        D2, L2 = 5e-3, 200e-3
        D3, L3 = D1, L1
        eps_rough = 10e-6
        nu = 5e-5
        rho = 1000
        rho_seq = [800, 900, 1000, 1100, 1200, 1300, 1400, 1600, 1800, 2000]
        v1 = 1
        v1_seq = [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10]

        print('+++ nu:', nu)

        # dp_set is array of [dp_total, dp1, ..., dp3]
        dp_set = [dp_in_red_mid_exp_out(v1=v1, D1=D1, L1=L1,
                  D2=D2, L2=L2, D3=D3, L3=L3, nu=nu, rho=rho,
                  eps_rough=eps_rough) for v1 in v1_seq]
        dp_set = 1e-6 * np.atleast_2d(dp_set)

        for withoutTotalLoss in [True, False]:
            labels = ['total', 'inlet', 'reduce', 'middle', 'expand', 'outlet']
            for i in range(int(withoutTotalLoss), len(dp_set[0])):
                if labels[i] == 'middle':
                    plt.plot(v1_seq, dp_set[:, i], label=labels[i], ls='--')
                else:
                    plt.plot(v1_seq, dp_set[:, i], label=labels[i])
            plt.xlabel('$v$ [m/s]')
            plt.ylabel(r'$\Delta p$ [MPa]')
            plt.legend(bbox_to_anchor=(0, 1), loc='upper left')
            plt.grid()
            plt.show()

    # DN80/2  -> equivalent pipe diameter: 56.57 mm
    D1, D2, v1 = 40e-3, 20e-3, 1.
    D1, D2, v1, rBend, DN = 56.57e-3, 40e-3, 8.5, 113.5e-3, 80e-3
    D1 = 80e-3
    rho = 1000.
    nu = 1e-6
    eps_rough = 10e-6
    k_functions = [resistanceSquarePipeReduction,
                   resistanceTaperedPipeReduction,
                   resistanceSquarePipeExpansion,
                   resistanceTaperedPipeExpansion]
    if 0 or ALL:
        Re_seq = np.linspace(1e0, 1e4, 10000)
        k = [poiseulleColebrook(Re, D1, eps_rough) for Re in Re_seq]
        plt.plot(Re_seq, k)
        plt.xlabel('Re')
        plt.ylabel('$k_{straight}$ [/]')
        plt.show()

    if 0 or ALL:
        # plot of k(rBend), phiBend=const
        k = resistancePipeBend

        # D1 = 40e-3 ; rBend = 112.5e-3
        x = np.linspace(0.01, 10.0, 100)
        y = [k(v=v, D=D1, rBend=rBend, phiBendDeg=75) for v in x]
        plt.xlabel('$v$')
        plt.ylabel('$k_{bend}$ [/]')
        plt.plot(x, y)
        plt.show()
        x = np.linspace(0.05, 5.0, 1000) * 112.5e-3
        y = [k(v=v1, D=D1, rBend=r, phiBendDeg=75) for r in x]
        plt.plot(x, y)
        plt.xlabel('$r_{bend}$')
        plt.show()

        x = np.linspace(0.0, 90.0, 100)
        y = [k(v=5.0, D=D1, rBend=100e-3, phiBendDeg=phi) for phi in x]
        plt.xlabel(r'$\varphi_{bend}$')
        plt.plot(x, y)
        plt.show()

    if 0 or ALL:
        # plot dp(nu)  for v-sequence
        for v in [0.05, 0.1, 0.2, 1, 10]:
            plt.xlabel(r'$\nu$ [mm$^2$/s]')
            plt.ylabel('$p$ [kPa]')
            nu_seq = np.linspace(1e-7, 1e-3, 1000)
            for k in k_functions:
                print('\n\n***', k.__name__)
                if str(k).find('Expansion') == -1:
                    v1 = v
                else:
                    v1 = v * (D1/D2)**2
                dp1 = np.array([pressureDrop(k(v1=v1, D1=D1, D2=D2, nu=nu,
                                             eps_rough=eps_rough), v1, rho)
                                for nu in nu_seq])
                s = str(k).split(sep=' ')[1][10:]
                plt.title('v_low: '+str(v)+', D1: '+str(D1)+', D2: '+str(D2) +
                          ', eps: '+str(eps_rough)+' v1_expan=v2_reduc')
                plt.plot(nu_seq*1e6, dp1*1e-3, label=s)
            plt.show()

    if 0 or ALL:
        # dp(nu)  for a v-sequence
        for k in k_functions:
            print('\n\n***', k.__name__)
            if 0:
                nu_seq = [x * 1e-7 for x in range(1, int(1e5))]
                dp1 = [pressureDrop(k(v1=v1, D1=D1, D2=D2, nu=nu,
                                      eps_rough=eps_rough), v, rho)
                       for nu in nu_seq]
                x = [x * 1e6 for x in nu_seq]
                y = [y * 1e-3 for y in dp1]
                plt.title('v: '+str(v1))
                plt.xlabel(r'$\nu$ [mm$^2$/s]')
                plt.ylabel('$p$ [kPa]')
                plt.plot(x, y)
                plt.show()

            if 1:
                plt.xlabel('$v$ [m/s]')
                plt.ylabel('$p$ [kPa]')
                v_seq = np.linspace(0.1, 10., 50)
                nu_seq = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
                for nu in nu_seq:
                    dp2 = [pressureDrop(k(v1=v1, D1=D1, D2=D2, nu=nu,
                                          eps_rough=eps_rough), v1, rho)
                           for v1 in v_seq]
                    y = [y * 1e-3 for y in dp2]
                    plt.plot(v_seq, y,
                             label='nu:'+str(round(nu*1e6, 1))+'e-6')
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.show()

            if 0:
                plt.xlabel(r'$Re \cdot 10^{-3}$ [/]')
                plt.ylabel('$p$ [kPa]')
                v1_seq = np.array([.1, .2, .4, .6, .8, 1, 2, 3, 4, 5, 6, 7, 8,
                                   9, 10])
                nu_seq = np.array([1e-7, 1e-6, 1e-5, 1e-4, 1e-3])
                for nu in nu_seq:
                    Re_seq = v1_seq * D1 / nu
                    dp_seq = [pressureDrop(k(v1=v1, D1=D1, D2=D2, nu=nu,
                              eps_rough=eps_rough), v1, rho) for v1 in v1_seq]
                    dp_kPa = 1e-3 * np.array(dp_seq)
                    plt.plot(Re_seq * 1e-3, dp_kPa,
                             label='nu:'+str(round(nu*1e6, 1))+'e-6')
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.show()
