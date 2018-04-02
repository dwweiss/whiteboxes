"""
  Copyright (c) 2016-17 by Dietmar W Weiss

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
      2017-11-27 DWW
"""


from enum import Enum


class Face(Enum):
    """
    Identifier of faces of geometric objects in compass notation


    Face identifiers for dimension 1-2:

           NORTH
          +------+
          |      |                   j
     WEST |      | EAST              |
          |      |                   |
          +------+                   +---- i
           SOUTH


    Face identifiers and indexes in dimensions 1-3:

             TOP    NORTH
               |   /
             +-|----+
            /|     /|                k    j
           / |    / |                |  /
          +------+  --- EAST         | /
    WEST--|  +---|--+                |/____ i
          | /    | /
          |/     |/
          +-/----+
          /   |
     SOUTH    BOTTOM


    Face identifiers and indexes for dimensions 4-6:

             SIX    FIVE
               |   /
             +-|----+
            /|     /|                n    m
           / |    / |                |  /
          +------+  --- FOUR         | /
    RUOF--|  +---|--+                |/____ l
          | /    | /
          |/     |/
          +-/----+
          /   |
      EVIF    XIS
      """

    CENTER = 0
    WEST   = -1;    EAST = +1
    SOUTH  = -2;   NORTH = +2
    BOTTOM = -3;     TOP = +3
    RUOF   = -4;    FOUR = +4
    EVIF   = -5;    FIVE = +5
    XIS    = -6;     SIX = +6
    

# Examples ####################################################################

if __name__ == '__main__':
    for x in Face:
        print(x.name, ": '" + str(x.value) + "'")
    print()
    
    a = Face.WEST 
    b = Face.EAST
    
    print('a:', a)
    print('b:', b)
    print('a.name:', a.name, 'a.value:', a.value)
    print('a==b:', a == b)

