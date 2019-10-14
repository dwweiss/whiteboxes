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
      2019-09-12 DWW

  Reference
      Blevins: Applied fluid dynamics handbook, table 6-5, p. 57
      https://neutrium.net/fluid_flow/
              pressure-drop-from-fittings-expansion-and-reduction-in-pipe-size/
"""

__all__ = ['pressure_drop',
           'poiseulle_colebrook', 'resistance_pipe',
           'resistance_pipe_bend',
           'resistance_square_pipe_expansion', 
           'resistance_square_pipe_reduction',
           'resistance_tapered_pipe_expansion', 
           'resistance_tapered_pipe_reduction',
           'dp_in_red_mid_exp_out', 'dp_tapered_in_red_mid_exp_out']

from math import log10, fabs, sqrt, sin, radians
from scipy.optimize import fsolve
import numpy as np

# upper limit of laminar pipe flow range of Reynolds numbers
REYNOLDS_PIPE_LAMINAR = 2300


def pressure_drop(k, v, rho):
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


def poiseulle_colebrook(Re, D, eps_rough, bi_sectional_search=False):
    """
    Friction factor of straight pipe

    Args:
        Re (float):
            Reynolds number

        D (float):
            inner pipe diameter [m]

        eps_rough (float):
            inner pipe roughness [m]

        bi_sectional_search (bool, optional):
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
        if bi_sectional_search:
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


def resistance_pipe(v, D, L=1.0, nu=1e-6, eps_rough=10e-6):
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
    return L / D * poiseulle_colebrook(Re=v*D/nu, D=D, eps_rough=eps_rough)


def _resistance_moderate_bend(v, D, r_bend, phi_bend_deg, nu, eps_rough):
    """
    Resistance coefficient of moderate pipe bend with: r_bend/D >= 1.8

    Args:
        v (float):
            axial component of velocity at inlet [m/s]

        D (float):
            inner pipe diameter at inlet and outlet [m]

        r_bend (float):
            bending radius [m]

        phi_bend_deg (float):
            bending angle [deg]

        nu (float):
            kinematic viscosity [m^2/s]

        eps_rough (float):
            inner pipe roughness [m]

    Returns:
        (float):
            resistance coefficient  [/]
    """
    ratio = r_bend / D
    assert ratio >= 1.8, 'not moderate bend'

    alpha = 1.0
    if ratio < 50.0:
        if phi_bend_deg <= 45.0:
            alpha = 1.0 + 5.13 * ratio**-1.47
        elif phi_bend_deg <= 90.:
            if ratio < 9.85:
                alpha = 0.95 + 4.42 * ratio**-1.96
        else:
            alpha = 1.0 + 5.06 * ratio**-4.52

    Re = v * D / nu
    if Re / ratio**2 <= 360.:
        fC = 0.336 * (Re * np.sqrt(ratio))**-0.2
        return 0.0175 * alpha * fC * phi_bend_deg * ratio
    else:
        return 0.00431 * alpha * phi_bend_deg * Re**-0.17 * ratio**0.84


