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
      2020-11-16 DWW
"""

import unittest


class Parent(object):
    """
    Demonstrates structuring of a task
    """
    def __init__(self, identifier: str = 'Parent'):
        self.identifier = identifier
        self.data = 0

    def pre(self):
        self.data += 2.
        return True

    def task(self):
        self.data *= 3
        return 0.0

    def post(self):
        print('+++ data:', self.data, '  <=====')
        return True
    
    def __call__(self):
        print()
        print('This is:', "'" + self.identifier + "'")
        
        print('*** Pre-process')
        ok = self.pre()
        print('    ok:', ok)

        print('*** Task')
        res = self.task()
        print('    res:', res)

        print('*** Post-process')
        ok = self.post()
        print('    ok:', ok)

        print('End of:', "'" + self.identifier + "'")
        
        return res
        
    
class Child(Parent):
    """
    Demonstrates derivation of a child class from a parent class
    """
    def __init__(self, identifier: str = 'Child'):
        super().__init__(identifier=identifier)

    def pre(self):
        self.data += 4.
        return True


class Child2(Parent):
    """
    Demonstrates derivation of a child class from a parent class
    similar to class Child; 
    
    Additionally, the pre()-method of the Parent class will be called 
    before executing the own pre()-method 
    """
    def __init__(self, identifier: str = 'Child2'):
        super().__init__(identifier=identifier)

    def pre(self):
        super().pre()
        
        self.data += 4.
        return True
                

class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        foo = Parent()
        foo()

    def test2(self):
        foo = Child()
        foo()

    def test3(self):
        foo = Child2()
        foo()


if __name__ == '__main__':
    unittest.main()
