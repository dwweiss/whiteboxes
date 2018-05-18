"""
  Copyright (c) 2018- by Dietmar W Weiss

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
      2018-05-18 DWW
"""

import numpy as np
try:
    from lmfit import Minimizer, Parameters, report_fit
    # TODO from lmfit import conf_interval, printfuncs
except ImportError:
    print('??? package lmfit not imported')


def f(x, **kwargs):
    """
    Theoretical submodel f(x) for SINGLE data point

    Args:
        x (1D array_like of float):
            input, shape: (nInp)

        kwargs (dict, optional):
            keyword arguments:

            define (bool, optional):
                if True then return definition of fit parameters
                default: False

            c0, c1, ... (float, optional):
                coefficients

    Returns:
        (1D array_like of float, or float):
            output, shape: (nOut) if 'define' is False
        or
        (dict):
            dict of initial values and bounds of fit params if 'define' is True
    """
    if 'define' in kwargs:
        # dict of values of lmfit.Parameters: {'key': (value, min, max), ...}
        return {'c0': (5, -10, 100), 'c1': (0.2, -10, 10), 'c2': (3, -10, 9), 
                'c3': (.007, -10, 10)}

    c0, c1, c2, c3 = kwargs.get('c0', 1), kwargs.get('c1', 1), \
        kwargs.get('c2', 1), kwargs.get('c3', 1)

    y0 = c0 * np.sin(x[0] * c2 + c1) * np.exp(-x[0]**2 * c3)
    y1 = x[1]
    return y0, y1


