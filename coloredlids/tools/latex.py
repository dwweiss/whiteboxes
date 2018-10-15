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
      2018-10-15 DWW
"""

from typing import Optional


def to_latex(x: str) -> str:
    """
    Converts symbol in string to a Latex formatted string. Intended for
    titles and axis labels in plots.

    Args:
        x:
            raw text

    Returns:
        valid Latex string

    Note:
        sniplet for generation of Mx..Fz part of dict:
        for l in ['', 'A', 'B', 'C', 'D']:
            for v in ['F', 'M']:
                for a in ['x', 'y', 'z']:
                    s = "r'$\hat " + v + '_{' + a + '}$'
                    if l:
                        s += ' (' + l + ')'
                    print("               '" + v + a + l + "': " + s + "',")
    """
    dict = {'alpha': r'$\alpha$',
             'beta': r'$\beta$',
            'gamma': r'$\gamma$',
            'Delta': r'$\Delta$',
            'delta': r'$\delta$',
          'epsilon': r'$\epsilon$',
              'phi': r'$\phi$',
              'rho': r'$\varrho$',
            'sigma': r'$\sigma$',
            'Sigma': r'$\Sigma$',
              'tau': r'$\tau$',
               'xi': r'$\xsi$',
              'xsi': r'$\xsi$',
             'zeta': r'$\zeta$',
              'eta':  'eta',  # 'eta' is sub-string of 'beta' and 'zeta'
               '==':  '=',
               '!=': r'$\ne$',
               '<>': r'$\ne$',
               '>=': r'$\ge$',
               '<=': r'$\le$',
        '[degrees]': r'[$\degree$]',
         '[degree]': r'[$\degree$]',
            '[deg]': r'[$\degree$]',
          '[deg C]': r'[$\degree C$]',
           '[degC]': r'[$\degree C$]',
          '[deg F]': r'[$\degree F$]',
           '[degF]': r'[$\degree F$]',
               'Df':  r'$\Delta f$',
               'Dm':  r'$\Delta m$',
               'Dx':  r'$\Delta x$',
               'Dy':  r'$\Delta y$',
               'Dz':  r'$\Delta z$',

               'Fx': r'$\hat F_{x}$',
               'Fy': r'$\hat F_{y}$',
               'Fz': r'$\hat F_{z}$',
               'Mx': r'$\hat M_{x}$',
               'My': r'$\hat M_{y}$',
               'Mz': r'$\hat M_{z}$',
               'FxA': r'$\hat F_{x}$ (A)',
               'FyA': r'$\hat F_{y}$ (A)',
               'FzA': r'$\hat F_{z}$ (A)',
               'MxA': r'$\hat M_{x}$ (A)',
               'MyA': r'$\hat M_{y}$ (A)',
               'MzA': r'$\hat M_{z}$ (A)',
               'FxB': r'$\hat F_{x}$ (B)',
               'FyB': r'$\hat F_{y}$ (B)',
               'FzB': r'$\hat F_{z}$ (B)',
               'MxB': r'$\hat M_{x}$ (B)',
               'MyB': r'$\hat M_{y}$ (B)',
               'MzB': r'$\hat M_{z}$ (B)',
               'FxC': r'$\hat F_{x}$ (C)',
               'FyC': r'$\hat F_{y}$ (C)',
               'FzC': r'$\hat F_{z}$ (C)',
               'MxC': r'$\hat M_{x}$ (C)',
               'MyC': r'$\hat M_{y}$ (C)',
               'MzC': r'$\hat M_{z}$ (C)',
               'FxD': r'$\hat F_{x}$ (D)',
               'FyD': r'$\hat F_{y}$ (D)',
               'FzD': r'$\hat F_{z}$ (D)',
               'MxD': r'$\hat M_{x}$ (D)',
               'MyD': r'$\hat M_{y}$ (D)',
               'MzD': r'$\hat M_{z}$ (D)',

             'dot m': r'[$\dot m$]',
             'dot_m': r'[$\dot m$]',
             'dot V': r'[$\dot V$]',
              'dotV': r'[$\dot V$]',
             'dot_V': r'[$\dot V$]',
                 't': 't',  # 't' is sub-string of eta' and 'tau'
            }

    str(x)
    if x in dict:
        # x equals dictionary entry
        x = dict[x]
        x = x.replace('_{x}', '_{X}')
        x = x.replace('_{y}', '_{Y}')
        x = x.replace('_{z}', '_{Z}')
        return x
    else:
        # x contains dictionary entry
        for key, val in dict.items():
            if key in x:
                x = x.replace(key, val)
                x = x.replace('_{x}', '_{X}')
                x = x.replace('_{y}', '_{Y}')
                x = x.replace('_{z}', '_{Z}')
            break
        return x


def from_latex(x: str) -> str:
    """
    Strips Latex formatting from string

    Args:
        x:
            Latex string

    Returns:
        string without Latex formatting
    """
    x = str(x)
    return x.translate({ord(c): None for c in r'\${}'})


def guess_unit(x: Optional[str]=None) -> str:
    """
    Guesses measurement unit from given Latex formatted string

    Args:
        x:
            Latex string

    Returns:
        unit
    """
    x = from_latex(x)
    if not x:
        return '[/]'
    elif any(x.startswith(a) for a in
             ['alpha', 'alfa', 'beta', 'gamma', 'delta', 'phi', 'psi']):
        return to_latex('[deg]')
    elif x in ['t', 'w', 'h', 'l', 'Dx', 'Dy', 'Dz',
               'Delta x', 'Delta y', 'Delta z',
               'Delta_x', 'Delta_y', 'Delta_z']:
        return '[mm]'
    elif any(x.startswith(a) for a in ['F']):
        return '[kN]'
    elif any(x.startswith(a) for a in ['hat F', 'hat_F']):
        return '[kN/m]'
    elif any(x.startswith(a) for a in ['f', 'Df', 'Delta f', 'Delta_f']):
        return '[Hz]'
    elif any(x.startswith(a) for a in ['M']):
        return '[kNm]'
    elif any(x.startswith(a) for a in ['hat M', 'hat_M']):
        return '[kN]'
    elif any(x.startswith(a) for a in ['m', 'Dm', 'Delta m', 'Delta_m']):
        return '[kg]'
    elif any(x.startswith(a) for a in ['dot m', 'dot_m']):
        return '[kg/s]'
    elif any(x.startswith(a) for a in ['V']):
        return '[m$^3$]'
    elif any(x.startswith(a) for a in ['dot V', 'dot_V']):
        return '[m$^3$/s]'
    elif x in ['varrho', 'rho']:
        return '[kg/m$^3$]'
    elif any(x.startswith(a) for a in ['v']):
        return '[m/s]'
    elif any(x.startswith(a) for a in ['A']):
        return '[m$^2$]'
    elif any(x.startswith(a) for a in ['T', 'theta']):
        return '[$\degree$]'
    elif any(x.startswith(a) for a in ['U', 'u']):
        return '[mm]'
    else:
        print("!!! no guess of unit of x: '" + x + "'")
        return ''


def guess_scale(x: str) -> str:
    """
    Guess unit-prefixes (scale) of symbols in a Latex string

    Args:
        x:
            Latex string containing a symbol

    Returns:
        guess of unit
    """
    x = from_latex(x)
    if x == '[um]':
        return 1e6
    elif x == '[mm]':
        return 1e3
    elif x == '[km]':
        return 1e-3
    elif x == '[m]':
        return 1.
    elif x.startswith('[mN'):
        return 1e-3
    elif x.startswith('[N'):
        return 1.
    elif x.startswith('[kN'):
        return 1e-3
    elif x.startswith('[MN'):
        return 1e-6
    elif x.startswith('[GN'):
        return 1e-9
    elif x == '[mPa]':
        return 1e3
    elif x == '[Pa]':
        return 1.
    elif x == '[kPa]':
        return 1e-3
    elif x == '[MPa]':
        return 1e-6
    elif x == '[GPa]':
        return 1e-9
    elif x == '[Hz]':
        return 1.
    elif x.startswith('[deg'):
        return 1.
    else:
        print("!!! no guess of scale of x: '" + x + "'")
    return 1.
