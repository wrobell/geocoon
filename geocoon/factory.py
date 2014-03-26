#
# GeoCoon - library to integrate Shapely GIS geometries with Pandas data frames
#
# Copyright (C) 2014 by Artur Wroblewski <wrobell@pld-linux.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pandas
import shapely.wkb

import binascii

import geocoon.core
 
def from_shapes(shapes, index=None):
    """
    Create a GIS series from collection of GIS shapes.

    :param shapes: Collection of shapes.
    :param index: Series index.
    """
    shapes = tuple(shapes)
    name = shapes[0].__class__.__name__ + 'Series'
    cls = getattr(geocoon.core, name)
    return cls(shapes, index=index)
    

def from_wkb(wkb, index=None):
    """
    Create a GIS series from collection of WKB binary strings.
    
    :param wkb: Collection of WKB binary strings.
    :param index: Series index.
    """
    to_bin = lambda v: v if isinstance(v, bytes) else binascii.unhexlify(v)
    shapes = (shapely.wkb.loads(to_bin(v)) for v in wkb)
    return from_shapes(shapes, index=index)


# vim: sw=4:et:ai

