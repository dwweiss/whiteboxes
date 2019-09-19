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
      2019-09-17 DWW
"""

import numpy as np
from scipy.optimize import minimize, basinhopping, curve_fit
import matplotlib.pyplot as plt


class Fit1D(object):
    """
    Compares performance of optimizers from SciPy for least-squares fit of
    function f(x) in 1D space
    """

    def __init__(self, identifier='Fit1D'):
        self.identifier = identifier

        np.random.seed(1729)

        def f(x, a=1, b=1, c=1, d=1):
            return a * np.cos(x * 1) + 0.1 * b * x + 0.01 * c * x**2 + d
        self.f = f

        self.X = np.linspace(-7, 7, 100)
        self.Y = None
        self.noise = 0.4
        self.loss = None
        self.C = None

    def pre(self):
        self.Y = self.f(self.X) + np.random.normal(-self.noise, self.noise,
                                                   size=self.X.size)

        # L2-norm of difference between prediction and target
        self.loss = lambda C: np.sqrt(np.sum((self.f(self.X, C[0], C[1], C[2],
                                                     C[3]) - self.Y)**2))
        plt.plot(self.X, self.Y, self.X, self.f(self.X))
        plt.show()

    def task(self):
        C0 = [2, 3, 11, -22]

        res1 = minimize(self.loss, C0, method='nelder-mead',
                        options={'xtol': 1e-8, 'disp': False})
        res2 = basinhopping(self.loss, C0, niter=100, T=1.0, stepsize=0.5,
                            minimizer_kwargs=None, take_step=None,
                            accept_test=None, callback=None, interval=50,
                            disp=False, niter_success=None)
        res3 = minimize(self.loss, C0, method='BFGS',
                        options={'xtol': 1e-8, 'disp': False})
        self.C = curve_fit(self.f, self.X, self.Y, p0=None, sigma=None,
                           absolute_sigma=False, check_finite=True,
                           bounds=(-np.inf, np.inf), method=None,
                           # jac=None,
                           )[0]

        print('nelder-mead: ', res1.x)
        print('              L2:', self.loss(res1.x))
        print('basinhopping:', res2.x)
        print('              L2:', self.loss(res2.x))
        print('BFGS:        ', res3.x)
        print('              L2:', self.loss(res3.x))
        print('least-squa.: ', self.C)
        print('              L2:', self.loss(self.C))

        self.X_tst = np.linspace(-10, +10, 100)
        self.Y_tst1 = self.f(self.X_tst, res1.x[0], res1.x[1], res1.x[2],
                             res1.x[3])
        self.Y_tst2 = self.f(self.X_tst, res2.x[0], res2.x[1], res1.x[2],
                             res1.x[3])
        self.Y_tst3 = self.f(self.X_tst, res3.x[0], res3.x[1], res1.x[2],
                             res1.x[3])
        self.Y_tst4 = self.f(self.X_tst, self.C[0], self.C[1], self.C[2],
                             self.C[3])
        self.Y_exa = self.f(self.X_tst)

    def post(self):
        fontsize = 15
        plt.rcParams.update({'font.size': fontsize})
        plt.rcParams['legend.fontsize'] = fontsize
        plt.title('Comparison')
        plt.plot(self.X_tst, self.f(self.X_tst), label='init')
        plt.plot(self.X, self.Y, label='noise')
        plt.plot(self.X_tst, self.Y_tst1, label='nelder-mead', ls='--')
        plt.plot(self.X_tst, self.Y_tst2, label='basinhopping', ls=':')
        plt.plot(self.X_tst, self.Y_tst3, label='bfgs', ls=':')
        plt.plot(self.X_tst, self.Y_tst4, label='ls', ls=':')
        plt.plot(self.X_tst, self.Y_exa, label='ana')
        plt.legend(bbox_to_anchor=(1.05, 1.03), loc='upper left')
        plt.grid()
        plt.show()

        plt.title('                                            Delta')
        plt.plot(self.X_tst, self.Y_tst1 - self.f(self.X_tst),
                 label='neldermead', ls='--')
        plt.plot(self.X_tst, self.Y_tst2 - self.f(self.X_tst),
                 label='basinhopp', ls=':')
        plt.plot(self.X_tst, self.Y_tst3 - self.f(self.X_tst),
                 label='bfgs', ls=':')
        plt.plot(self.X_tst, self.Y_tst4 - self.f(self.X_tst),
                 label='ls', ls=':')
        plt.plot(self.X, self.Y - self.f(self.X), label='noise', ls=':')
        plt.legend(bbox_to_anchor=(1.05, 1.03), loc='upper left')
        plt.grid()
        plt.show()

    def __call__(self):
        self.pre()
        self.task()
        self.post()


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    foo = Fit1D()
    if 0 or ALL:
        s = 'test optimizer with build-in example method f()'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))
        # check optimizer with Train1D.f()
        foo()

    if 0 or ALL:
        s = 'test optimizer with external function f() assigned below'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        def f(x, a=1, b=1, c=1, d=1):
            return a * np.cos(x * 1) + 0.1 * b * x + 0.01 * c * x**2 + d
        foo.f = f
        foo()

    if 0 or ALL:
        s = 'test optimizer with a method with self-access assigned below'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        def f(self, x, a=1, b=1, c=1, d=1):
            return a * np.cos(x * 1) + 0.1 * b * x + 0.01 * c * x**2 + d
        foo.f = f.__get__(foo, Fit1D)
        foo()
