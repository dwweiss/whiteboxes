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
      2018-10-15 DWW
"""

import numpy as np


def x_y_xy(X, Y, U):
    """
    Approximates u(x,y) = c0 + c1*x + c2*y + c3 *x*y

    Least-square approximation
        F = sum{ ( c0 + c1*X_i + c2*Y_i + c3*X_i*Y_i - U_meas_i )^2 } ==> 0

        dF/dc0 = 0 = sum 2*(...) * 1
        dF/dc1 = 0 = sum 2*(...) * x
        dF/dc2 = 0 = sum 2*(...) * y
        dF/dc3 = 0 = sum 2*(...) * xy

       | n      sum_x   sum_y   sum_xy   |   | c0 |   | sum_u   |
       | sum_x  sum_x2  sum_xy  sum_x2y  |   | c1 |   | sum_ux  |
       | sum_y  sum_xy  sum_y2  sum_xy2  | * | c2 | = | sum_uy  |
       | sum_xy sum_x2y sum_xy2 sum_x2y2 |   | c3 |   | sum_uxy |

    Args:
        X (1D array of float):
            arguments
        Y (1D array of float):
            arguments
        U (1D array of float):
            dependent variable

    Returns:
        weights (1D array of float)

    Example:
        X = [13., 21., 32., 52., 13., 21., 32., 52., 52., 52.]
        Y = [.56, .65, .7, .7, 2.03, 1.97, 1.92, 1.81, 2.89, 7.83]
        U = [-0.313, -0.192, -0.145, -0.172, -0.563, -0.443, -0.408, -0.391,
             -0.63,  -1.701 ]
        C = x_y_xy( X, Y, U)
    """
    assert len(X) >= 4
    assert len(X) == len(Y), 'lenX:' + str(len(X)) + ' lenY:' + str(len(Y))
    assert len(X) == len(U), 'lenX:' + str(len(X)) + ' lenY:' + str(len(U))
    X = np.asfarray(X)
    Y = np.asfarray(Y)
    U = np.asfarray(U)

    n = len(X)
    x, y, x2, y2, xy, x2y2, xy2, x2y = 0., 0., 0., 0., 0., 0., 0., 0.
    u, ux, uy, uxy = 0., 0., 0., 0.

    for i in range(n):
        XY = X[i] * Y[i]
        XX = X[i] * X[i]
        YY = Y[i] * Y[i]
        xy += XY
        x += X[i]
        y += Y[i]
        x2 += XX
        y2 += YY
        x2y += XX * Y[i]
        xy2 += X[i] * YY
        x2y2 += XX * YY
        u += U[i]
        uxy += U[i] * XY
        ux += U[i] * X[i]
        uy += U[i] * Y[i]

    A = np.array([[n,  x,   y,   xy],
                  [x,  x2,  xy,  x2y],
                  [y,  xy,  y2,  xy2],
                  [xy, x2y, xy2, x2y2]])
    F = np.array([u,   ux,  uy,  uxy])

    return np.linalg.solve(A, F)


def x_y(X, Y, U):
    """
    Approximates u(x,y) = c0 + c1*x + c2*y

    Least-square approximation
        F = sum{ ( c0 + c1*X_i + c2*Y_i + c3*X_i*Y_i - U_meas_i )^2 } ==> 0

        dF/dc0 = 0 = sum 2*(...) * 1
        dF/dc1 = 0 = sum 2*(...) * x
        dF/dc2 = 0 = sum 2*(...) * y

       | n      sum_x   sum_y  |   | c0 |   | sum_u   |
       | sum_x  sum_x2  sum_xy | * | c1 | = | sum_ux  |
       | sum_y  sum_xy  sum_y2 |   | c2 |   | sum_uy  |

    Args:
        X (1D array of float):
            arguments
        Y (1D array of float):
            arguments
        U (1D array of float):
            dependent variable

    Returns:
        weights (1D array of float)
    """
    assert len(X) >= 3
    assert len(X) == len(Y), 'lenX:' + str(len(X)) + ' lenY:' + str(len(Y))
    assert len(X) == len(U), 'lenX:' + str(len(X)) + ' lenY:' + str(len(U))
    X = np.asfarray(X)
    Y = np.asfarray(Y)
    U = np.asfarray(U)

    n = len(X)
    x, y, x2, y2, xy = 0., 0., 0., 0., 0.
    u, ux, uy = 0., 0., 0.

    for i in range(n):
        XY = X[i] * Y[i]
        XX = X[i] * X[i]
        YY = Y[i] * Y[i]
        xy += XY
        x += X[i]
        y += Y[i]
        x2 += XX
        y2 += YY
        u += U[i]
        ux += U[i] * X[i]
        uy += U[i] * Y[i]

    A = np.array([[n,  x,   y],
                  [x,  x2,  xy],
                  [y,  xy,  y2]])
    F = np.array([u,   ux,  uy])

    return np.linalg.solve(A, F)


def x_y_xy_x2_y2(X, Y, U):
    """
    Approximates u(x,y) = c0 + c1*x + c2*y + c3*xy + c4*x^2 + c5*y^2

    Args:
        X (1D array of float):
            arguments
        Y (1D array of float):
            arguments
        U (1D array of float):
            dependent variable

    Returns:
        weights (1D array of float)
    """
    assert len(X) >= 6
    assert len(X) == len(Y), 'lenX:' + str(len(X)) + ' lenY:' + str(len(Y))
    assert len(X) == len(U), 'lenX:' + str(len(X)) + ' lenU:' + str(len(U))
    X = np.asfarray(X)
    Y = np.asfarray(Y)
    U = np.asfarray(U)

    n = len(X)
    x, y, x2, x3, x4, y2, y3, y4 = 0., 0., 0., 0., 0., 0., 0., 0.
    xy, x2y, xy2, x2y2, xy3, x3y = 0., 0., 0., 0., 0., 0.
    u, ux, uy, uxy, ux2, uy2 = 0., 0., 0., 0., 0., 0.

    for i in range(n):
        XY = X[i] * Y[i]
        XX = X[i] * X[i]
        YY = Y[i] * Y[i]
        x += X[i]
        y += Y[i]
        x2 += XX
        x3 += XX * X[i]
        x4 += XX*XX
        y2 += YY
        y3 += YY * Y[i]
        y4 += YY*YY
        x2y += XX * Y[i]
        xy2 += X[i] * YY
        x3y += XX * XY
        xy3 += XY * YY
        x2y2 += XX * YY
        u += U[i]
        uxy += U[i] * XY
        ux += U[i] * X[i]
        uy += U[i] * Y[i]
        ux2 += U[i] * XX
        uy2 += U[i] * YY

    A = np.array([[n,  x,   y,   xy,   x2,   y2],
                  [x,  x2,  xy,  x2y,  x3,   xy2],
                  [y,  xy,  y2,  xy2,  x2y,  y3],
                  [xy, x2y, xy2, x2y2, x3y,  xy3],
                  [x2, x3,  x2y, x3y,  x4,   x2y2],
                  [y2, xy2, y3,  xy3,  x2y2, y4]])
    F = np.array([u,   ux,  uy,  uxy,  ux2,  uy2])

    return np.linalg.solve(A, F)


def xy_x2_y2(X, Y, U):
    """
    Approximates u(x,y) = c0 + c1*x*y + c2*x^2 + c3*y^2

    Args:
        X (1D array of float):
            arguments
        Y (1D array of float):
            arguments
        U (1D array of float):
            dependent variable

    Returns:
        weights (1D array of float)
    """
    assert len(X) >= 4
    assert len(X) == len(Y), 'lenX:' + str(len(X)) + ' lenY:' + str(len(Y))
    assert len(X) == len(U), 'lenX:' + str(len(X)) + ' lenU:' + str(len(U))
    X = np.asfarray(X)
    Y = np.asfarray(Y)
    U = np.asfarray(U)

    n = len(X)
    x2, x4, y2, y4 = 0., 0., 0., 0.
    xy, x2y2, xy3, x3y = 0., 0., 0., 0.
    u, uxy, ux2, uy2 = 0., 0., 0., 0.

    for i in range(n):
        XY = X[i] * Y[i]
        XX = X[i] * X[i]
        YY = Y[i] * Y[i]
        xy += XY
        x2 += XX
        y2 += YY
        x2y2 += XX * YY
        u += U[i]
        uxy += U[i] * XY
        ux2 += U[i] * XX
        uy2 += U[i] * YY

    A = np.array([[n,  xy,   x2,   y2],
                  [xy, x2y2, x3y,  xy3],
                  [x2, x3y,  x4,   x2y2],
                  [y2, xy3,  x2y2, y4]])
    F = np.array([u,   uxy,  ux2,  uy2])

    return np.linalg.solve(A, F)
