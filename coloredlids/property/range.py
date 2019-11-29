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

__all__ = ['Range', 'Scalar', 'Floats',
           'relative_to_absolute_range', 'percentage_of_bound', 
           'in_range', 'in_range_full_scale', 'in_range_abs_rel_error',
           'is_bound_absolute',
           'is_bound_relative_to_reading', 'is_bound_relative_to_full_scale',
           'is_range_relative_to_reading', 'is_range_relative_to_full_scale',]

import numpy as np
np.random.seed(19680801)

from typing import List, Optional, Tuple, Union
import matplotlib.pyplot as plt

Scalar = Optional[Union[float, int, str]]
Floats = Optional[Union[float, List[float], np.ndarray]]


def is_bound_absolute(bound: Scalar) -> bool:
    return '%' not in str(bound)


def percentage_of_bound(bound: Scalar) -> Optional[float]:
    if '%' in str(bound):
        return float(bound[:bound.find('%')]) * 1e-2
    else:
        return None


def is_bound_relative_to_reading(bound: Scalar, 
                                 full_scale_pattern: str = '%FS') -> bool:
    return '%' in str(bound) and full_scale_pattern not in str(bound).upper()


def is_range_relative_to_reading(range_: 'Range') -> bool:
    return is_bound_relative_to_reading(range_.lo) \
       and is_bound_relative_to_reading(range_.up)


def is_bound_relative_to_full_scale(bound: Scalar, 
                                    full_scale_pattern: str = '%FS') -> bool:
    return full_scale_pattern in str(bound).upper()


def is_range_relative_to_full_scale(range_: 'Range', 
                                    full_scale_pattern: str = '%FS') -> bool:
    return is_bound_relative_to_full_scale(range_.lo, full_scale_pattern) \
       and is_bound_relative_to_full_scale(range_.up, full_scale_pattern)


def relative_to_absolute_range(range_: 'Range', full_scale: 'Range',
                               relative_pattern: str = '%') \
        -> Optional['Range']:
    """
    Calculates absolute values of bounds of 'range_' which are defined
    relative to 'full_scale'. Relative bounds are of type str and
    must contain the character '%' after the number, e.g. '2%' or '5%FS'

    Args:
        range_:
            range with absolute or relative bounds: 7, '7', '2%', '2%FS'

        full_scale:
            range with absolute bounds: eg. -3 or '-3'
    
        relative_pattern:
            substring defining a bound as relative to full scale range
            or relative to reading, usually: '%' 
    
    Returns:
        absolute range 
        OR
        None if one of the bounds of range_ is None or if one of the 
            bounds of full_scale cannot be converted to float 
        
    Example:
        range_ = Range('-1%FS', 4.)
        full_scale = Range(-11., 22.)
        rng = relative_to_absolute_range(range_, full_scale)
        
        # upper bound of range_ is already absolute
        print(rng)  # => (-0.11, 4.) 
        
    Note:
        If range_[i] is of type int or float, full_scale[i] is 
        ignored  
        
        The function tolerates that: 
            one or all bounds of range_ are of type float or int
            one or all bounds of range_full_scale are of type str
            
            
                                   -----------------------
                                   |                     |
                                   |                   abs(-10%) = 0.1 
                                   |       full_scale    |
relative_to_absolute_range(2., ('-10%', 7), (-3, 8))     V
                                   range      |  |      0.1*(-3) --> lo:-0.3
                                              |  v            ^
                                              |  up: 8        |
        lo is lower bound and up is           |               |
        upper bound of effective range        -----------------
        
                                  # range_full_scale.lo = -3 is 
                                  # multiplied with abs(-10e-2) => -0.3 
                                  # range_full_scale.up = 8 is ignored 
                                  # because range_[1] = 7 
    """
    if range_ is None:
        return None
    
    lo  = range_.lo
    is_relative_lo = False
    
    try:
        float(lo)
    except:
        is_relative_lo = True
        
        if full_scale is None:
            return None
        if  not isinstance(lo, str) or not relative_pattern in lo.upper():
            return None
        
        lo = full_scale.lo
        try:
            lo = float(lo)
        except (TypeError, ValueError) as err:
            print('??? relative_to_absolute_range() 1:', err, 'lo:', lo)
            return None
        
    up = range_.up
    is_relative_up = False
    try:
        float(up)
    except:
        is_relative_up = True

        if full_scale is None:
            return None
        if not isinstance(up, str) or not relative_pattern in up.upper():
            return None
        
        up = full_scale.up
        try:
            up = float(up)
        except (TypeError, ValueError) as err:
            print('??? relative_to_absolute_range() 2:', err, 'up:', up)
            return None

    if is_relative_lo:
        try:
            lo = float(range_.lo[:range_.lo.find('%')]) * 1e-2
            lo = np.abs(lo)
            lo *=  float(full_scale.lo)
        except (TypeError, ValueError) as err:
            print('??? relative_to_absolute_range() 3:', err, 'lo:', lo)
    if is_relative_up:
        try:
            up = float(range_.up[:range_.up.find('%')]) * 1e-2
            up *=  float(full_scale.up)
        except (TypeError) as err:
            print('??? relative_to_absolute_range() 4:', err, 'up:',up)

    distr = range_.distr if range_.distr is not None else full_scale.distr

    return Range(lo, up, distr)


