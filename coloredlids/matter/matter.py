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
      2018-09-17 DWW
"""

from typing import Optional, Sequence, Union

from grayboxes.base import Base
from genericmatter import GenericMatter
import ferrous
import nonferrous
import nonmetals
import liquids
import gases


class Matter(Base):
    """
    Collection of physical and chemical properties of matter

    Note:
        The class is designed as a follower in theoretical submodel tree
    """

    def __init__(self, identifier: str='Matter') -> None:
        """
        Args:
            identifier:
                Identifier of collection of matter
        """
        super().__init__(identifier=identifier)
        self.program = self.__class__.__name__

        classes = []
        matter = (ferrous, nonferrous, nonmetals, liquids, gases)
        for md in matter:
            classes += [v() for c, v in md.__dict__.items()
                        if isinstance(v, type) and
                        v.__module__.lower() == md.__name__.lower()]
        self.data = {}
        for mat in classes:
            self.data[mat.identifier.lower()] = mat

    def __call__(self, identifier: Optional[str]=None) \
            -> Optional[Union[GenericMatter, Sequence[GenericMatter]]]:
        """
        Select specific matter

        Args:
            identifier:
                Identifier of matter.
                If None or 'all', then all matter will be returned

        Returns:
            - Selected matter or:
            - List all matter if identifier is None or 'all' or
            - None if identifier is unknown

        Example:
            collection = Matter()
            mat = collection('iron')
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
            String of keys list of available matter
        """
        return str(self.data.keys())
