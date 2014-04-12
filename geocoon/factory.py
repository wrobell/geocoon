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

import binascii
from functools import partial

import pandas
from pandas.core.groupby import SeriesGroupBy
import shapely.wkb
import shapely.geometry

import geocoon.core
 
def from_shapes(shapes, index=None, cls=None):
    """
    Create a GIS series from collection of GIS shapes.

    If GIS series class is not specified, then it is determined from the
    class of first geometry in the collection.

    :param shapes: Collection of shapes.
    :param index: Series index.
    :param cls: GIS series class.
    """
    if not cls:
        shapes = tuple(shapes)
        n = shapes[0].__class__.__name__
        name = n + 'Series'
        if not hasattr(geocoon.core, name):
            raise ValueError('The {} geometry not supported yet'.format(n))
        cls = getattr(geocoon.core, name)
    return cls(shapes, index=index)
    

def from_wkb(wkb, index=None):
    """
    Create a GIS series from collection of WKB binary strings.
    
    :param wkb: Collection of WKB binary strings.
    :param index: Series index.
    """
    shapes = (shapely.wkb.loads(v, isinstance(v, str)) for v in wkb)
    return from_shapes(shapes, index=index)


def as_line_string(series):
    """
    Create line string from GIS series.

    The method works for grouped GIS series - for each grouping key
    a line string is created.

    :param series: GIS series.
    """
    cls = shapely.geometry.LineString
    if isinstance(series, SeriesGroupBy):
        lines = series.apply(partial(_shape_from_coords, shape_cls=cls))
        return geocoon.core.LineStringSeries(lines)
    else:
        return _shape_from_coords(series, cls)


def as_polygon(series):
    """
    Create polygon from GIS series.

    The method works for grouped GIS series - for each grouping key
    a polygon is created.

    :param series: GIS series.
    """
    cls = shapely.geometry.Polygon
    if isinstance(series, SeriesGroupBy):
        lines = series.apply(partial(_shape_from_coords, shape_cls=cls))
        return geocoon.core.PolygonSeries(lines)
    else:
        return _shape_from_coords(series, cls)


def _shape_from_coords(data, shape_cls):
    """
    Create shape from a coordinates taken from collection of geometries.

    :param data: Collection of geometries.
    :param shape_cls: Class of geometry to be created.
    """
    return shape_cls(c for g in data for c in g.coords)


# vim: sw=4:et:ai
