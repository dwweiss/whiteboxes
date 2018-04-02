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
      2017-12-10 DWW
"""


def isFunction(x):
    """
    Checks if argument x is callable

    Args:
        x (any type):
            instance to be checked

    Returns:
        (bool):
            True if x is callable
    """
    return x is not None and hasattr(x, '__call__')


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 0 or ALL:
        def f():
            return 0.0

        class C(object):
            def f(self): pass
        c = C()

        for x in [f, lambda a: 1.0, c.f, c]:
            print('x:', str(x)[:str(x).index('at')-1] + str(x)[-1],
                  '=> isFunction:', isFunction(x))
        print()

        n = None
        i = 1
        b = True
        d = 1.0
        l = [1, 2]
        t = (1, 2)
        s = 'abc'
        for x in [n, i, b, d, l, t, s]:
            print('x:', x, '=> isFunction:', isFunction(x))
