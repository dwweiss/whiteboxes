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
      2021-11-10 DWW
"""

from collections import OrderedDict
import numpy as np
from typing import Dict, Optional

try:
    from conversion import atm
    from matter import Gas
    from mixformulas import mix_mason, mix_mass, mix_mole
except:
    from coloredlids.property.conversion import atm
    from coloredlids.property.matter import Gas
    from coloredlids.property.mixformulas import mix_mason, mix_mass, mix_mole


class GasMix(Gas):
    """
    Physical and chemical properties of gas mixture
            
    Mass fraction related properties:
        h, c_p
        
    Volumetric or mole fraction related properties: 
        rho, M, mu
        lambda
        ==> ideal gas: volumetric fraction equals mole fraction

    Units:
        M [kg/kmol]  molar mass
        m [kg]       mass
        N [kmol]     amount of substance [mol=6.022e23]
        V [m3]       volume
        v [m3/kg]    specific volume (inverse of density)
        y [mol/mol]  mole fraction N_i/N (ideal gas: equals V_i/V)
        Y [kg/kg]    mass fraction

    Mole fraction or volumetric fraction y_i if ideal gas 
    (in [kmol/kmol] or %vol):
        N = m / M
        y_i = N_i / N_tot = V_i / V_tot = p_i / p_tot
              N_i / N_tot = (m_i/M_i) / (m_tot/M_tot)
        y_i = m_i / m_tot * M_tot / M_i
        
        M_tot = sum_i { M_i * y_i }
        p_i = y_i * p_tot
        rho_tot = sum_i { rho_i(p_i) * y_i }
    
    Mass fraction Y_i ([kg/kg] or %mass):
        Y_i = m_i / m_tot 
              m_i / m_tot = y_i / (M_tot / M_i)  
        Y_i = y_i * M_i / M_tot
    
        M_tot = sum_j { M_j * y_j }
        Y_i = y_i * M_i / M_tot
        
    Example:
        c_p is related to mass fraction Y_i = m_i / m_tot,
        mass fraction is mole fraction y_i times molar mass fraction 

            c_p = sum_i {cp_i * Y_i} 
                = sum_i {cp_i * y_i * M_i / M_tot}
            
        heat capacity of humid air = dry air + water vapor:

            c_p = c_air * m_air/m_tot         + c_vap * m_vap/m_tot
                = c_air * y_air * M_air/M_tot + c_vap * y_vap * M_vap/M_tot

        k is related to mole fraction y_i = N_i / N_tot,
        mole fraction equals volumetric fraction V_i/V_tot if ideal gas 

            k = sum_i {k_i * y_i} 
            
        thermal conductivity of humid air = dry air + water vapor:

            k = k_air * V_air/V_tot + k_vap * V_vap/V_tot
              = k_air * N_air/N_tot + k_vap * N_vap/N_tot
              = k_air * y_air       + k_vap * y_vap

    Note:
        mole fraction y_i=N_i/N of ideal gas component equals its
        volumetric fraction V_i/V and its partial pressure fraction p_i/p:

            y_i = N_i/N_tot = p_i/p_tot = V_i/V_tot,   i=1..n_components
            
        mass fraction is:
            m = N * M -> N = m/M -> N_i/N = (m_i/M_i) / (m_tot/M_tot)
            M_tot = sum_i {y_i * M_i} [kmol/kmol] * [kmol]
    """

    def __init__(self, identifier: str = 'gas_mix',
                 latex: Optional[str] = None,
                 comment: Optional[str] = None) -> None:
        """
        Args:
            identifier:
                Identifier of matter

            latex:
                Latex-version of identifier. If None, identical with identifier

            comment:
                Comment on matter

        Note:
            Do NOT define a self.__call__() method in this class
        """
        super().__init__(identifier=identifier, latex=latex, comment=comment)

        self.components: Dict[Gas, float] = OrderedDict()
        
        self.c_p.calc = self._c_p
        self.k.calc = self._k
        self.mu.calc = self._mu
        self.rho.calc = self._rho
        
        self._k_mix_formula: str = 'mason'   # ['mason', 'mole']
        
    def add(self, component: Gas, mole_frac: float) -> bool:
        """
        Args:
            component:
                object or instance of child class of Gas
                
            mole_frac:
                mole fraction of component [mol/mol]

        Returns:
            False if component is False
        """
        if component is None:
            return False
        
        if not isinstance(component, Gas):
            component = component()
        self.components[component] = mole_frac

        M = 0.
        for gas, mole_frac in self.components.items():
            M += mole_frac * gas.M()
        self.M.calc = lambda T, p, x: M

        return True

    def check(self, silent: bool = False) -> bool:
        if len(self.components.items()) == 0:
            return False
        
        sum_mole_frac = 0.
        for mole_frac in self.components.values():
            sum_mole_frac += mole_frac
        ok = np.isclose(sum_mole_frac, 1.)
        if not ok and not silent:
            print('!!! sum of mole fractions is not 1.0, ', sum_mole_frac, 
                  self.components.values())
        return ok

    def _c_p(self, T: float, p: float = atm(), x: float = 0.) -> float:
        y_all, M_all, c_p_all = [], [], []

        for gas, mole_frac in self.components.items():
            if mole_frac < 1e-8:
                continue
            p_partial = mole_frac * p
            
            y_all.append(mole_frac) 
            M_all.append(gas.M(T, p, x)) 
            c_p_all.append(gas.c_p(T, p_partial))
            
        return mix_mass(y=y_all, M=M_all, property_=c_p_all)

    def _k(self, T: float, p: float = atm(), x: float = 0.) -> float:
        y_all, M_all, k_all, mu_all = [], [], [], []

        for gas, mole_frac in self.components.items():
            if mole_frac < 1e-8:
                continue
            p_partial = mole_frac * p
            
            y_all.append(mole_frac) 
            M_all.append(gas.M(T, p, x)) 
            k_all.append(gas.k(T, p_partial, x)) 
            mu_all.append(gas.mu(T, p_partial, x))

        if self._k_mix_formula.startswith('mas'):
            k = mix_mason(y=y_all, M=M_all, k=k_all, mu=mu_all)
        else:
            k = mix_mole(y=y_all, M=M_all, property_=k_all)
            
        return k

    def _mu(self, T: float, p: float = atm(), x: float = 0.) -> float:
        y_all, M_all, mu_all = [], [], []

        for gas, mole_frac in self.components.items():
            if mole_frac < 1e-8:
                continue
            p_partial = mole_frac * p
            
            y_all.append(mole_frac)
            M_all.append(gas.M(T, p, x)) 
            mu_all.append(gas.mu(T, p_partial, x))
            
        return mix_mole(y=y_all, M=M_all, property_=mu_all)

    def _rho(self, T: float, p: float = atm(), x: float = 0.) -> float:
        rho = 0.
        for gas, mole_frac in self.components.items():
            if mole_frac < 1e-8:
                continue
            p_partial = mole_frac * p
            
            rho_i = gas.rho(T, p_partial, x)
            if rho_i is None:
                return None
            
            rho += mole_frac * rho_i 
            
        return rho
