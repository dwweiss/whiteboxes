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
      2019-09-27 DWW
"""

import __init__
__init__.init_path()

import unittest
import os

from coloredlids.heat.free_convection import FreeConvectionPlate
from coloredlids.matter.gases import Air
from coloredlids.matter.generic import C2K


class TestUM(unittest.TestCase):
    def setUp(self):
        print('///', os.path.basename(__file__))

    def tearDown(self):
        pass

    def test1(self):

        def main():
            T_surf = C2K(40)      # [K]
            T_inf = C2K(20)       # [K]
            phi_plate = 90.       # [deg], 90=vertical plate
            L = 0.1
        
            foo = FreeConvectionPlate(fluid=Air(), eps_rad=0.5)
            alpha_conv = foo.alpha_conv(T_surf=T_surf, T_inf=T_inf, L=L,
                                        phi_plate=phi_plate)
            alpha_rad = foo.alpha_rad(T_surf=T_surf, T_inf=T_inf)
            alpha_comb = foo.alpha_combined(T_surf=T_surf, T_inf=T_inf, L=L,
                                            phi_plate=phi_plate)
        
            # print local variables
            for key in sorted(locals(), key=lambda s: s.lower()):
                if key not in ('foo', 'kwargs'):
                    x = locals()[key]
                    if isinstance(x, float) and abs(x) > 0.1:
                        x = round(x, 3)
                    print('{:>15}: {}'.format(key, x))
                
        main()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