def in_range(val: Floats, range_: 'Range') -> bool:
    """
    Checks if scalar 'val' or all elements of array 'val' are within 
    lower and upper bound of 'range_'. 
    
    Args:
        val:
            actual value as scalar (int, float, str) or sequence of it 
        
        range_: 
            lower & upper bound [range_.lo, range_.up] of value 
            range and distribution range_.distr

    Returns:
        False if 'val' is not within 'range_.lo' and 'range_.up'
        
    Note: 
        The function tolerates that lower and upper bound might be 
        mistakenly swapped 
    """
    try:
        val = [float(x) for x in np.atleast_1d(val)]
        lo, up = float(range_[0]), float(range_[1])
    except (TypeError) as err:
        print('??? in_range():', err)
        return False
    
    if lo > up:
        lo, up = up, lo
        print('!!! in_range(): swap', (up, lo), '==>', (lo, up))

    return all(np.greater_equal(val, lo)) and all(np.less_equal(val, up))


def in_range_full_scale(val: Floats, range_: 'Range', 
                        full_scale: 'Range') -> bool:
    """
    Checks if val is in of bounds of 'range_' which can be defined
    relative to 'full_scale'. Relative bounds are of type str and
    must contain the character '%' after the number, e.g. '-1.2%'

    Args:
        range_:
            range with bounds given absolute or relative: 7, '7' or '2%'

        full_scale:
            range with bounds given absolute: eg. -3 or '-3'
            
    Returns:        
        True if val or all elements of val within the given bounds
    """
    return in_range(val, relative_to_absolute_range(range_, full_scale))


def in_range_abs_rel_error(val: float, ref: float, range_: 'Range') -> bool:
    """
    Checks if absolute error (val - ref) or relative error 
    (val - ref) / ref is within the given error range. A relative error 
    limit is applied if range_[i] is a string and contains character '%'
    
    Args:
        val:
            Actual value 
        
        ref: 
            Reference value 
            
        range_: 
            Lower und upper bound of valid error range. 
            If range_[i] contains '%', the error is relative
            
    Returns:
        False if error (absolute or relative) is not within range_.lo
        and range_.up
        
    Note:
        The function tolerates that one or both bounds of range_ are 
        of type float or int
    """
    try:
        val = np.array([float(x) for x in np.atleast_1d(val)])
        ref = np.array([float(x) for x in np.atleast_1d(ref)])
    except (TypeError, ValueError) as err:
        print('??? in_range_abs_rel:()', err)
        return False
    
    lower_bound_is_relative = '%' in str(range_.lo)
    upper_bound_is_relative = '%' in str(range_.up)
        
    abs_err = val - ref
    if lower_bound_is_relative or upper_bound_is_relative:
        try:
            rel_err = abs_err / ref
        except ZeroDivisionError as err:
            print('??? in_range_abs_rel:()', err)
            return False
    
    if lower_bound_is_relative:
        s = range_.lo[:range_.lo.find('%')]
        try:
            lower_bound = float(s) * 1e-2
        except (TypeError) as err:
            print('??? in_range_abs_rel:()', err)
        if any(np.less(rel_err, lower_bound)):
            return False
    else:
        try:
            lower_bound = float(range_.lo)
        except (TypeError) as err:
            print('??? in_range_abs_rel:()', err)
        if any(np.less(abs_err, lower_bound)):
            return False
       
    if upper_bound_is_relative:
        s = range_.up[:range_.up.find('%')]
        try:
            upper_bound = float(s) * 1e-2
        except (TypeError) as err:
            print('??? in_range_abs_rel:()', err)

        if any(np.greater(rel_err, upper_bound)):
            return False
    else:
        upper_bound = float(range_.up)
        if any(np.greater(abs_err, upper_bound)):
            return False
    
    return True


