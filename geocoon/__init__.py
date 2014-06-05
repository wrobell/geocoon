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
GeoCoon is a library to integrate Shapely GIS geometries with Pandas data
frames.
"""

__version__ = '0.2.0'

from .core import GeoDataFrame, PointSeries, LineStringSeries, \
    PolygonSeries
from .sql import read_sql
from .factory import from_shapes, from_wkb, as_line_string, as_polygon

# vim: sw=4:et:ai
