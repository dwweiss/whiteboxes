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
      2018-06-25 DWW
"""

# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 0 or ALL:
        s = 'Assigns new method to class instance with access to self.* member'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        class Test(object):
            def __init__(self, x=0):
                self.x = x

            def execute(self):
                print("original execute(), y=x,   y:", self.x)

        def execute(self):
            print("replaced execute(), y=2*x, y:", 2 * self.x)

        # create instance 'test' of class 'Test'
        foo = Test(x=4)

        # call execute() defined in class Test
        foo.execute()
        foo.execute = execute.__get__(foo, Test)

        # call externally def. execute() assigned to instance 'test' of 'Test'
        foo.execute()
