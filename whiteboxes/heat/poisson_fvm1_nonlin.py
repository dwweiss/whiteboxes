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
      2023-12-04 DWW
"""

import matplotlib.pyplot as plt
from numba import jit
import numpy as np
from typing import Callable, Dict, Iterable, Optional, Tuple, Union

import initialize
initialize.set_path()

from whiteboxes.numerics.tdma import tdma

__all__ = ['poisson_bc1_bc1_fvm1', 'poisson_bc1_bc1_nonlin_fvm1',
           'dqdt_for_bc1_seq']

@jit
def _fvm1_equation_system(i, x_cen, x_vrt, T, conductivity, source,
                          Lo, Di, Up, Rs):
    """
    assembling of matrix [Lo, Di, Up] and right-hand side vector {Rs}

               T_w       T_e
                |         |
                v         v
        -----------------------------
    ... |   +   |    +    |    +    | ...
        -----------------------------
                     ^
                     | T
    """        
    # unknown at cell faces
    T_w = (T[i] + T[i-1]) / 2
    T_e = (T[i+1] + T[i]) / 2
    
    # conductivity at cell faces k_w = k(x_w=x_vrt[i-1], T_w)
    k_w = conductivity(x_vrt[i-1], T_w)
    k_e = conductivity(x_vrt[i], T_e)
    
    Up[i] = -k_e / (x_cen[i+1] - x_cen[i])
    Lo[i] = -k_w / (x_cen[i] - x_cen[i-1])
    Di[i] = - Up[i] - Lo[i]
    if source is None:
        Rs[i] = 0.
    else:
        Rs[i] = (x_vrt[i] - x_vrt[i-1]) * source(x_cen[i], T[i])

    return Lo, Di, Up, Rs


def poisson_bc1_bc1_fvm1(T: np.ndarray | None = None, 
                         **kwargs: Any) -> Tuple[np.array, np.ndarray, float, float] | None:
    """
    Solves Poisson equation with 2 Dirichlet boundary conditions in 1D space
    The conductivity is not dependent solution T
    
        d/dx[k(x) dT/dx] = S(x), 
            domain: [0, L], boundary conditions: T(x=0), T(x=L) 
    
    Returns:
        x (1D array of float): 
            independent variable
        T (1D array of float): 
            dependent variable T(x)
        dTdx_west:
            gradient of T at west boundary dT/dx(x=0)
        dTdx_east:
            gradient of T at east boundary dT/dx(x=L)
                
        0    1        2                n_vol  n_vol+1 <-- cell index
       ---------------------- ... --------------
       |+|   +   |    +    |       |    +    |+|
       ---------------------- ... --------------
        :                                     :
        :<------------- L --- ... ---------- >:            
    """
    precompiled_code = not True  # chose this option for employing jit

    conductivity: Callable[[float], float] = kwargs.get('conductivity', None) 
    L: float = kwargs.get('L', 1.) 
    n_vol: int = kwargs.get('n_vol', 50)
    source: Callable[[float], float] = kwargs.get('source', None)
    T_west: float = kwargs.get('T_west', 0.)
    T_east: float = kwargs.get('T_east', 1.)
    
    if conductivity is None:
        conductivity = lambda x, T: 1.    
    if T is not None:
        n_vol = len(T) - 1
    if n_vol < 3:
        return None
    
    # mesh generation, cells with index 0 and n_vol+1 are ghostcells
    # with a reduced width of Dx/2
    Dx = L / n_vol
    x_cen = np.arange(-Dx/2, L + Dx/2, Dx)
    x_cen[0], x_cen[-1] = 0., L
    x_vrt = x_cen + Dx / 2
    x_vrt[0], x_vrt[-1] = x_cen[0], x_cen[-1]


    if T is None:
        T = np.linspace(T_west, T_east, x_cen.size)

    Lo, Di = np.zeros(x_cen.size), np.zeros(x_cen.size)
    Up, Rs = np.zeros(x_cen.size), np.zeros(x_cen.size)

    for i in range(1, x_cen.size-1):
        """
        assembling of matrix [Lo, Di, Up] and right-hand side vector {Rs}

                   T_w       T_e
                    |         |
                    v         v
            -----------------------------
        ... |   +   |    +    |    +    | ...
            -----------------------------
                         ^
                         | T
        """        
        if precompiled_code:
            Lo, Di, Up, Rs = _fvm1_equation_system(i, x_cen, x_vrt, T, 
                conductivity, source, Lo, Di, Up, Rs)
        else:
            # unknown at cell faces
            T_w = (T[i] + T[i-1]) / 2
            T_e = (T[i+1] + T[i]) / 2
            
            # conductivity at cell faces k_w = k(x_w=x_vrt[i-1], T_w)
            k_w = conductivity(x_vrt[i-1], T_w)
            k_e = conductivity(x_vrt[i], T_e)
            
            Up[i] = -k_e / (x_cen[i+1] - x_cen[i])
            Lo[i] = -k_w / (x_cen[i] - x_cen[i-1])
            Di[i] = - Up[i] - Lo[i]
            if source is None:
                Rs[i] = 0.
            else:
                Rs[i] = (x_vrt[i] - x_vrt[i-1]) * source(x_cen[i], T[i])

    # Dirichlet condition at west boundary of domain
    # T_0 * 1 + 0 * T_1 = T_0
    Di[0] = 1.
    Up[0] = 0.
    Rs[0] = T_west

    # Dirichlet condition at east boundary of domain
    # T_{n_vol} * 0 + T_{n_vol+1} * 1 = T_{n_vol+1}
    Lo[-1] = 0.
    Di[-1] = 1.
    Rs[-1] = T_east

    T = tdma(Lo, Di, Up, Rs)
    
    # temperature gradient at boundaries
    dTdx_west = (T[1] - T[0]) / (x_cen[1] - x_cen[0])
    dTdx_east = (T[-1] - T[-2]) / (x_cen[-1] - x_cen[-2])

    return np.asfarray(x_cen), np.asfarray(T), dTdx_west, dTdx_east


def poisson_bc1_bc1_nonlin_fvm1(T: np.ndarray | None = None, **kwargs: Any
) -> Dict[str, float | np.ndarray] | None:
    """
    Solves Poisson equation with 2 Dirichlet boundary conditions in 
    steady state and in 1D space
    The conductivity k can be dependent on the solution: k = k(x, T(x))
    
        d/dx[k(x, T) dT/dx] = S(x, T), 
            domain: [0, L], 
            boundary conditions: T(x=0)=T_w, T(x=L)=T_e 

    Kwargs:
        conductivity (Callable[[float, float], float]):

        L (float):
            length of physical domain
        max_it (int):
            maximum number of iterations
        min_it (int):
            minimum number of iterations        
        mse (float):
            stop iteration, if mean square difference less than 'mse'
        omega (float):
            under-relaxation
        source (callable):
            right-hand side source term
        conductivity (callable):
            conductivity function, e.g. k = k_ref + dk/dT * (T - T_ref) 
            
    Returns:
        Dictionary:
            'x' (1D array of float): 
                independent variable
            'T' (1D array of float): 
                dependent variable T(x)
                
            'dTdx_west' (float):
                gradient of T at west boundary dT/dx(x=0)
            'dTdx_east' (float):
                gradient of T at east boundary dT/dx(x=L)
                
            'dqdt_west' (float):
                flux at west boundary: -k(T(x=0)) * (-1) * dT/dx(x=0)
            'dqdt_east' (float):
                flux at east boundary: -k(T(x=L)) * (+1) * dT/dx(x=L)
                
            'hist_mse':
                history of mean-square difference between previous 
                and current result 
            'hist_dTdx_west ':
                history of temperature gradient at west boundary 
            'hist_dTdx_east ':
                history of temperature gradient at east boundary 
    """
    conductivity: Callable[[float], float] = kwargs.get('conductivity',
                                                      lambda x, T: 1 + T * 0.1) 
    L: int = kwargs.get('L', 1.)
    max_it: int = kwargs.get('max_it', 50)
    min_it: int = kwargs.get('min_it', 3)
    mse: float = kwargs.get('mse', 1e-4)
    omega = kwargs.get('omega', 1.0)
    
    result = {}
    result['hist_mse'] = []
    result['hist_dTdx_west'] = []
    result['hist_dTdx_east'] = []

    T_prv = None    
    for it in range(max_it):
        if T_prv is None:
            T_prv = T
        else:
            T_prv = T_prv * (1 - omega) + T * omega
        res = poisson_bc1_bc1_fvm1(T=T_prv, **kwargs)
        if res is None:
            return None
        
        x, T, dTdx_west, dTdx_east = res
        
        if T_prv is not None:
            mse_ = np.mean(np.square(T - T_prv))
            
            result['hist_mse'].append(mse_)
            result['hist_dTdx_west'].append(dTdx_west)
            result['hist_dTdx_east'].append(dTdx_east)
            
            if mse_ < mse and it > min_it:
                break
            
    n_w, n_e = -1, +1  # outward pointing normal at west and east boundary

    result['T'] = T
    result['x'] = x
    result['it'] = it
    result['dTdx_west'] = dTdx_west
    result['dTdx_east'] = dTdx_east
    result['dqdt_west'] = n_w * dTdx_west * conductivity(x=0, T=T[0])
    result['dqdt_east'] = n_e * dTdx_east * conductivity(x=L, T=T[-1])
        
    return result


def dqdt_for_bc1_seq(k_coeff: Iterable[float] | None = None, 
                     T_west: float | Iterable[float] = 0.,
                     T_east: float | Iterable[float] = 1., 
                     T_ref: float | None = 0.,
                     L: float = 1.0, 
                     n_vol: int = 1000,
                     mse: float = 1e-3,
                     plot_scale: Tuple[Tuple[float, str], 
                                       Tuple[float, str]] | None = None,
                     silent: bool = True,
                     ) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solves the Poisson equation for 
        a sequence 'T_west' of boundary conditions of first kind and 
        a sequence 'T_east' of boundary conditions of first kind
    
    Calculates the heat flux density dq/dt at west and east boundary 
    for all T_west/T_east combinations 
    
    The conductivity is defined as the polynomium
    
        k(T) = k0 + k1*(T-T_ref) + k2*(T-T_ref)^2  + k3*(T-T_ref)^3  
                                                   + k4*(T-T_ref)^4
    
    Plots solutions for all T_west/T_east combinations in one figure
        
    Args:
        k_coeff
            array containing reference thermal conductivity and 
            derivative(s) of conductivity with respect to temperature;
            length of k_coeff defines the degree of the polynomium
        T_west
            sequence of temperatures at west boundary
        T_east
            sequence of temperatures at east boundary
        T_ref:
            reference temperature for conductivity calculation;
            If T_ref is None, then min(T_west, T_east) will be used
        L
            length
        n_vol
            number of finite volumes
        plot_scale:
            Pair of (scale, unit) pairs for axis labelling and scaling
        silent:
            if False, then plot sequence of iterative solutions
        
    Returns:
        dqdt_west:
            sequence of heat flux densities at west boundary for all 
            combinations of T_west (outer loop) and T_east (inner loop)        
        dqdt_east:
            sequence of heat flux densities at east boundary for all 
            combinations of T_west (outer loop) and T_east (inner loop)        
    """
    if plot_scale is None:
        plot_scale = ((1e0, 'm'), (1., 'K'))
        
    T_west, T_east = np.atleast_1d(T_west), np.atleast_1d(T_east)
    
    if T_ref is None:
        T_ref = np.min([T_west.min(), T_east.min()])
        
    if k_coeff is None:
        k_coeff = (1., 0.)
    k_coeff = np.atleast_1d(k_coeff)

    def conductivity(x, T):
        n = len(k_coeff)
        dT = T - T_ref
        sqr_dT = dT * dT
        
        c = 0.
        if n > 0:
            c += k_coeff[0]
        if n > 1:
            c += k_coeff[1] * dT
        if n > 2:
            c += k_coeff[2] * sqr_dT
        if n > 3:
            c += k_coeff[3] * dT * sqr_dT
        if n > 4:
            c += k_coeff[4] * sqr_dT * sqr_dT
            
        return c
    
    dqdt_west, dqdt_east = [], []
    for T_west_i in T_west:
        for T_east_i in T_east:
            res = poisson_bc1_bc1_nonlin_fvm1(
                T=None, 
                L=L, 
                n_vol=n_vol, 
                T_west=T_west_i, 
                T_east=T_east_i, 
                conductivity=conductivity, 
                source=None,
                mse=mse,
                silent=silent)
            dqdt_west.append(res['dqdt_west'])
            dqdt_east.append(res['dqdt_east'])
            
            if not silent: 
                plt.plot(res['x'] * plot_scale[0][0], 
                         res['T'] * plot_scale[1][0], label='T_w/T_e: ' 
                         + str((T_west_i, T_east_i)) + r'  $\dot q:$' 
                         + str((int(res['dqdt_west']), int(res['dqdt_east']))))
        if not silent:
            plt.xlabel('x [' + plot_scale[0][1] + ']')
            plt.ylabel('T [' + plot_scale[1][1] + ']')
            plt.legend(); plt.grid(); plt.show()

    return np.asfarray(dqdt_west), np.asfarray(dqdt_east)


dqdt_for_bc1_seq()
