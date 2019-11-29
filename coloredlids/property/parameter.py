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
      2019-11-28 DWW
"""

__all__ = ['Parameter']

import collections
from typing import Dict, Optional, Sequence, Tuple, Union
import numpy as np
import matplotlib.pyplot as plt

from coloredlids.property.range import (Range, Floats, 
    percentage_of_bound, is_bound_absolute, is_bound_relative_to_reading) 


class Parameter(object):
    """
    Defines a parameter with:
      - identifier (raw string and and latex version),
      - actual value,
      - reference value,
      - absolute/relative flag,
      - unit,
      - accuracy (absolute, relative to reading '%',
                  relative to full scale '%FS'),
      - repeatability,
      - dictionary of ranges (lower and upper bounds of valid values) 
      - sampling rate,
      - rate-of-change (d(Parameter)/dt)
      - trust score
      

                            identifier [unit] 
                                  ^    
                                  |
      <-- error related ranges--> | <--- VAL related ranges ---->
          (VAL<->REF relation)    |    (no reference to REF) 
      --------------------------- | -----------------------------
        ('expected', 'tolerated') | ('calibrated', 'operational')
                                  |
                                  |------------------
                                  |                ^
                                  |------------    |
             ........             |          ^     | 
              ^                   |          |     | 
              :    .............. X VAL .... | c   | o
              t     ^             |          | a   | p
              o     : diff.                  | l   | e
              l     : between     |          | i   | r
              r     : val         |          | b   | a
              a     : and         |          | r   | t
              t     : ref         |          | a   | i
              e     v             |          | t   | o
              d    .......... REF o          | e   | n
              :                   |          v d   | a 
              :                   |------------    | l
              v                   |                |  
             .........            |                |  
                                  |                v
                                  |------------------
                                  |
        
      Notes:
          np.isscalar(x) returns True if x is of one of these types 
    """

    def __init__(self, identifier: str = 'Parameter',
                 unit: str = '/',
                 absolute: bool = True,
                 latex: Optional[str] = None,
                 val: Floats = None,
                 ref: Floats = None,
                 range_keys: Optional[Sequence[str]] = None,
                 comment: Optional[str] = None) -> None:
        """
        Args:
            identifier:
                parameter identifier (raw string)
                
            unit:
                measurement unit
                
            absolute:
                if True, values and tolerances are absolute 
                (temperature in Kelvin & pressure is not gauge pressure)
                
            latex:
                parameter identifier (latex notation, e.g. r'\varrho') 
                If None, latex is identical with indentifier
                
            val:
                actual value(s)
                
            ref:
                reference value(s)
                
            range_keys:
                list of keys of default ranges. If None, a list of
                default ranges will be assigned.
                
            comment:
                comment text 

        Note:
            Method __call__() returns self.val of type Floats
            
            Bounds og value ranges or of repeatability range can be:
                - absolute (e.g. 1.2),
                - relative to full scale (e.g. '1.2%FS')

            Bounds of accuracy range can be:
                - absolute (e.g. 1.2 or '1.2'),
                - relative to reading (e.g. '1.2%') or
                - relative to full scale (e.g. '1.2%FS')

        """
        self.identifier: str = identifier
        self.unit: str = unit
        if self.unit[0] != '[':
            self.unit = '[' + self.unit
        if self.unit[-1] != ']':
            self.unit = self.unit + ']'
        self.absolute: bool = bool(absolute)        
        
        if latex:
            self.latex: str = latex        # Latex symbol, e.g. '\alpha' 
        else:
            self.latex: str = self.identifier
        if len(self.latex) > 0:
            if self.latex[0] != '$':
                self.latex = '$' + self.latex
            if self.latex[-1] != '$':
                self.latex = self.latex + '$'
        
        self._val: Floats = val
        self._ref: Floats = ref
        
        if len(np.atleast_1d(self.val)) != len(np.atleast_1d(self.ref)):
            print("!!! 'val' and 'ref' are arrays of different size:",
                  (self.val.dim, self.ref.dim))
        
        if range_keys is None:
            range_keys = ('calibrated', 'tolerated', 'full_scale', 'expected')
                
        self._ranges: Dict[str, Range] = {}
        if range_keys:
            for key in range_keys:
                self._ranges[key] = Range()

        self._ranges['full_scale'] = Range(0., 100., None)
        self._ranges['calibrated'] = Range('-0.5%', '+0.5%', None)
        self._ranges['accuracy'] = Range('-1%', '+1%', None)
        self._ranges['repeatability'] = Range(-0.01, 0.01, '95%')

        self.comment: str = comment if comment is not None else ''

        self.sampling: float = 100.                              # [1/s]
        self.rate_of_change: float = 0.                # [(self.unit)/s]
        self.trust_score: int = 10  # confidence, 10: excellent, 0: poor

    def __call__(self) -> Floats:
        """
        Returns:
            actual value 
        """
        return self.val

    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    @property
    def ranges(self) -> Dict[str, Range]:
        """          
        Returns:
            dictionary of ranges (lo, up, distr)

        Example:
            foo = Parameter(range_keys=['expected'])
            foo.ranges['expected'] = (-1.2, '3%', None)

            rng = foo.ranges['expected']
            print(rng)
            # ==> (-1.2, '3%', None) 

            rng = foo.ranges.get('unknown_key')
            print(rng)
            # ==> None

            # add key to dictionary 
            foo.ranges['critical'] = (-np.inf, np.inf, None)
            rng = foo.ranges.get('critical')
            print(rng)
            # ==> (-inf, inf, None)
        """
        return self._ranges        

    def __getitem__(self, key: str) -> Union[Floats, Range]:
        """
        Args:
            key:
                key of parameter range
            
        Returns:
            self._ranges[key] as tuple of lower/upper bound,distribution 
            or 
            self.val if key is 'val'
            or 
            self.ref if key is 'ref' 
            or 
            self.accuracy if key is 'accuracy' 
            or 
            self.repeatability if key is 'repeatability' 
            or 
            None if key is unknown

        Examples:
            foo = Parameter(value_range_keys=('expected'))
            foo['expected'] = Range(-1.2, 3.4)
            # ...
            rng = foo['expected']
            print(rng)
            # ==> (-1.2, 3.4, None)

            rng = foo['unknown_key']
            print(rng)
            # ==> None
            
            foo.val = [3.45, 1.1, 2.2]
            # ...
            print(foo.val)
            # ==> [3.45, 1.1, 2.2]
            print(foo['val'])
            # ==> [3.45, 1.1, 2.2]

            foo.ref = 3.45
            # ...
            print(foo.ref)
            # ==> 3.45
            print(foo['ref'])
            # ==> 3.45
            
            foo.accuracy = Range(-0.01, 0.01, '95%')
            print(foo.accuracy)
            # ==> (-0.01, 0.01, '95%')
            print(foo['accuracy'])
            # ==> (-0.01, 0.01, '95%')
        """
        return self.get_range(key)
        
    def __setitem__(self, key: str, value: Union[Floats, Range]) -> bool:
        """
        Args:
            key:
                key of parameter range 
            
            value:
                tuple of lower and upper bound of range + distribution 
                If key is 'val', value is a float or an array of float
                If key is 'ref', value is a float or an array of float
    
        Returns: 
            False is key is unknown
    
        Examples:
            foo = Parameter()
            
            foo.set_range('val', [1.1, 2.2, 3.3])
            val = foo.val
            print(val)
            # ==> [1.1, 2.2, 3.3]    

            foo.set_range('ref', 2.3456)
            ref = foo.ref
            print(ref)
            # ==> 2.3456    
            
            foo.set_range('expected', 3.4) 
            rng = foo['expected']
            print(rng)
            # ==> (0.0, 1.2) 

            foo.set_range('critical', -1.2) 
            rng = foo['critical']
            print(rng)
            # ==> (-1.2, 0.0) 

            foo.set_range('tolerated', -1.2, '5.6%') 
            rng = foo['tolerated']
            print(rng)
            # ==> (-1.2, '5.6%')  
        """
        return self.set_range(key, value)

    def set_range(self, key: str, value: Union[Floats, Range, 
                                               Sequence[float]])-> bool:            
        if key.lower().startswith('val'):
            self.val = value
        elif key.lower().startswith('ref'):
            self.ref = value
        else:
            if isinstance(value, (collections.Sequence,)):
                lo, up, distr = None, None, None
                if len(value) > 0:
                    lo = value[0] 
                if len(value) > 1:
                    up = value[1] 
                if len(value) > 2:
                    distr = value[2] 
                self.ranges[key] = Range(lo, up, distr)
            elif isinstance(value, Range):
                self.ranges[key] = value
            else:
                assert 0
        return True

    def get_range(self, key: str) -> Union[Floats, Range]:
        """
        See __getitem__()
        """
        if key is None:
            return None
        elif key == 'val':
            return self.val
        elif key == 'ref':
            return self.ref
        else:
            return self._ranges.get(key)

    @property
    def val(self) -> Floats:
        return self._val

    @val.setter
    def val(self, value: Floats) -> None:
        self._val = value

    @property
    def value(self) -> Floats:
        return self._val

    @value.setter
    def value(self, value: Floats) -> None:
        self._val = value

    @property
    def ref(self) -> Floats:
        return self._ref

    @ref.setter
    def ref(self, value: Floats) -> None:
        self._ref = value

    @property
    def reference(self) -> Floats:
        return self._ref

    @reference.setter
    def reference(self, value: Floats) -> None:
        self._ref = value

    @property
    def full_scale(self) -> Optional[Range]:
        return self._ranges.get('full_scale')

    @full_scale.setter
    def full_scale(self, value: Range) -> None:
        self._ranges['full_scale'] = value

    @property
    def calibrated(self) -> Optional[Range]:
        return self._ranges.get('calibrated')

    @calibrated.setter
    def calibrated(self, value: Range) -> None:
        self._ranges['calibrated'] = value

    @property
    def accuracy(self) -> Optional[Range]:
        return self._ranges.get('accuracy')

    @accuracy.setter
    def accuracy(self, value: Range) -> None:
        self._ranges['accuracy'] = value

    @property
    def repeatability(self) -> Optional[Range]: 
        return self._ranges.get('repeatability')

    @repeatability.setter
    def repeatability(self, value: Range) -> None:
        self._ranges['repeatability'] = value

    def simulate(self, range_key: Optional[str] = None, 
                 size: Optional[Union[int, Tuple[int]]] = None,
                 plot: bool = False) -> Floats:
        """
        Simulates values within absolute and relative 
        (to full_scale/reading) ranges 
        
        Bounds relative to reading are calculated as percentages 
        of the elements of an already assigned self.ref array
        
        Args:
            range_key:
                key of the range bounding the output
                
            plot:
                plot simulated array(s) if True
                
        Returns:
            False if range_key is invalid or self.ref is empty in case 
            that a bound is relative to reading, eg. (-1, '10%', None)
        """
        if range_key is None:
            range_key = 'calibrated'
        if range_key not in self.ranges:
            return False
        if size is None and self.ref is not None:
            size = self.ref.size

        rng = self.ranges[range_key]
        
        if not is_bound_relative_to_reading(rng.lo) \
               and not is_bound_relative_to_reading(rng.up):
            
            # None of the bounds is relative to reading
            self.val = rng.simulate(size=size, 
                                    full_scale=self.full_scale, plot=plot)
            # add random data to reference array if reference exists 
            if self.ref is not None:
                self.val = self.ref + self.val
        else:
            # One or both of the bounds is relative to reading
            if self.ref is None:
                return None
            val = []
            for ref_ in np.atleast_1d(self.ref):
                if is_bound_absolute(rng.lo):
                    lo = float(rng.lo)
                else:
                    perc = percentage_of_bound(rng.lo)
                    if is_bound_relative_to_reading(rng.lo):
                        lo = perc * ref_
                    else:
                        lo = np.abs(perc) * self.full_scale.lo
            
                if is_bound_absolute(rng.up):
                    up = float(rng.up)
                else:
                    perc = percentage_of_bound(rng.up)
                    if is_bound_relative_to_reading(rng.up):
                        up = perc * ref_
                    else:
                        up = np.abs(perc) * self.full_scale.up
                val_ = Range(lo, up, rng.distr).simulate()
                val.append(val_)
                
            # add random data to reference array 
            self.val = self.ref + np.asfarray(val)
            
            if plot:
                plt.plot(self.val, label='val', linestyle='', marker='.')
                if is_bound_relative_to_reading(rng.lo) or \
                   is_bound_relative_to_reading(rng.up):
                    plt.plot(self.ref, label='ref', linestyle='', marker='.')
                    plt.legend()
                plt.grid()
                plt.show()
                
        return self.val
            
    def __str__(self) -> str:
        s = '\n{'
        d = collections.OrderedDict(sorted(self.__dict__.items()))
        
        for key, val in d.items():
            s += "  '" + key + "': "
            if isinstance(val, str):
                s += "'" + str(val) + "'"
            else:
                s += str(val)
            s += ',\n '
        s += '}'
        return s