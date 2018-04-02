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
      2018-01-25 DWW
"""


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 0

    if 1 or ALL:
        """
        Example of printing values of local variables. If this print is made
        outside of a function, whole local() dictionary is printed (useless ?)
        """
        s = 'Print locals() within external FUNCTION'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        def foo():
            s = 'abc dde'
            reverse = s[::-1]
            replaced = s.replace('d', 'x')
            capitilised = ' '.join([x.capitalize() for x in s.split()])

            ######################################################
            for key in sorted(locals(), key=lambda s: s.lower()):
                if key != 'kwargs':
                    print('{:>15}: {}'.format(key, locals()[key]))
            ######################################################
            print()

        foo()

    if 1 or ALL:
        s = 'Print locals() within method of class, WITHOUT self.* members'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        class C(object):
            def foo(self):
                s = 'abc dde'
                reverse = s[::-1]
                replaced = s.replace('d', 'x')
                capitilised = ' '.join([x.capitalize() for x in s.split()])

                ######################################################
                for key in sorted(locals()):
                    if key not in ('self', 'kwargs'):
                        print('{:>15}: {}'.format(key, locals()[key]))
                ######################################################
        c = C()
        c.foo()
        
    if 1 or ALL:
        s = 'Print variables within method of class WITH self.* members'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        class C(object):
            def foo(self):
                s = 'abc dde'
                reverse = s[::-1]
                self.replaced_SELF = s.replace('d', 'x')
                capitilised = ' '.join([x.capitalize() for x in s.split()])

                ######################################################
                l = dict(locals(), **self.__dict__)
                for key in sorted(l):
                    if key not in ('self', 'kwargs'):
                        print('{:>15}: {}'.format(key, l[key]))
                ######################################################
        c = C()
        c.foo()
