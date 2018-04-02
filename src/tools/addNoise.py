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
      2017-12-21 DWW
"""

import numpy as np


def addNoise(x, relative=0.0, absolute=None):
    """
    Adds noise to an array of any dimension

    Args:
        x (array_like of float):
            initial array

        relative (float, optional):
            maximum noise added, relative to difference between maximum and
            minimum of array x only effective if 'absolute' is None

        absolute (float, optional):
            maximum of absolute noise added to x

    Returns:
        (array of float):
            array with noise

    Note:
        'absolute' overrules 'relative' argument (as in real life ;-)
        In case of negative 'relative' and 'absolute', x returns unchanged
    """
    x = np.asfarray(x)
    if absolute is None:
        dx = relative * (x.max() - x.min()) if relative is not None else 0.0
    else:
        dx = absolute
    if dx <= 0.:
        return x
    else:
        return x + np.random.normal(loc=0.0, scale=dx, size=x.shape)


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    import matplotlib.pyplot as plt

    if 0 or ALL:
        X = np.linspace(-1, 3, num=4)

        print('1 X_noise:', addNoise(X, 0.1))
        print('2 X_noise:', addNoise(X, absolute=0.2))

        # 'absolute' overrules the 'relative' argument
        print('3 X_noise:', addNoise(X, relative=0.25, absolute=0.5))
        print('4 X_noise:', addNoise(X, relative=None, absolute=0.5))
        print('5 X_noise:', addNoise(X, relative=0.1,  absolute=None))
        print('6 X_noise:', addNoise(X, relative=None, absolute=None))
