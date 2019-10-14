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

from copy import deepcopy

from grayboxes.base import Base
from grayboxes.xyz import xyz
from grayboxes.plot import plot_trajectory
from coloredlids.mesh.cross_section import CrossSection


class PipeworkBase(Base):
    """
    Double-linked list of cross sections forming a pipework with straight pipe
    segment, bows and pipe expansion and reductions.
    """

    def __init__(self, identifier='', argv=None):
        super().__init__(identifier, argv)
        self.head = None
        self.tail = None
        self.way = 0.

    def __str__(self):
        s = ''
        crossSection = self.head
        while crossSection is not None:
            s += str(crossSection) + '\n'
            crossSection = crossSection.next
        return s

    def get(self, identifier):
        crossSection = self.head
        while crossSection is not None:
            if crossSection.identifier == identifier:
                return crossSection
            crossSection = crossSection.next
        return None

    def n_cross_section(self):
        return len(self.keys())

    def n_pipe_section(self):
        return max(0, self.nCrossSection() - 1)

    def keys(self):
        k = []
        crossSection = self.head
        while crossSection is not None:
            k.append(crossSection.identifier)
            crossSection = crossSection.next
        return k

    def set_begin(self, identifier, C, E, N):
        """
        Sets characteristic points (C, E, N) of initial cross section

        Args:
            identifier (string):
                identifier of cross-section

            C, E, N (xyz):
                center, east and north point defining circle area

        Returns:
            Reference to cross section
        """
        self.head = CrossSection(identifier)
        self.head.C = xyz(C[0], C[1], C[2])
        self.head.E = xyz(E[0], E[1], E[2])
        self.head.N = xyz(N[0], N[1], N[2])
        self.tail = self.head
        return self.head

    def add(self, identifier, offset=None, rotAxis=None, scaling=None):
        """
        Adds an existing cross section with an unique identifier to pipework

        Args:
            identifier (string):
                identifier of cross-section

            offset (tuple/list of float):
                list of offsets in x-, y-, z-direction

            rotAxis (tuple/list of float/string):
                list of rotation axis, one component is a string containing
                rotation angle, optional with postfix 'deg'

            scaling (tuple/list of float):
                list of scaling of cross-section in default position
                (x-y-plane)

        Returns:
            (binding): 
                to tail cross section
        """
        if self.head is None:
            self.head = CrossSection(identifier)
            self.tail = self.head
        else:
            previous = self.tail
            previous.next = deepcopy(previous)
            self.tail = previous.next
            self.tail.identifier = identifier
            self.tail.prev = previous
            self.tail.prev.rotAxis = rotAxis

        if scaling is not None:
            self.tail.scale(scaling)
        if offset is not None:
            self.tail.translate(offset)
        if rotAxis is not None:
            self.tail.prev.rotAxis = rotAxis
            (rotAxisModified, rBend, phiInRad) = \
                self.tail.prev.extractRotationData()
            self.tail.rotate(phiInRad, rotAxisModified)
        return self.tail

    def pre(self):
        super().pre()

        self.way = 0.
        crossSection = self.head
        while crossSection is not None and crossSection.next is not None:
            crossSection.wayToNext = crossSection.wayToNextCenter()
            self.way += crossSection.wayToNext
            crossSection = crossSection.next

        self.write('+++ nCrossSection: ' + str(self.nCrossSection()))
        self.write('+++ nPipeSection: ' + str(self.nPipeSection()))
        self.write('+++ keys: ' + str(self.keys()))
        self.write('+++ way: ' + str(self.way))
        self.write('+++ ' + str(self))
        if not self.silent:
            self.plot()

    def plot(self):
        if self.head is None or self.head.next is None:
            return
        crossSection = self.head
        x, y, z = [], [], []
        x2, y2, z2 = [], [], []
        x3, y3, z3 = [], [], []
        crossSection = self.head
        while crossSection is not None:
            #  (x, y, z) plots triangle C-E-N-C of all sections (blue lines)
            x.append(crossSection.C.x)
            x.append(crossSection.E.x)
            x.append(crossSection.N.x)
            x.append(crossSection.C.x)
            y.append(crossSection.C.y)
            y.append(crossSection.E.y)
            y.append(crossSection.N.y)
            y.append(crossSection.C.y)
            z.append(crossSection.C.z)
            z.append(crossSection.E.z)
            z.append(crossSection.N.z)
            z.append(crossSection.C.z)

            # (x2, y2, z2) connects E-points of all sections (green lines)
            x2.append(crossSection.E.x)
            y2.append(crossSection.E.y)
            z2.append(crossSection.E.z)

            # (x3, y3, z3) connects N-points of all sections (red lines)
            x3.append(crossSection.N.x)
            y3.append(crossSection.N.y)
            z3.append(crossSection.N.z)

            crossSection = crossSection.next

        plot_trajectory(x, y, z, x2, y2, z2, x3, y3, z3,
                       labels=['x', 'y', 'z', 'C', 'E', 'N'])

    def scale(self, factor):
        crossSection = self.head
        while crossSection is not None:
            crossSection.scale(factor)
            crossSection = crossSection.next
        return None

    def task(self):
        super().task()

    def post(self):
        super().post()


