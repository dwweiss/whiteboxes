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
      2017-12-07 DWW
"""

from copy import deepcopy
from math import pi, radians
from collections import OrderedDict

from xyz import xyz


class CrossSection(object):
    """
    Defines single cross-section of a pipe. This cross section can be deformed.
    All five points of the compass notation (C, W, E, S, N) can be used.
    Current implementation is limited to (C, E, N) for definition of
    deformation of the ideal circle form.

    The cross sections are intended to be elements in a double linked list.

    Note:
        Cross section points are indexed in compass coordinates:    N
                                                                    |
          ^                                                     W---C---E
          |                                                         |
          N ...                                                     S
          | \  :..               NE_star = (N + E) / 2;
          |   \   NE             (NE - C) = (NE_star - C) * r / r_star
          |  NE*   :.            with r = ((E - C).magnitude() +
          |      \  :.                     (N - C).magnitude()) * 0.5
          |        \ :                r_star = (NE_star - C).magnitude()
          C----------E--->
    """
    def __init__(self, identifier='?'):
        self.identifier = identifier
        self.points = OrderedDict()
        self.points['C'] = xyz(0., 0., 0.)
        self.points['E'] = xyz(1., 0., 0.)
        self.points['N'] = xyz(0., 1., 0.)

        self.rotAxis = None
        self.wayToNext = None

        self.prev = None
        self.next = None

    @property
    def C(self):
        return self.points['C']

    @C.setter
    def C(self, value):
        self.points['C'] = value

    @property
    def W(self):
        return self.points['W']

    @W.setter
    def W(self, value):
        self.points['W'] = value

    @property
    def E(self):
        return self.points['E']

    @E.setter
    def E(self, value):
        self.points['E'] = value

    @property
    def S(self):
        return self.points['S']

    @S.setter
    def S(self, value):
        self.points['S'] = value

    @property
    def N(self):
        return self.points['N']

    @N.setter
    def N(self, value):
        self.points['N'] = value

    @property
    def SW(self):
        return self.points['SW']

    @SW.setter
    def SW(self, value):
        self.points['SW'] = value

    @property
    def SE(self):
        return self.points['SE']

    @SE.setter
    def SE(self, value):
        self.points['SE'] = value

    @property
    def NW(self):
        return self.points['NW']

    @NW.setter
    def NW(self, value):
        self.points['NW'] = value

    @property
    def NE(self):
        return self.points['NE']

    @NE.setter
    def NE(self, value):
        self.points['NE'] = value

    def __str__(self):
        s = "+++ id: '" + '{:10}'.format(str(self.identifier) + "',")
        for compass, coor in self.points.items():
            s += compass + ': [' + '{:7.5f},'.format(coor.x) + \
                '{:7.5f},'.format(coor.y) + '{:7.5f}'.format(coor.z) + '], '
        if self.rotAxis is not None:
            s += 'rot: ' + str(self.rotAxis) + ', '
        if self.wayToNext is not None:
            s += 'way: ' + '{:7.5f}'.format(self.wayToNext)
        return s

    def translate(self, offset):
        for el in self.points.values():
            el.translate(offset)

    def rotate(self, phiRad, rotAxis):
        for el in self.points.values():
            el.rotate(phiRad, rotAxis)

    def scale(self, factor):
        for el in self.points.values():
            el.scale(factor)
        if self.rotAxis is not None:
            for i in [0, 1, 2]:
                if not isinstance(self.rotAxis[i], str):
                    if type(factor) is list:
                        self.rotAxis[i] *= float(factor[i])
                    else:
                        self.rotAxis[i] *= float(factor)

    def diameter(self):
        """
        Returns:
            Equivalent diameter
        """
        return (self.E - self.C).magnitude() + (self.N - self.C).magnitude()

    def area(self):
        """
        Returns:
            Cross-sectional area
        """
        return pi * (self.E - self.C).magnitude() * (self.N -
                                                     self.C).magnitude()

    def normal(self):
        """
        Returns:
            Normal vector
        """
        n = self.vectorProduct(self.E - self.C, self.N - self.C)
        return n / n.magnitude()

    def extractRotationData(self):
        """
        Extracts rotation data from 'rotAxis' list which must contain one
            string and two floats; the rotation is around the axis for which
            the  angle is given as string;
        angle string can optionally end with 'deg' or 'rad';
        in case of 'deg', the angle is converted to radians

        Returns:
            modified rotation axis (angle string replaced with 'None'),
            bending radius [m], rotation angle [rad];
            ('None','None','None') is returned if rotAxis equals 'None'

        Example:
            rotAxis: [1.2, '90deg', 2.3] -> rotation around y-axis with
            an angle of 90 degrees, rotation center is (x=1.2, z=2.3)
        """
        if self.rotAxis is None or len(self.rotAxis) < 3:
            return (None, None, None)

        if isinstance(self.rotAxis[0], str):
            i = 0
        elif isinstance(self.rotAxis[1], str):
            i = 1
        elif isinstance(self.rotAxis[2], str):
            i = 2
        else:
            self.write('??? rotAxis does not contain the angle string')
            return (None, None, None)

        j = self.rotAxis[i].lower().find('deg')
        if j != -1:
            phiInRad = radians(float(self.rotAxis[i][:j]))
        else:
            j = self.rotAxis[i].lower().find('rad')
            if j != -1:
                phiInRad = float(self.rotAxis[i][:j])
            else:
                phiInRad = float(self.rotAxis[i])
        rot = deepcopy(self.rotAxis)
        rot[i] = None

        if i == 0:
            rBend = (self.C - xyz(self.C.x, rot[1], rot[2])).magnitude()
        elif i == 1:
            rBend = (self.C - xyz(rot[0], self.C.y, rot[2])).magnitude()
        elif i == 2:
            rBend = (self.C - xyz(rot[0], rot[1], self.C.z)).magnitude()

        return (rot, rBend, phiInRad)

    def wayToNextCenter(self):
        if self.next is None:
            return None
        elif self.rotAxis is None:
            return (self.next.C - self.C).magnitude()
        else:
            (rotAxisModified, rBend, phiInRad) = self.extractRotationData()
            return rBend * phiInRad


# Examples ###################################################################
            
if __name__ == '__main__':
    foo = CrossSection()
    print(foo)