class Range(object):
    """
    Range of a parameter defined by lower bound,upper bound and 
    distribution.
    
    The member of the range can be accessed via getter methods, indices 
    or string keys.
    
    Eaxmple:
        x = Range(-3, 7)
        up = x.up
        
        # all statements return the same value:       
        up = x[1]
        up = x['up']
        up = x['hi']
        up = x['max']
        
        y = x.simulate(size=100)
        print(y)
        
        s = str(x)  # ==> (-3, 7, None)
    """
    def __init__(self, *args: Scalar) -> None:
        """
        VarArgs:
            args:
                lower bound, upper bound and/or probability/distribution
        """
        self._lo: Scalar = None
        self._up: Scalar = None
        self._distr: Scalar = None
        self.set_range(*args)
    
    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj        
    
    @property
    def lo(self) -> Scalar:
        return self._lo

    @property
    def up(self) -> Scalar:
        return self._up

    @property
    def distr(self) -> Scalar:
        return self._distr

    @property
    def probality(self) -> Scalar:
        return self._distr
    
    def __getitem__(self, key: Union[int, str]) -> Scalar:
        return self.get_bound(key)

    def get_bound(self, key: Union[int, str]) -> Scalar:
        if isinstance(key, int):
            if key == 0:
                return self._lo
            elif key == 1:
                return self._up
            elif key == 2:
                return self._distr
            else:
                return None
        elif isinstance(key, str):
            key_ = key.lower()
            if key_.startswith(('lo', 'min',)):
                return self._lo
            elif key_.startswith(('up', 'hi', 'max',)):
                return self._up
            elif key_.startswith(('distr', 'prob',)):
                return self._distr
            else:
                return None
        else:
            return None

    def get_range(self) -> Tuple[Scalar, Scalar, Scalar]:
        return (self._lo, self._up, self._distr)

    def set_range(self, *args: Scalar) -> bool:
        self._lo = None
        self._up = None
        self._distr = None
        
        if len(args) == 0:
            return False
        elif len(args) == 1:
            self._up = args[0] 
        elif len(args) == 2:
            self._lo = args[0] 
            self._up = args[1] 
        else:
            self._lo = args[0] 
            self._up = args[1] 
            self._distr = args[2] 
        return True
            
    def simulate(self, size: Optional[Union[int, Tuple[int]]] = None,
                 full_scale: Optional['Range'] = None,
                 plot: bool = False) -> Floats:
        """
        Generates random data in the range [self.lo, self.up] for the 
        following distributions:

            self.dist.startswith(('cont', 'samp', 'flat')):
                continous distribution

            self.dist.startswith(('norm', 'bell', 'gauss')):
                Gaussian distribution with the maximum at (up+lo)/2 
                and a scale of distribution of: +/- (up-lo)/3.]

        Args:
            size:
                size of output array. If size is None, float is returned  
                
            full_scale: 
                range for converting relative to absolute ranges

            plot:
                if True, output and histogram is plotted
                                
        Returns:
            random array of dimension of size if size is not None
            OR
            a float if size is None
            OR
            None if self.distr contains an invalid distribution
            
        """
        if full_scale is not None:
            rng = relative_to_absolute_range(Range(self.lo, self.up, 
                                                   self.distr), full_scale)
            if rng is None:
                return None
            lo, up, distr = rng.lo, rng.up, rng.distr
        else:
            lo, up, distr = self.lo, self.up, self.distr
            
        if up is None:
            print('??? Range.simulate(), up:', up)
            return None
        if lo is None:
            lo = 0
        if distr is None:
            distr = 'gauss'
            
        try:
            lo = float(lo)
        except (TypeError,ValueError) as err:
            print('??? Range.simulate(), err:', err, 'lo:', lo)
            lo = 0.
        try:
            up = float(up)
        except (TypeError,ValueError) as err:
            print('??? Range.simulate(), err:', err,'up:', up)
            up = 1.
  
        if distr.lower().startswith(('cont', 'flat', 'samp')):
            y_ = np.random.random(size=size)
            y = lo + (up - lo) * y_
        elif distr.lower().startswith(('gauss', 'norm', 'bell')):
            y = np.random.normal(loc=(up+lo)/2, scale=np.abs((up-lo)/3.0), 
                                 size=size)            
        else:
            y_ = np.random.normal(size=size)
            y = lo + (up - lo) * y_
             
        if plot:
            n = np.prod(size)
            plt.title('Random generation: ' + self.__str__())
            if distr.lower().startswith(('cont', 'flat', 'samp')):
                plt.plot(y, marker='.', linestyle='', color='blue')
            else:
                y_center = 0.5 * (up + lo)
                dy = 0.607 * (up - y_center) # y-value at x+/-sigma
                if not n:
                    plt.plot(y, marker='.', linestyle='', color='blue')
                else:
                    for i, y_ in enumerate(y): 
                        color = 'blue'
                        if y_center - dy < y_ < y_center + dy: 
                            color= 'red'
                        plt.scatter(x=i, y=y_, marker='.', color=color)
                plt.xlabel(r'red: $\bar y \pm 3 \sigma=' + \
                           str(np.round(y_center, 3)) + ' \pm ' + \
                           str(np.round(dy, 3)) + '$')
            plt.grid()
            plt.show()

            if n:
                plt.title('Random generation: ' + self.__str__())
                plt.hist(y, bins = max(min(n, 4), n // 8))
                plt.grid()
                plt.show()
        return y

    def __str__(self) -> str:
        return str((self._lo, self._up, self._distr))