class LmfitExample(object):
    """
    Demonstrates the use of the Lmfit package for curve fitting
    """

    def __init__(self):
        self.x = None
        self.y = None
        self.X = None
        self.Y = None
        self.ready = True
        self._weights = None  # dictionary {str: float} of fit parameters
        self.best = None

        self.f = f  # assign externally defined function

    def train(self, X, Y, **kwargs):
        """
        Trains model. X and Y are stored as self.X and self.Y if both not None

        Args:
            X (2D or 1D array_like of float):
                training input, shape: (nPoint, nInp) or shape: (nPoint)

            Y (2D or 1D array_like of float):
                training target, shape: (nPoint, nOut) or shape: (nPoint)

            kwargs (dict, optional):
                keyword arguments

                trainers (string or list of string):
                    trainer type, if 'all' then following trainers are tried: 
                    
                    ’leastsq’:       Levenberg-Marquardt (default)
                    ’least_squares’: Least-Squares minimization, using 
                                     Trust Region Reflective method by default
                    ’differential_evolution’: differential evolution
                    ’brute’:         brute force method
                    ’nelder’:        Nelder-Mead
                    ’lbfgsb’:        L-BFGS-B
                    ’powell’:        Powell
                    ’cg’:            Conjugate-Gradient
                    ’newton’:        Newton-Congugate-Gradient
                    ’cobyla’:        Cobyla
                    ’tnc’:           Truncate Newton
                    ’trust-ncg’:     Trust Newton-Congugate-Gradient
                    ’dogleg’:        Dogleg
                    ’slsqp’:         Sequential Linear Squares Programming

                epochs (int):
                    maximum number of epochs

                goal (float):
                    residuum to be met

                trials (int):
                    number of repetitions of training with same trainer
                ...

        Returns:
            (dict {str: float or str or int}):
                result of best training trial:
                    'trainer' (str): best trainer
                    'L2'    (float): sqrt{sum{(net(x)-Y)^2}/N} of best training
                    'abs'   (float): max{|net(x) - Y|} of best training
                    'iAbs'    (int): index of Y where absolute error is maximum
                    'epochs'  (int): number of epochs of best training

        Note:
            If X or Y is None, or training fails then self.best['trainer']=None
        """

        def residual(params, X=None, Y=None, **kwargs):
            """
            Objective function to be minimized (passed to lmfit.minimize())

            Args:
                params (ordered dict or lmfit.Parameter):
                    dictionary of parameters with value, min, max etc

                X (2D or 1D array_like of float):
                    training input, shape: (nPoint, nInp)

                Y (2D or 1D array_like of float):
                    training target, shape: (nPoint, nOut)

                kwargs (dict, optional):
                    keyword arguments

            Returns:
                (2D array of float):
                    difference between prediction f(X) and target Y(X)
            """
            opt = kwargs.copy()
            opt.update(params.keys())
            if X is None:
                X = self.X
            if Y is None:
                Y = self.Y
            res = np.subtract(self.predict(X, **opt), Y)

            if res.shape[1] > 1:
                res = res.flatten()
            return res

        ###

        silent = kwargs.get('silent', True)
        trainers = kwargs.get('trainers', None)
        if trainers is None:
            trainers = ['leastsq']
        trainers = np.atleast_1d(trainers)

        if isinstance(trainers[0], str) and trainers[0].lower() == 'all':
            trainers = ['leastsq', 
                        'least_squares',
                        # TODO .. takes 2 positional arguments but * were given

                        #'differential_evolution',  # TypeError: penalty() 
                        #     takes 2 positional arguments but 4 were given
                        #'brute', 
                        #'nelder', 
                        #'lbfgsb', 
                        #'powell', 
                        #'cg', 'newton', 
                        #'cobyla', 'tnc', 'trust-ncg', 'dogleg', 'slsqp'
                        ]

        if X is not None and Y is not None:
            self.X, self.Y = X, Y

        params = Parameters()
        for key, val in self.f(None, define=True).items():
            if isinstance(val, (int, float)):
                params.add(key, value=val)
            elif len(val) == 1:
                params.add(key, value=val[0])
            elif len(val) == 2:
                params.add(key, value=val[0], min=val[1])
            elif len(val) == 3:
                params.add(key, value=val[0], min=val[1], max=val[2])
            else:
                assert 0, str(key) + ': ' + str(val)

        self.ready = True
        self.best = {'L2': np.inf}
        for trainer in trainers:
            if not silent:
                print("+++ trainer:'" + trainer + "'")
            self._weights = None  # see self.predict(), differeantn. train/pred
            if trainer in ('leastsq', 'least_squares'):
                fnc = residual
            else:
                fnc = residual
            minimizer = Minimizer(fnc, params, fcn_args=(X, Y))
            args = kwargs if trainer not in ('least_squares') else {}
            result = minimizer.minimize(method=trainer, args=args)
                
            self.ready = True
            if self.ready:
                self._weights = result.params.valuesdict()  # fit param as dict
            L2 = np.sqrt(np.mean((self.predict(self.X) - self.Y)**2))
            if self.best['L2'] > L2:
                self.best = {'trainer': trainer, 'L2': L2, 'abs': np.inf,
                             'iAbs': -1, 'epochs': -1}
            if not silent:
                report_fit(result)
                print('+++ best:', self.best)
                
        if not silent:
            report_fit(result)
            # TODO :
            # ci = conf_interval(minimizer, result)
            # printfuncs.report_ci(ci)

    def predict(self, x, **kwargs):
        """
        Prediction for MULTIPLE data points. With MPI (requires parallel.py)
        the execution can be distributed.
        x and y=f(x) are stored as self.x and self.y

        Args:
            x (2D or 1D array_like of float):
                prediction input, shape: (nPoint, nInp) or shape: (nInp)

            kwargs (dict, optional):
                keyword arguments

                c0, c1, ... (multiple float):
                    coefficients
                    default: 1.0

                ... further options to be passed to self.f

        Returns:
            (2D array of float):
                if x is not None and self.ready: prediction output
            or
            (None):
                otherwise
        """
        kw = kwargs.copy()
        if 'x' in kw:
            del kw['x']
        if self._weights is not None:
            kw.update(self._weights)
        self.x = x
        self.y = [np.atleast_1d(self.f(x=_x, **kw)) for _x in self.x]
        self.y = np.array(self.y)

        return self.y


# Examples ####################################################################

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    ALL = 1

    if 1 or ALL:
        model = LmfitExample()

        X0 = np.linspace(0, 15, 301)
        X1 = np.linspace(-10, 10, 301)
        X = np.c_[X0, X1]

        Y_exa = model.predict(X, c0=5, c1=0.2, c2=3, c3=0.007)
        Y = Y_exa + np.random.normal(size=Y_exa.shape, scale=0.2)
        y0 = model.predict(X, silent=False)

        best = model.train(X, Y, silent=False, trainers='all')
        print('weights:', list(model._weights.values()))
        y = model.predict(X)

        plt.title('Lmfit $Y(X)$ vs $f(X)$')
        plt.xlabel('$X$')
        plt.ylabel('$y$')
        plt.plot(X[:, 0], Y[:, 0], 'k+', label='$Y$')
        plt.plot(X[:, 0], y0[:, 0], 'g', label='$y_0$')
        plt.plot(X[:, 0], y[:, 0], 'b', label='$y$')
        plt.legend()
        plt.show()
