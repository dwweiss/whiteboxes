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
      2018-05-30 DWW
"""

from Parameter import C2K, K2C
import GenericMatter as gm


class R4_230NA(gm.NonMetal):
    """
    Properties of R-4-230 Polyphenylene Sulfide Resins

    References:
        [1] Chevron Phillips Chemical Company LP, Ryton R-4-230
        [2] Solvay Specialty Polymers Ryton R-4
                http://www.matweb.com/search/datasheet.aspx?
                matguid=1f9801f2d83d4b4abea8896fa898ff32&ckck=1
        [3] Chevron Phillips Ryton R-4 04 PPS
                http://www.matweb.com/search/datasheet.aspx?
                matguid=29b9c2bee27942209e3e3747639fbefe
    """

    def __init__(self, identifier='Ryton', latex=None, comment=None):
        """
        Args:
            identifier (string, optional):
                identifier of matter

            latex (string, optional):
                Latex-version of identifier. If None, identifier is assigned

            comment (string, optional):
                comment on matter
        """
        super().__init__(identifier, latex=latex, comment=comment)

        self.version = '240817_dww'
        if comment is None:
            self.comment = 'Ryton R-4-230 40% fiberglass reinforced ' + \
                           'polyphenylene sulfide resins'
        self.T.ref = C2K(20)

        self.nu_mech = 0.38        # TODO from Solvay Spec. Polymers Ryton R-4
        self.friction = 0.5
        self.R_compr.calc = lambda T=0, p=0, x=0: 0*K2C(T) + 268e6

        self.E.calc = lambda T=0, p=0, x=0: 14.5e+9
        self.beta.calc = lambda T=0, p=0, x=0: 15e-6
        self.c_p.calc = lambda T=0, p=0, x=0: 1000
        #      TODO difference between c_p of reference [2]: 1003 and [3]: 1000
        self.Lambda.calc = lambda T=0, p=0, x=0: 3.63
        self.rho.calc = lambda T=0, p=0, x=0: 1680
        self.rho_el.calc = lambda T=0, p=0, x=0: 1e+12

        self.T_melt = (C2K(1399), C2K(1454))


class Concrete(gm.NonMetal):
    def __init__(self, identifier='concrete', latex=None, comment=None):
        """
        Args:
            identifier (string, optional):
                identifier of matter

            latex (string, optional):
                Latex-version of identifier. If None, identifier is assigned

            comment (string, optional):
                comment on matter
        """
        super().__init__(identifier, latex=latex, comment=comment)
        self.c_p.calc = lambda T=0, p=0, x=0: 0.8
        self.rho.calc = lambda T=0, p=0, x=0: 2300
        self.Lambda.calc = lambda T=0, p=0, x=0: 1.8


class Ceramic(gm.NonMetal):
    def __init__(self, identifier='ceramic', latex=None, comment=None):
        """
        Args:
            identifier (string, optional):
                identifier of matter

            latex (string, optional):
                Latex-version of identifier. If None, identifier is assigned

            comment (string, optional):
                comment on matter
        """
        super().__init__(identifier, latex=latex, comment=comment)
        self.c_p.calc = lambda T=0, p=0, x=0: 835
        self.rho.calc = lambda T=0, p=0, x=0: 1920
        self.Lambda.calc = lambda T=0, p=0, x=0: 0.72


# Examples ####################################################################

if __name__ == '__main__':
    ALL = 0

    import NonMetals as thisModule
    classes = [v for c, v in thisModule.__dict__.items()
               if isinstance(v, type) and v.__module__ == thisModule.__name__]

    if 1 or ALL:
        for mat in classes:
            print('class:', mat.__name__)
            foo = mat()
            print(foo.identifier, '*' * 50)
            foo.plot()
