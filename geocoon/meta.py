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

"""
The metadata for GIS geometries.

The metadata is based on `Simple Feature Access OGC standard <http://www.opengeospatial.org/standards/sfa>`_
and Shapely documentation.

To update the metadata information of the classes

- check the diagrams in "Geometry object model" (section 6.1) of the OGC
  specification
- describe GIS classes using `meta` function
- comment out, don't remove methods not supported by Shapely
- convert camel case names to use underscores
- comment other method renames appropriately

"""

from collections import namedtuple

Meta = namedtuple('Meta', 'first_is_geom returns_geom is_property')
Meta.__doc__ = """
Metadata of method of GIS geometry class.

:param first_is_geom: First parameter of method is geometry.
:param returns_geom: True if method returns a geometry.
:param is_property: True if Shapely presents method as property.
"""

def meta(first_is_geom=False, returns_geom=False, is_property=False):
    """
    Create metadata for method of GIS geometry class.

    .. seealso: :py:class:`Meta`
    """
    return Meta(first_is_geom, returns_geom, is_property)


META_POINT = {
    'x': meta(is_property=True),
    'y': meta(is_property=True),
    'z': meta(is_property=True),
    # 'm': meta(is_property=True),
}

# vim: sw=4:et:ai
