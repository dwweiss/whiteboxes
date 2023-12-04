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
      2020-11-04 DWW
"""

__all__ = ['Range',
           'relative_to_absolute_range', 'percentage_of_bound', 
           'in_range', 'in_range_full_scale', 'in_range_abs_rel_error',
           'is_bound_absolute',
           'is_bound_relative_to_reading', 'is_bound_relative_to_full_scale',
           'is_range_absolute',
           'is_range_relative_to_reading', 'is_range_relative_to_full_scale',]

import numpy as np
np.random.seed(19680801)

import matplotlib.pyplot as plt
from typing import Iterable, Optional, Tuple, Union
    

def percentage_of_bound(bound: Union[None, float, int, str]) \
        -> Optional[float]:
    """
    converts argument to float, 
    multiplies float with 1e-2 if argument is str and argument contains '%'
    """
    if '%' in str(bound):
        return float(bound[:bound.find('%')]) * 1e-2
    else:
        return bound


def is_bound_relative_to_reading(bound: Union[None, float, int, str], 
                                 full_scale_pattern: str = '%FS') -> bool:
    """
    Returns:
        True if bound contains '%' and bound does not contain '%FS'
    """
    return '%' in str(bound) and full_scale_pattern not in str(bound).upper()


def is_range_relative_to_reading(range_: 'Range') -> bool:
    """
    Returns:
        True if both bounds of range_ contain '%' and both do not contain '%FS'
    """
    return is_bound_relative_to_reading(range_.lo) \
       and is_bound_relative_to_reading(range_.up)


def is_bound_relative_to_full_scale(bound: Union[None, float, int, str], 
                                    full_scale_pattern: str = '%FS') -> bool:
    """
    Returns:
        True if bound contains '%FS'
    """
    return full_scale_pattern in str(bound).upper()


def is_range_relative_to_full_scale(range_: 'Range', 
                                    full_scale_pattern: str = '%FS') -> bool:
    """
    Returns:
        True if both bounds of range_ contain '%FS'
    """
    return is_bound_relative_to_full_scale(range_.lo, full_scale_pattern) \
       and is_bound_relative_to_full_scale(range_.up, full_scale_pattern)


def is_bound_absolute(bound: Union[None, float, int, str]) -> bool:
    """
    Returns:
        True if bounds does not contain '%' and can be converted to float
    """
    try:
        float(bound)
        return True
    except:
        return False

def is_range_absolute(range_: 'Range') -> bool:
    """
    Returns:
        True if both bounds do not contain '%' and can be converted to float
    """
    return is_bound_absolute(range_.lo) and is_bound_absolute(range_.up)


def relative_to_absolute_range(range_: 'Range', 
                               full_scale: 'Range',
                               relative_pattern: str = '%') \
        -> Optional['Range']:
    """
    Calculates absolute values of bounds of 'range_' which are defined
    relative to span of 'full_scale'. Relative bounds are of type str
    and must contain '%' after the number, e.g. '2%' or '-5%FS'

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
        full_scale = Range(-11., 22.)           # span = 22.-(-11.) = 33
        rng = relative_to_absolute_range(range_, full_scale)
        
        # upper bound of range_ is already absolute
        print(rng)  # => (-0.33, 4.) 
        
    Note:
        If range_[i] is of type int or float, full_scale[i] is 
        ignored  
        
        The function tolerates that: 
            one or all bounds of range_ are of type float or int
            one or all bounds of range_full_scale are of type str
            
            
                                   -----------------------
                                   |                     |
                                   |                   '-10%' -> -0.1 
                                   |       full_scale    |
    relative_to_absolute_range(('-10%', 7), (-3, 8))     V
                                   range      |  |     -0.1*(11) -> lo:-1.1
                                              v  v            ^
                                            span: 11          |
        lo is lower bound and up is            |              |
        upper bound of effective range         ----------------
        
                                   # full scale span = 8-(-3) = 11 is 
                                   # multiplied with -10e-2 => -1.1 
                                   # range_.up = 7 stays unchanged
    """
    if not isinstance(range_, Range):
        return None
    
    lo = range_.lo
    up = range_.up
    distr = range_.distr 

    is_lo_relative = lo is not None and not is_bound_absolute(lo) 
    is_up_relative = up is not None and not is_bound_absolute(up) 
    
    # if range_.lo is absolute, full_scale.lo can can have any value 
    if is_lo_relative:
        if not isinstance(full_scale, Range) \
               or not is_bound_absolute(full_scale.lo):
            return None

    # if range_.up is absolute, full_scale.up can can have any value 
    if is_up_relative:
        if not isinstance(full_scale, Range) \
               or not is_bound_absolute(full_scale.up):
            return None

    if is_lo_relative or is_up_relative:
        if distr is None:
            distr = full_scale.distr
        try:
            span = float(full_scale.up) - float(full_scale.lo)
        except (TypeError, ValueError):
            return None

    if is_lo_relative:    
        try:
            lo = float(range_.lo[:range_.lo.find('%')]) * 1e-2
        except (TypeError, ValueError):
            return None
        lo *= span

    if is_up_relative:    
        try:
            up = float(range_.up[:range_.up.find('%')]) * 1e-2
        except (TypeError, ValueError):
            return None
        up *= span
 
    return Range(lo, up, distr)


def in_range(val: Union[None, float, Iterable[float]], 
             range_: 'Range') -> bool:
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
    if val is None or range_ is None:
        return False
    
    try:
        val = [float(x) for x in np.atleast_1d(val)]
    except (TypeError) as err:
        print('??? in_range():', err, 'val:', val)
        return False
    try:
        lo, up = float(range_[0]), float(range_[1])
    except (TypeError) as err:
        print('??? in_range():', err, 'val:', 'range_:', range_)
        return False
    
    if lo > up:
        lo, up = up, lo
        print('!!! in_range(): swap', (up, lo), '==>', (lo, up))

    return all(np.greater_equal(val, lo)) and all(np.less_equal(val, up))


def in_range_full_scale(val: Union[None, float, Iterable[float]], 
                        range_: 'Range', 
                        full_scale: 'Range') -> bool:
    """
    Checks if val is within span of 'range_' which can be defined
    absolute or relative to 'full_scale'. Relative bounds are of type 
    str and must contain character '%' after the number, e.g. '-1.2%'

    Args:
        val:
            actual value as scalar (int, float, str) or sequence of it 
        
        range_:
            range with relative or absolute bounds: 7, '7' or '2%'

        full_scale:
            range with absolute bounds: eg. -3 or '-3'
            
    Returns:        
        True if val or all elements of val within the given bounds
    """
    converted_range = relative_to_absolute_range(range_, full_scale)
    if converted_range is None:
        return False
    
    return in_range(val, converted_range)


def in_range_abs_rel_error(val: float, 
                           ref: float, 
                           range_: 'Range') -> bool:
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
    
                              y ^    simulate():
                                |
         up  -----   - - - - -  +    x    x    x
          ^  | R |              |      x      x    x
          |  | a |              |          x    x 
          |  | n |              |            x    x
          |  | g |              |        x       x  x
          v  | e |              |   x       x
         lo  -----   - - - - -  + 
                                |
                                ---------------------> x
    Eaxmple:
        rng = Range(-3, 7)
        up = rng.up
        
        # all statements return the same value:       
        up = rng[1]
        up = rng['up']
        up = rng['hi']
        up = rng['max']
        
        y = rng.simulate(size=100)
        print(y)
        
        s = str(rng)  # ==> (-3, 7, None)
    """
    def __init__(self, *args: Union[None, float, int, str]) -> None:
        """
        VarArgs:
            args:
                lower bound, upper bound and/or probability/distribution
        """
        self._lo: Union[None, float, int, str] = None
        self._up: Union[None, float, int, str] = None
        self._distr: Union[None, float, int, str] = None
        self.set_range(*args)
    
    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj        
    
    @property
    def lo(self) -> Union[None, float, int, str]:
        return self._lo

    @property
    def up(self) -> Union[None, float, int, str]:
        return self._up

    @property
    def distr(self) -> Union[None, float, int, str]:
        return self._distr

    @property
    def probability(self) -> Union[None, float, int, str]:
        return self._distr
    
    def __getitem__(self, key: Union[int, str]) \
            -> Union[None, float, int, str]:
        return self.get_bound(key)

    def get_bound(self, key: Union[int, str]) -> Union[None, float, int, str]:
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
            elif key_.startswith(('span', 'delta',)):
                return self.span()
            else:
                return None
        else:
            return None

    def get_range(self) -> Tuple[Union[None, float, int, str], 
                                 Union[None, float, int, str], 
                                 Union[None, float, int, str]]:
        return (self._lo, self._up, self._distr)

    def set_range(self, *args: Union[None, float, int, str]) -> bool:
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
            
    def span(self) -> Optional[float]:
        try:
            return float(self._up) - float(self._lo)
        except:
            return None
        
    def simulate(self, size: Union[None, int, Tuple[int]] = None,
                 full_scale: Optional['Range'] = None,
                 plot: bool = False) -> Union[None, float, np.ndarray]:
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
