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
      2020-12-13 DWW
"""

from collections import OrderedDict
from typing import List, Optional, Union

from coloredlids.matter import ferrous
from coloredlids.matter import gases
from coloredlids.matter import liquids
from coloredlids.matter import nonferrous
from coloredlids.matter import nonmetals
from coloredlids.property.matter import Matter
from grayboxes.base import Base


class Matters(Base):
    """
    Convenience class providing properties of all matter in modules:
        (ferrous, nonferrous, nonmetals, liquids, gases)
        
    Note:
        For getting a list of all available matter write:
            collection: matter = Matter() 
            all_matter: str = collection('all') 
    """

    def __init__(self, identifier: str = 'Matters') -> None:
        """
        Args:
            identifier:
                Identifier of collection of matter
        """
        super().__init__(identifier=identifier)        
        self.program = self.__class__.__name__

        classes = []
        matter = (ferrous, nonferrous, nonmetals, liquids, gases,)
        for mat in matter:
            classes += [class_() for key, class_ in mat.__dict__.items()
                        if isinstance(class_, type) and 
                        key[0] != '_' and
                        mat.__name__[0] != '_' and
                        class_.__module__.lower() == mat.__name__.lower()]
        self.data = OrderedDict()
        for class_ in classes:
            self.data[class_.identifier.lower()] = class_

    def __call__(self, identifier: Optional[str] = None) \
            -> Optional[Union[Matter, List[Matter]]]:
        """
        Select specific matter

        Args:
            identifier:
                Identifier of matter.
                If None or 'all', then all matter will be returned

        Returns:
            Selected matter 
            or 
            list of all matter if identifier is None
            or 
            None if identifier is invalid

        Example:
            matter = Matter()
            iron = matter('iron')
            
        """
        if identifier is None or identifier == 'all':
            return self.data.values()
        if identifier.lower() not in self.data:
            self.write('??? unknown identifier of matter: ' + identifier)
            return None
        return self.data[identifier.lower()]

    def __str__(self) -> str:
        """
        Returns:
            List of String of keys list of available matter
        """
        return str(self.data.keys())    
