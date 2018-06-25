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
      2018-06-25 DWW
"""

from . parameter import C2K
from grayboxes.base import Base

from . nonmetals import NonMetals
from . nonferrousmetals as NonFerrousMetals
from . ferrousmetals as FerrousMetals
from . liquids import Liquids
from . gases import Gases


def molecularWeight(identifier):
    """
    Args:
        identifier (string):
            Element or organic compound

    Returns:
        (float):
            Molecular weight (molar mass) in [kg/mol]

    Reference:
        https://www.lenntech.com/calculators/molecular/
        molecular-weight-calculator.htm
    """
    first = identifier[0].upper()
    if first == 'A':
        if   identifier == 'Ar':     return 39.95e-3
    elif first == 'C':
        if   identifier == 'C':      return 12.01e-3
        elif identifier == 'CO2':    return 44.01e-3
        elif identifier == 'CH4':    return 16.04e-3
        elif identifier == 'C2H4':   return 28.05e-3
        elif identifier == 'C2H5OH': return 12.01e-3
        elif identifier == 'C2H6':   return 30.07e-3
        elif identifier == 'C3H6':   return 42.07e-3
        elif identifier == 'C3H8':   return 44.01e-3
        elif identifier == 'C4H10':  return 58.12e-3
    elif first == 'H':
        if   identifier =='H':       return 1.008e-3
        elif identifier =='He':      return 4.003e-3
        elif identifier =='H2O':     return 18.02e-3
        elif identifier =='H2S':     return 34.08e-3
    elif first == 'N':
        if identifier =='N2':        return 28.01e-3
    elif first == 'O':
        if   identifier =='O':       return 16.00e-3
        elif identifier =='O2':      return 32.00e-3

    assert 0, 'identifier:' + str(identifier)
    return None


class Matter(Base):
    """
    Collection of physical and chemical properties of matter

    Intended to be a follower of root in a Base-based tree

    Args:
        identifier (string, optional):
            identifier of collection of matter
    """
    def __init__(self, identifier='Matter'):
        super().__init__(identifier=identifier)
        self.program = self.__class__.__name__
        self.version = '150917_dww'

        classes = []
        for md in [FerrousMetals, NonFerrousMetals, NonMetals, Liquids, Gases]:
            classes += [v() for c, v in md.__dict__.items()
                        if isinstance(v, type) and
                        v.__module__ == md.__name__]

        self.data = {}
        for mat in classes:
            self.data[mat.identifier.lower()] = mat

    def __call__(self, identifier=None):
        if identifier is None or identifier == 'all':
            return self.data.values()
        if identifier.lower() not in self.data:
            self.write('??? unknown identifier of matter: ', identifier)
            return None
        return self.data[identifier.lower()]

    def __str__(self):
        """
        Returns:
            (array of string):
                array of keys of available matter
        """
        return str(self.data.keys())


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 1

    if 1 or ALL:
        print('collection:', [m.identifier for m in Matter()('all')])

    if 0 or ALL:
        matter = Matter()
        for mat in matter('all'):
            print('mat:', mat.identifier)
            if 1:
                mat.plot()

    if 0 or ALL:
        s = 'Water'
        print('-' * len(s) + '\n' + s + '\n' + '-' * len(s))

        collection = Matter()
        print('Collection:', collection)  # dict_keys(['304','Ryton','Water'])
        mat = collection('water')
        mat.plot('c_p')

        rho = mat.plot('rho')
        Lambda = mat.Lambda(T=C2K(100))
        print('Lambda:', Lambda)
        c_p = mat.c_p(T=C2K(20), p=mat.p.ref)

        mat.plot('all')