def _resistance_sharp_bend(v, D, r_bend, phi_bend_deg, nu, eps_rough):
    """
    Resistance coefficient of sharp pipe bend with: r_bend/DPipe < 1.8

    Args:
        v (float):
            axial component of velocity at inlet [m/s]

        D (float):
            inner pipe diameter at inlet and outlet [m]

        r_bend (float):
            bending radius [m]

        phi_bend_deg (float):
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
    x = r_bend / D         # example: x(D=80mm, r_bend=112.5mm) = 2.81

    if x >= 1.8:
        print("??? function called with x: '" + str(x) + "'")

    if phi_bend_deg < 20.:
        if   x <= 0.5:  K = 0.053
        elif x <= 0.75: K = 0.038
        elif x <= 1.0:  K = 0.035
        elif x <= 1.5:  K = 0.040
        else:           K = 0.045
    elif phi_bend_deg <= 30.:
        if   x <= 0.5:  K = 0.12
        elif x <= 0.75: K = 0.070
        elif x <= 1.0:  K = 0.058
        elif x <= 1.5:  K = 0.060
        else:           K = 0.065
    elif phi_bend_deg <= 45.:
        if   x <= 0.5:  K = 0.27
        elif x <= 0.75: K = 0.14
        elif x <= 1.0:  K = 0.10
        elif x <= 1.5:  K = 0.090
        else:           K = 0.089
    elif phi_bend_deg <= 75.:
        if   x <= 0.5:  K = 0.80
        elif x <= 0.75: K = 0.31
        elif x <= 1.0:  K = 0.20
        elif x <= 1.5:  K = 0.15
        else:           K = 0.14
    elif phi_bend_deg <= 90.:
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


def resistance_pipe_bend(v, D, r_bend, phi_bend_deg, nu=1e-6, eps_rough=10e-6):
    """
    Resistance coefficient of pipe bend

    Args:
        v (float):
            axial component of velocity at inlet [m/s]

        D (float):
            inner pipe diameter at inlet and outlet [m]

        r_bend (float):
            bending radius [m]

        phi_bend_deg (float):
            bending angle [degrees]

        nu (float, optional):
            kinematic viscosity [m^2/s]

        eps_rough (float, optional):
            inner pipe roughness [m]

    Returns:
        (float):
            resistance coefficient  [/]
    """
    if r_bend / D >= 1.8:
        return _resistance_moderate_bend(v, D, r_bend, phi_bend_deg, nu, 
                                         eps_rough)
    else:
        return _resistance_sharp_bend(v, D, r_bend, phi_bend_deg, nu, 
                                      eps_rough)


def resistance_square_pipe_reduction(v1, D1, D2, nu=1e-6, eps_rough=10e-6):
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
        f1 = poiseulle_colebrook(Re=Re1, D=d1, eps_rough=eps_rough)
        x = (d1 / d2)**2
        return (0.6 + 0.48 * f1) * x * (x-1)


def resistance_tapered_pipe_reduction(v1, D1, D2, nu=1e-6, eps_rough=10e-6,
                                      alpha_deg=90.):
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

        alpha_deg (float, optional):
            opening angle (over both sides) [deg]

    Returns:
        (float):
            resistance coefficient  [/]

    Note:
        1) if alpha=90 deg, function returns 0.7071*squarePipeReduction
        2) use v1 for velocity in pressure drop calculations

    """
    x = sin(0.5*radians(alpha_deg))
    if alpha_deg < 45.:
        x *= 1.6
    else:
        x = np.sqrt(x)
    return x * resistance_square_pipe_reduction(v1, D1, D2, nu, eps_rough)


def resistance_square_pipe_expansion(v1, D1, D2, nu=1e-6, eps_rough=10e-6):
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
        f1 = poiseulle_colebrook(Re=Re1, D=d1, eps_rough=eps_rough)
        return (1 + 0.8 * f1) * (1 - (d1 / d2)**2)**2


