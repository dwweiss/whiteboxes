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
      2019-11-27 DWW
"""

import __init__
__init__.init_path()

import unittest
import numpy as np
import matplotlib.pyplot as plt

from coloredlids.property.parameter import Parameter, Range
from coloredlids.property.conversion import deg2rad, rad2deg


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test1(self):
        x1 = 90
        y = deg2rad(x1)
        print('deg2rad(90):', y)
        x2 = rad2deg(np.pi*0.5)
        print('rad2deg(pi*0.5):', x2)

        self.assertTrue(np.isclose(x1, x2))


    def test2(self):
        print('*** test: Parameter.__getitem__()')
        
        foo = Parameter(identifier='rho_liq', 
                        latex=r'$\varrho_{liq}$',
                        unit='kg/m3', 
                        range_keys=['expected'])
        print('foo:', foo)
        print('-' * 40)

        print('+++ val (not a member of self._ranges)')
        for val_ in (1e-1, [1.2, 3.4, 5.6]):
            foo.val = val_
            print('    val:', val_, foo.val, foo['val'])
            
            self.assertEqual(foo.val, val_)
            self.assertEqual(foo.val, foo['val'])
            # ! 'value' is an unknown key
            self.assertNotEqual(foo.val, foo['???'])
            # ! self.val is NOT a range:
            self.assertNotEqual(foo.val, foo.ranges.get('val'))
        print('-' * 40)

        print('+++ ref (not a member of self._ranges)')
        foo.ref = [-1.2, 4.5, 6.7]
        print('ref', foo.ref)
        self.assertEqual(foo.ref, foo['ref'])
        self.assertEqual(foo.ref, foo._ref)
        print('-' * 40)

        print('+++ accuracy (not a member of self._ranges)')
        foo.accuracy = Range(-1.2, '3.4%')
        print('    accuracy', foo.accuracy)
        self.assertEqual(foo.accuracy, foo.ranges['accuracy'])
        self.assertEqual(foo.accuracy, foo['accuracy'])
        print('-' * 40)

        print('+++ repeatability (not a member of self._ranges)')
        foo.repeatability = (-1.234, '3.456%', '95%')
        print('    repeatability', foo.repeatability)
        self.assertEqual(foo.repeatability, foo.ranges['repeatability'])
        self.assertEqual(foo.repeatability, foo['repeatability'])
        print('-' * 40)

        print('+++ example member of self._ranges)')
        foo['expected'] = (-1.2, '3.4%FS')
        print('expected', foo['expected'])
        # ! self.ref IS a member of self._ranges
        self.assertEqual(foo['expected'], foo.ranges.get('expected'))

        print('-' * 40)
        print(foo)
        print('-' * 40)

        self.assertTrue(True)


    def test3(self):
        print('*** test: Range.simulate()')

        x = Range(-1, 1)
        x.simulate(size=100, plot=True)

        self.assertTrue(True)


    def test4(self):
        print('*** test: Range.simulate(), full_scale')
        full_scale = Range(-11, 30)
        x = Range(-1, '30%', 'cont')
        x.simulate(size=1000, plot=True, full_scale=full_scale)

        x = Range(-1, '30%', 'gauss')
        x.simulate(size=1000, plot=True, full_scale=full_scale)

        self.assertTrue(True)
        

    def test5(self):
        print('+++ tuple to Range and simulate')
        x = Parameter()
        x['test'] = (11, 22, 'bell')
        print(x['test'], type(x['test']))
        y = x['test'].simulate(size=10, plot=True)
        print(y)

        x['test'] = (66, 77, 'flat')
        y = x.simulate(range_key='test', size=10000, plot=True)

        self.assertTrue(True)


    def test6(self):
        print('+++ Range.simulate and plot')
        print('-' * 40)
        x = Range(-1, 1)
        y = x.simulate(size=256, plot=True)

        print('y:', y)

        x = Range(-10, 20,'gauss')
        x.simulate(size=1000, plot=True)

        x = Range(-1, 10,'bell')
        x.simulate(size=1000, plot=True)
        
        x = Range(-4, 7, 'cont')
        x.simulate(size=4096, plot=True)
        
        self.assertTrue(True)


    def test7(self):
        print('+++ Parameter.simulate and plot')
        print('-' * 40)

        plot = True
        
        x = Parameter()
        x.full_scale = Range(-110, 440)
        x.ref = np.sin(np.linspace(-7, 8, num=100))        

        x.calibrated = Range('-15%', '15%', 'gauss')   # rel to self.ref
        x.simulate(range_key='calibrated', plot=plot)

        x.calibrated = Range('-10%FS', '10%FS', 'flat')
        x.simulate(range_key='calibrated', plot=plot)

        x.calibrated = Range('-11%FS', '11%FS', 'flat')
        x.ref = np.exp(np.linspace(.1, 100, num=200))
        x.simulate(range_key='calibrated', plot=plot)

        x.calibrated = Range('-1%FS', 600, 'flat')
        x.ref = None
        x.simulate(range_key='calibrated', plot=plot, size=300)

        x.calibrated = Range('-10%', 0.1, 'flat') # relative to self.ref
        x.ref = np.sin(np.linspace(-7, 8, num=100))        
        x.simulate(range_key='calibrated', plot=plot)  # size would be ignored

        x.calibrated = Range('-2.3', '4.5', 'gauss')
        x.simulate(range_key='calibrated', plot=plot)
        
        y = x.val
        plt.title('Double check y=x.val')
        plt.plot(y)
        plt.show()
        
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
