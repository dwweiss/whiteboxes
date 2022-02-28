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
      2018-07-14 DWW
"""

__all__ = ['mix_mole', 'mix_mass', 'mix_mason']


import numpy as np
from typing import Iterable, Optional


"""
    Properties of gas mixtures:    
        mass related property: 
            c_p = c_p1 * Y1 + c_p2 * Y2

        mole related property: 
            lambda = lambda1 * y1 + lambda2 * y2
    
    Generalization for multi-components mixture
        y_i is mole fraction of component i
        Y_i is mass fraction of component i
        p_i is partial pressure of component i
        
        M = sum_j { y_j * M_j }     
        Y_i = y_i * M_i / M         
    
        c_p = sum_i { c_p_i(T,p_i) * Y_i }
            = sum_i { c_p_i(T,p_i) * y_i * M[i] / sum_j {y_j * M_j} }
        k   = sum_i { k_i(T,p_i) * y_i] }
        rho = sum_i { rho_i(T,p_i) * y_i }

    Example of binary mixture:

        Mixture of 4 mol H2 with 1 mol O2:
            M1 = 2 g/mol
            M2 = 32 g/mol
            N1 = 4 mol
            N2 = 1 mol
            N = 4 mol + 1 mol = 5 mol
        
        mole fractions y_i:
            y1 = N1/N = 4 mol/5 mol = 0.8 mol/mol
            y2 = N2/N = 1 mol/5 mol = 0.2 mol/mol
        
        total molar mass M:
            M = M1 * y1 + M2 * y2 = 2 g/mol * 0.8 + 32 g/mol * 0.2 = 8 g/mol
        
        total mass m:
            m1 = N1 * M1 = 4 mol *  2 g/mol = 8 g
            m2 = N2 * M2 = 1 mol * 32 g/mol = 32 g
            m = m1 + m2 = 40 g
        
        mass fractions Y_i:
            Y1 = m1/m =  8g / 40g = 0.2 g/g
            Y2 = m2/m = 32g / 40g = 0.8 g/g
        
        double check:
            Y1 = y1 * M1/M = 0.8 mol/mol *  2 g/mol / 8 g/mol = 0.2 g/g
            Y2 = y2 * M2/M = 0.2 mol/mol * 32 g/mol / 8 g/mol = 0.8 g/g

            Y1 = m1/m = N1*M1 / (N*M) = 4mol* 2g/mol / (5mol*8g/mol) = 0.2 g/g
            Y2 = m2/m = N2*M2 / (N*M) = 1mol*32g/mol / (5mol*8g/mol) = 0.8 g/g
"""


def mix_mole(y: Iterable[float],
             M: Iterable[float],
             property_: Iterable[float]) -> float:
    """
    Calculates property of a mixture based on mole fractions of 
    mixture components. 
    
        phi = sum_i {phi_i * y_i}
    
    Args:
        y:
            mole fractions of components (equals volumetric fractions 
            if ideal gas) [kmol/kmol]

        M:
            molar masses of components [kmol/kg]

        property_:
            physical or chemical property of mixture components
    
    Returns:
        property of mixture [unit of 'property_']
        
    Note:
        mole fraction N_i/N of ideal gas component equals its volumetric 
        fraction V_i/V and its partial pressure fraction p_i/p:

            y_i = N_i/N = p_i/p = V_i/V,   i=1..n_components
            
    Literature:
        https://www.google.dk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiFsdHTueHtAhUE6OAKHbJiDaYQFjACegQIAhAC&url=https%3A%2F%2Forbit.dtu.dk%2Ffiles%2F117984374%2FPL11b.pdf&usg=AOvVaw3RkR9HkVxRVFELaoby3Hi5
        https://www.researchgate.net/publication/257571187_Thermal_Conductivity_of_Humid_Air
    """
    assert len(y) == len(M) == len(property_), f'{y=}, {M=}, {property_=}'

    mole_fractions = np.asfarray(y)
    properties = np.asfarray(property_) 
    return np.sum(mole_fractions * properties)


def mix_mass(y: Iterable[float],
             M: Iterable[float],
             property_: Iterable[float],
             silent: bool = False) -> float:
    """
    Calculates mass fractions Y_i from mole fractions y_i and estimates 
    property of a mixture based on mixture components. 
    
        M = sum_j { y_j * M_j } 
        phi = sum_i { phi_i * y_i * M_i / M }

    Args:
        y:
            mole fractions (equals volumetric fractions if ideal gas) 
            of components [kmol/kmol]

        M:
            molar masses of components [kmol/kg]

        property_:
            physical or chemical property of mixture components

        silent:
            if False, then print information
    
    Returns:
        property of mixture in [unit('property_')]
        
    Note:
        mole fraction y_i = N_i/N of an ideal gas component in an ideal 
        gas mixture equals its volumetric fraction V_i/V and its 
        partial pressure fraction p_i/p (Y is the mass fraction): 

            Y[i] = m_i / m = N_i*M_i / (N*M) 
                 = N_i/N * M_i/M = y_i * M_i / M
                                            with: M = sum_j { y_j * M_j }
            Y_i = y_i * M_i / M             
    """
    assert len(y) == len(M) == len(property_), f'{y=}, {M=}, {property_=}'

    mole_fractions, M = np.asfarray(y), np.asfarray(M)
    properties = np.asfarray(property_)
    
    M_total = np.sum(M * mole_fractions)
    mass_fractions = mole_fractions * M / M_total
    return np.sum(properties * mass_fractions)


def mix_mason(y: Iterable[float],
              M: Iterable[float], 
              k: Iterable[float], 
              mu: Optional[Iterable[float]],
              silent: bool = False) -> float:
    """
    Calculates thermal conductivity of gas mixture with equation by 
    Mason & Saxena
    
    Args:
        y:
            mole fractions of components [kmol/kmol]
            
        M:
            molar masses of components [kmol/kg]
            
        k:
            thermal conductivity of components [W/m/K]
            
        mu:
            dynamic viscosity of components [Pa s]
            OR 
            None if ratio of viscosities is unknown
    
    Returns:
        thermal conductivity of mixture [W/m/K]

    Note:
        y_i = p_i/p_tot = V_i/V_tot, i=1..n_components
    """    
    assert len(y) == len(M) == len(k), f'{y=}, {M=}, {k=}'
    assert mu is None or len(y) == len(mu), f'{y=}, {mu=}'
    
    if None in list(k):
        return None
        
    c0 = 1.065  # TODO check correction for polyatomic gases: 1.065
    
    def G(M1: float, M2: float, mu1: float, mu2: float) -> float:
        try:
            M12 = M1 / M2
        except:
            if not silent:
                print('??? M1 M2', M1, M2, ' ==> correct to: M1/M2 = 1')
            M12 = 1.
        try:
            mu12 = mu1 / mu2
        except:
            if not silent:
                print('??? {mu1=}, {mu2=}, correct to: mu1/mu2 = 1')
            mu12 = 1.

        return c0 / (2. * np.sqrt(2)) / np.sqrt(1. + M12) \
            * (1. + np.sqrt(mu12 / M12) * M12**0.25)**2
            
    k_mix = 0.
    for i in range(len(y)):
        denom = 1.
        for j in range(len(y)):
            if i != j: 
                if mu is not None:
                    a = G(M[i], M[j], mu[i], mu[j])
                else:
                    a = 1.
                    if not silent:
                        print('!!! mu is None')

                try:
                    b = y[j] / y[i]
                except:
                    b = 1e20
                    if not silent:
                        print('!!! y/y is 0.')
                denom += a * b
        k_mix += k[i] / denom
    return k_mix