class Pipework(PipeworkBase):
    """
    Double-linked list of cross section forming a pipework with test geometries

    Returns:
        Reference to head cross section
    """
    def __init__(self, identifier='', argv=None):
        super().__init__(identifier, argv)

    def create_double_out_of_plane_bends(self, r_pipe=15e-3*0.5):
        """
        create test geometry 1: 'double out-of-plane bends + straight segment'
        """
        rBow = (r_pipe * 2) * 1.5
        lOutSegment = 2 * (2 * r_pipe)

        hasCEN = True
        if hasCEN:
            C = (-rBow, -2*rBow,  -rBow)
            E = (C[0], C[1]-r_pipe, C[2])
            N = (C[0], C[1], C[2]-r_pipe)
            self.setBegin('begin', C, E, N)
        else:
            cs = self.add('begin', offset=None, rotAxis=['-90deg', -rBow, 0],
                          scaling=[r_pipe, r_pipe, 0])
            cs.rotate([-rBow, -rBow, '-90deg'])
        self.add('middle1', offset=None, rotAxis=[-rBow, -rBow, '90deg'])
        self.add('middle2', offset=None, rotAxis=['90deg', -rBow, 0])
        self.add('end', offset=[0., 0., lOutSegment])

        return self.head

    def create_straight_pipe(self, rPipe=15e-3*0.5, lPipe=1.):
        """
        create pipe as test geometry 2
        """
        self.add('begin', scaling=[rPipe, rPipe, 0])
        self.add('end', offset=[0., 0., lPipe])


# Examples ####################################################################

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.abspath('../..'))
    sys.path.append(os.path.abspath('../../../grayboxes'))

    
    
    foo = Pipework()

    if 1:
        r_pipe = 15e-3 * 0.5
        l_pipe = 0.5
        foo.create_straight_pipe(r_pipe, l_pipe)
        print('foo:', foo)

    if 1:
        r_pipe = 15e-3 * 0.5
        l_pipe = 0.5
        foo.create_double_out_of_plane_bends(r_pipe)
        print('foo:', foo)

    if 1:
        r_pipe = 15e-3 * 0.5
        r_bow = (r_pipe * 2) * 1.5
        l_out_segment = r_bow  # 2 * (2 * rPipe)

        C = (-r_bow, -2*r_bow,  -r_bow)
        E = (C[0], C[1]-r_pipe, C[2])
        N = (C[0], C[1], C[2]-r_pipe)
        foo.setBegin('begin', C, E, N)
        foo.add('middle1', None, [-r_bow,   -r_bow, '90deg'])
        foo.add('middle2', None, ['90deg', -r_bow, 0])
        foo.add('end', [0., 0., l_out_segment])

    foo()
    foo.scale(1000)
    print(foo)