def resistance_tapered_pipe_expansion(v1, D1, D2, nu=1e-6, eps_rough=10e-6,
                                      alpha_deg=90.):
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

        alpha_deg  (float, optional):
            opening angle (over both sides) [deg]

    Returns:
        (float):
            resistance coefficient  [/]
    Note:
        Use v1 as velocity in pressure drop calculations
    """
    if alpha_deg < 45.:
        x = 2.6 * np.sin(0.5 * radians(alpha_deg))
    else:
        x = 1
    return x * resistance_square_pipe_expansion(v1, D1, D2, nu, eps_rough)


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
    assert D1 > D2 < D3, str((D1, D2, D3))

    v2 = v1 * (D1 / D2)**2
    v3 = v2 * (D2 / D3)**2

    k1 = resistance_pipe(v=v1, D=D1, L=L1, nu=nu, eps_rough=eps_rough)
    k12 = resistance_square_pipe_reduction(v1=v1, D1=D1, D2=D2, nu=nu,
                                        eps_rough=eps_rough)
    k2 = resistance_pipe(v=v2, D=D2, L=L2, nu=nu, eps_rough=eps_rough)
    k23 = resistance_square_pipe_expansion(v1=v2, D1=D2, D2=D3, nu=nu,
                                        eps_rough=eps_rough)
    k3 = resistance_pipe(v=v3, D=D3, L=L3, nu=nu, eps_rough=eps_rough)

    dp1 = pressure_drop(k1,   v1, rho)
    dp12 = pressure_drop(k12, v1, rho) * (c0)  # tuning
    dp2 = pressure_drop(k2,   v2, rho) * (c1)  # tuning
    dp23 = pressure_drop(k23, v2, rho) * (c2)  # tuning
    dp3 = pressure_drop(k3,   v3, rho)
    dpTotal = (dp1 + dp12 + dp2 + dp23 + dp3) * (c3)  # tuning

    return dpTotal, dp1, dp12, dp2, dp23, dp3


def dp_tapered_in_red_mid_exp_out(v1, D1, L1, D2, L2, D3, L3,
                                  alpha12=90., alpha23=90.,
                                  nu=1e-6, rho=1e3, eps_rough=10e-6):
    """
    Pressure drop of the combination:
        1) straight pipe ==> 1/2) tapered pipe reduction
        ==> 2) thin straight pipe ==> 2/3) tapered pipe expansion
        ==> 3) straight pipe

    Resistance series:


         k1       k12          k2         k23             k3
    -----------------+                        +-------------------
                      \                      /
                    /  +--------------------+  \
    --v1->     alpha12           D2            alpha23    D3
    D1              \  +--------------------+  /
                      /                      \
    -----------------+                        +-------------------


    Args:
        v1 (float):
            axial component of velocity at inlet [m/s]

        D1 (float):
            inner pipe diameter at inlet [m]

        L1 (float):
            length of inlet section [m]

        alpha12 (float):
            opening angle (over both sides) [deg]

        D2 (float):
            inner pipe diameter of middle section [m]

        L2 (float):
            length of middle section [m]

        alpha23 (float):
            opening angle (over both sides) [deg]

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

    Returns:
        (6-tuple of float):
            (dp, dp1, dp12, dp2, dp23, dp3)
            total pressure drop and pressure drops over sections in figure [Pa]
    """
    if np.abs(v1) < 1e-20:
        return 0.

    pars = [v1, D1, L1, alpha12, D2, L2, alpha23, D3, L3, nu, rho, eps_rough]
    assert all([isinstance(x, (int, float, bool)) for x in pars])
    assert D1 > D2 and D2 < D3

    v2 = v1 * (D1 / D2)**2
    v3 = v2 * (D2 / D3)**2

    k1 = resistance_pipe(v=v1, D=D1, L=L1, nu=nu, eps_rough=eps_rough)

    k12 = resistance_tapered_pipe_reduction(v1=v1, D1=D1, D2=D2, nu=nu,
                                            eps_rough=eps_rough, 
                                            alpha_deg=alpha12)
    k2 = resistance_pipe(v=v2, D=D2, L=L2, nu=nu, eps_rough=eps_rough)
    k23 = resistance_tapered_pipe_expansion(v1=v2, D1=D2, D2=D3, nu=nu,
                                            eps_rough=eps_rough, 
                                            alpha_deg=alpha23)
    k3 = resistance_pipe(v=v3, D=D3, L=L3, nu=nu, eps_rough=eps_rough)

    dp1 = pressure_drop(k1,   v1, rho)
    dp12 = pressure_drop(k12, v1, rho)
    dp2 = pressure_drop(k2,   v2, rho)
    dp23 = pressure_drop(k23, v2, rho)
    dp3 = pressure_drop(k3,   v3, rho)
    dpTotal = (dp1 + dp12 + dp2 + dp23 + dp3)

    return dpTotal, dp1, dp12, dp2, dp23, dp3
