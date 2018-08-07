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
      2018-08-07 DWW
"""

from math import inf
import numpy as np
from scipy.optimize import curve_fit

from grayboxes.base import Base
from grayboxes.plotarrays import plotSurface, plotIsoMap


class Fit2DModel(Base):
    """
    Tunes a given theoretical 2D model self.f(x_com, x_tun) to synthetically 
    generated training data

    In the example section, the model of pressure drop in a pipework section 
    (reduction, straight pipe, expansion) is tuned 
    """

    def __init__(self, identifier='Fit2DModel', f=None, noise=None):
        """
        Note:
            as default, self.f() contains an example function for testing
        """
        super().__init__(identifier=identifier)

        # example method, has to be overloaded with actual theoretical model
        # x is an 1D array or a transposed 2D array, x.shape: (nInp, nPoint)
        self.f = f if f is not None else lambda x, a=1, b=1, c=1, d=1: \
            a * np.cos(x[0]) + 0.1 * b * x[1] + 0.01 * c * x[0]**2 + d

        # input and target arrays
        self.nx, self.ny = 20, 20
        self.X, self.Y = None, None

        # input and prediction arrays
        self.x, self.y = None, None

        # coefficients
        self.C = None

        # noise for synthetic data generation
        self.noise = noise if noise is not None else 0.25

    def pre(self, **kwargs):
        """
        Generates synthetic data for fitting of theoretical model self.f()
        """
        super().pre(**kwargs)

        if 'f' in kwargs:
            self.f = kwargs['f']
        if 'noise' in kwargs:
            self.noise = kwargs['noise']
        if 'x' in kwargs:
            self.x = kwargs['x']
        if 'X' in kwargs:
            self.X = kwargs['X']
        if 'Y' in kwargs:
            self.Y = kwargs['Y']

        # X0 and X1 are common model input
        if self.X is None:
            X0, X1 = np.meshgrid(np.linspace(0, 1, self.nx),
                                 np.linspace(-7, 7, self.ny))
            X0 = np.asfarray(X0).ravel()         # ravel() flattens to 1D array
            X1 = np.asfarray(X1).ravel()
            self.X = np.asfarray([X0, X1]).T

        # Y is target (exact + noise)
        if self.Y is None:
            Y_exact = self.f(self.X.T)
            plotSurface(self.X.T[0], self.X.T[1], Y_exact,
                        labels=['x0', 'x1', 'exact'])
            np.random.seed(1729)
            dy = self.noise * (Y_exact.max() - Y_exact.min())
            self.Y = Y_exact + np.random.uniform(-dy, dy, size=Y_exact.size)

        plotSurface(self.X.T[0], self.X.T[1], self.Y,
                    labels=['x0', 'x1', 'target: exact+noise'])

    def task(self, **kwargs):
        """
        Least-square fit of self.f() to the synthetic data generated in pre()
        """
        super().task(**kwargs)

        self.C = curve_fit(self.f, self.X.T, self.Y.T, p0=None,
                           sigma=None, absolute_sigma=False, check_finite=True,
                           bounds=(-inf, inf), method=None)[0]
        print('+++ Tuning parameters:', self.C)

        # y is prediction
        if self.x is None:
            self.x = self.X.copy()

        self.y = self.f(self.x.T, self.C[0], self.C[1], self.C[2], self.C[3])

        return self.y

    def post(self, **kwargs):
        """
        Plots exact solution, test data (exact solution + noise), prediction of
        test data with tuned model, difference between prediction and test data
        """
        super().post(**kwargs)

        plotSurface(self.X.T[0], self.X.T[1], self.f(self.X.T),
                    labels=['X0', 'X1', 'exact'])
        plotSurface(self.X.T[0], self.X.T[1], self.Y,
                    labels=['X0', 'X1', 'target'])
        plotSurface(self.x.T[0], self.x.T[1], self.y,
                    labels=['x0', 'x1', 'prediction'])
        plotIsoMap(self.x.T[0], self.x.T[1], self.y,
                   labels=['x0', 'x1', 'prediction'])
        plotSurface(self.x.T[0], self.x.T[1], self.y - self.Y,
                    labels=['x0', 'x1', r'$\Delta y = y - Y$'])
        plotIsoMap(self.x.T[0], self.x.T[1], self.y - self.Y,
                   labels=['x0', 'x1', r'$\Delta y = y - Y$'])


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 0 or ALL:
        # built-in method self.f, generate X from default and Y = f(X) + noise
        foo = Fit2DModel(noise=0.5)
        foo()

    if 0 or ALL:
        def fUser(x, a=1, b=1, c=1, d=1):
            return a * np.exp(x[0] * 1) + 0.1 * b * x[1] + \
                0.01 * c * x[0]**2 + d

        # user-defined self.f, generate X from default and Y = f(X) + noise
        foo = Fit2DModel(f=fUser, noise=0.2)
        foo()

    if 1 or ALL:
        """
        Pressure loss of the flow of a liquid trough a pipe reduction, a
        straight pipe and a pipe extension
        """
        from coloredlids.pressure_drop import dp_inlet_reduce_middle_expand_outlet

        def f(x, a=1, b=1, c=1, d=1):
            """
            Args:
                x (2D or 1D array_like of float):
                    x[:, 0]: mean velocity [m/s]
                    x[:, 1]: kinematic viscosity [m2/s]
                    first index is parameter index, second one is point index

                a, b, c, d (float, optional):
                    tuning parameter

            Returns:
                (1D array of float):
                    y: pressure loss [MPa], index is point index
            """
            if x.ndim == 1:
                X = np.atleast_2d(x.copy())
            else:
                X = np.atleast_2d(x.copy()).T

            eps_rough = 10e-6
            nu = 1e-6
            rho = 1000
            D1, L1 = 20e-3, 20e-3
            D2, L2 = 5e-3, 200e-3
            D3, L3 = D1, L1
            y = []
            for xx in X:
                v1, nu = xx[0], xx[1]
                dp = dp_inlet_reduce_middle_expand_outlet(v1=v1, D1=D1,
                             L1=L1, D2=D2, L2=L2, D3=D3, L3=L3, nu=nu, rho=rho,
                             eps_rough=eps_rough, a=a, b=b, c=c, d=d)
                y.append(dp[0])           # dp is array of (dp_total, dp1..dp3)
            return np.asfarray(y) * 1e-6

        # defines common parameters and creates 2D input array
        v1_seq = [1, 2, 3, 4, 5]
        nu_seq = [1e-6, 1e-5, 1e-4, 1e-3]
        X0, X1 = np.meshgrid(v1_seq, nu_seq)

        # flattens X0 and X1 to 1D arrays and creates 2D: X[0..nPoint-1][0..1]
        X = np.asfarray([X0.ravel(), X1.ravel()]).T

        foo = Fit2DModel(f=f, noise=0.1)

        # creates optionally training data (X, Y)
        if 1:
            if X is not None:
                Y_exact = f(X.T)
                plotSurface(X.T[0], X.T[1], Y_exact,
                            labels=['x0', 'x1', 'exact'])
                np.random.seed(1729)
                dy = foo.noise * (Y_exact.max() - Y_exact.min())
                Y = Y_exact + np.random.uniform(-dy, dy, size=Y_exact.size)

        # tunes model and predicts y(x)
        y = foo(X=X, Y=Y, x=X)
