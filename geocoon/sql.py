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

import pandas.io.sql

from .core import GeoDataFrame
from .factory import from_wkb

def read_sql(sql, con, geom_col, index_col=None, coerce_float=True,
        params=None):
    """
    Query SQL/MM database and return GIS data frame with specified column
    as GIS series.

    :param geom_col: GIS column (can be collection of column names).

    .. seealso:: pandas.io.sql.read_sql
    """
    if isinstance(geom_col, str):
        geom_col = (geom_col,)

    data = pandas.io.sql.read_sql(
        sql, con, index_col=index_col, coerce_float=coerce_float,
        params=params
    )
    data = GeoDataFrame(data)

    # coerce each column to GIS series
    for col in geom_col:
        data[col] = from_wkb(data[col], index=data.index)

    return data


# vim: sw=4:et:ai
