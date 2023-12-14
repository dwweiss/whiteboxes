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
import numpy as np
import unittest

from whiteboxes.property.range import Range
from whiteboxes.property.property import Property


class TestUM(unittest.TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test1(self):
        foo = Property(identifier='abc')
        foo.calc = lambda T, p, x=0: 0.1 + 1e-3*T - 1e-4*p
        print(foo)
        foo.plot('title')
        print('-' * 79)

        self.assertTrue(True)


    def test2(self):
        foo = Property(identifier='abc')

        foo.calibrated = Range(-123, '100%',  'gauss')
        foo.full_scale = Range(-40.,  1000.)

        foo.T.calibrated = Range('-5%', 100.,  'gauss')
        foo.T.full_scale = Range(-40.,  100.,  'cont')

        foo.p.calibrated = Range(0.1e5, '10%', 'cont')
        foo.p.full_scale = Range(0.1e5, 100e5, 'cont')
 
        size = 1000
        plot = True
        range_key = 'calibrated'

        print('\n+++ Simulate', foo.identifier + ':')
        if plot:
            print('\n+++ Simulate foo')
        foo.val = foo[range_key].simulate(size=size, plot=plot,
                                   full_scale=foo.full_scale)
        if plot:
            print('\n+++ Simulate foo.T')
        foo.T.val = foo.T[range_key].simulate(size=size, plot=plot,
                                              full_scale=foo.T.full_scale)
        if plot:
            print('\n+++ Simulate foo.p')
        foo.p.val = foo.p[range_key].simulate(size=size, plot=plot,
                                              full_scale=foo.p.full_scale)
        print('-' * 79)

        self.assertTrue(True)
        
        
    def test3(self):
        foo = Property(identifier='abc')

        # if bounds are relative to reading, array foo.ref is required

        foo.calibrated = Range(-123, '100%FS',  'gauss')
        foo.full_scale = Range(-40.,  1000.)

        foo.T.ref = np.sin(np.linspace(0,2*3.14,50))
        foo.T.calibrated = Range('-5%', '1%',  'gauss')
        foo.T.full_scale = Range(-40.,  100.,  'cont')

        foo.p.calibrated = Range(0.1e5, '1%FS', 'cont')
        foo.p.full_scale = Range(0.1e5, 100e5, 'cont')
 
        size = 1000
        plot = True
        range_key = 'calibrated'

        print('\n+++ Simulate property: all', foo.identifier + ':')
        if plot:
            print('\n+++ Simulate property: foo')
        foo.val = foo.simulate(range_key=range_key, size=size, plot=plot)
        print('-' * 79)

        self.assertTrue(True)


    def test4(self):
        foo = Property(identifier='abc')

        # if bounds are relative to reading, array foo.ref is required

        foo.calibrated = Range(-123, '100%FS',  'gauss')
        foo.full_scale = Range(-40.,  1000.)

        foo.T.ref = np.sin(np.linspace(0,2*3.14,50))
        foo.T.calibrated = Range('-5%', '1%FS',  'gauss')
        foo.T.full_scale = Range(-40.,  100.,  'cont')
 
        size = 1000
        plot = True
        range_key = 'calibrated'

        print('\n+++ Simulate property: all', foo.identifier + ':')
        if plot:
            print('\n+++ Simulate property: foo')
        foo.val = foo.simulate(range_key=range_key, size=size, plot=plot)
        print('-' * 79)

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
