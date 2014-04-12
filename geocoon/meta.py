#
# GeoCoon - GIS data analysis library based on Pandas and Shapely
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
- comment other method renames appropriately, i.e. standard uses `is_3D'
  but Shapely implements `has_z`

"""

from collections import namedtuple

from shapely.geometry import Polygon

Meta = namedtuple('Meta', 'first_is_geom returns_geom is_property')
Meta.__doc__ = """
Metadata of attribute or method of GIS geometry class.

The `returns_geom` can have the following values

    false
        Method returns a scalar.
    true
        Method returns geometry object of the same class as the owner of
        the method.
    class
        Method returns geometry object of the specified class.

:param first_is_geom: First parameter of method is geometry.
:param returns_geom: Description of object returned by method.
:param is_property: True if Shapely presents method as property.
"""


def meta(first_is_geom=False, returns_geom=False, is_property=False):
    """
    Create metadata for method of GIS geometry class.

    .. seealso: :py:class:`Meta`
    """
    return Meta(first_is_geom, returns_geom, is_property)


META_GEOMETRY = {
    # 'dimension': meta(is_property=True),
    # 'coordinate_dimension': meta(is_property=True),
    # 'spatial_dimension': meta(is_property=True),
    'geom_type': meta(is_property=True), # geometry_type
    # 'srid': meta(is_property=True),
    # 'envelope': meta(returns_geom=True, is_property=True),
    'wkt': meta(is_property=True), # as_text
    'wkb': meta(is_property=True), # as_binary
    'is_empty' : meta(is_property=True),
    'is_simple': meta(is_property=True),
    'has_z': meta(is_property=True), # is_3D
    # 'is_measured': meta(is_property=True),
    'boundary': meta(returns_geom=True, is_property=True),

    ## query,
    'equals': meta(first_is_geom=True),
    'disjoint': meta(first_is_geom=True),
    'intersects': meta(first_is_geom=True),
    'touches': meta(first_is_geom=True),
    'crosses': meta(first_is_geom=True),
    'within': meta(first_is_geom=True),
    'contains': meta(first_is_geom=True),
    'overlaps': meta(first_is_geom=True),
    'relate': meta(first_is_geom=True),
    # 'locate_along': meta(returns_geom=True),
    # 'locate_between': meta(returns_geom=True),

    ## analysis,
    'distance': meta(first_is_geom=True),
    'buffer': meta(returns_geom=Polygon), # in the OGC standard - geometry
    'convex_hull': meta(returns_geom=True),
    'intersection': meta(first_is_geom=True, returns_geom=True),
    'union': meta(first_is_geom=True, returns_geom=True),
    'difference': meta(first_is_geom=True, returns_geom=True),
    # sym_difference
    'symmetric_difference': meta(first_is_geom=True, returns_geom=True),
}


META_POINT = META_GEOMETRY.copy()
META_POINT.update({
    'x': meta(is_property=True),
    'y': meta(is_property=True),
    'z': meta(is_property=True),
    # 'm': meta(is_property=True),
})


META_CURVE = META_GEOMETRY.copy()
META_CURVE.update({
    'length': meta(is_property=True),
    # 'start_point': meta(returns_geom=True, is_property=True),
    # 'end_point': meta(returns_geom=True, is_property=True),
    # 'is_closed': meta(is_property=True),
    'is_ring': meta(is_property=True),
})


META_LINE_STRING = META_CURVE.copy()
META_LINE_STRING.update({
    # 'num_points': meta(is_property=True),
    # 'point_n': meta(returns_geom=True),
})


META_SURFACE = META_GEOMETRY.copy()
META_SURFACE.update({
    'area': meta(is_property=True),
    'centroid': meta(is_property=True, returns_geom=True), # TODO: returns point
    'point_on_surface': meta(is_property=True, returns_geom=True), # TODO: returns point
    # 'boundary': override with MultiCurve
})


META_SURFACE = META_GEOMETRY.copy()
META_SURFACE.update({
    'area': meta(is_property=True),
    'centroid': meta(is_property=True, returns_geom=True), # TODO: returns point
    # 'point_on_surface': meta(is_property=True, returns_geom=True), # TODO: returns point
    # 'boundary': TODO: override with MultiCurve
})


META_POLYGON = META_SURFACE.copy()
META_POLYGON.update({
    'exterior': meta(is_property=True, returns_geom=True), # exterior_ring, TODO: returns LineString
    # 'num_interior_ring': meta(is_property=True),
    # 'interiors': meta(is_property=True, returns_geom=True), # # is that interior_ring?, TODO: returns LineString
})

# vim: sw=4:et:ai
