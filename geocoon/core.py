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
from functools import partial
from shapely.geometry import Point, LineString, Polygon

from .meta import META_POINT, META_LINE_STRING, META_POLYGON
 
#
# GIS data frame and series definitions
#

class GeoSeries(pandas.Series):
    """
    Base implementation of GIS series based on Pandas' series.
    """
    def __getitem__(self, key):
        value = super().__getitem__(key)
        if isinstance(value, pandas.Series):
            return self._constructor(value)
        else:
            return value


    def __getslice__(self, slice):
        print(slice)
        value = super().__getslice__(slice)
        return self._constructor(value)


    @property
    def _constructor(self):
        return self.__class__



class PointSeries(GeoSeries):
    """
    GIS point series.
    """



class LineStringSeries(GeoSeries):
    """
    GIS line string series.
    """



class PolygonSeries(GeoSeries):
    """
    GIS polygon series.
    """



class GeoDataFrame(pandas.DataFrame):
    """
    GIS data frame based on Pandas' data frame.

    The `data` parameter has to be a dictionary at the moment.
    """
    def __init__(self, data, *args, **kw):
        """
        Create GIS data frame.

        Overrides Pandas' data frame constructor to determine, which
        columns are GIS series.

        .. seealso:: `pandas.DataFrame`

        """
        super().__init__(data, *args, **kw)

        self._geom_columns = {}

        if isinstance(data, dict):
            for k, col in data.items():
                if isinstance(col, GeoSeries):
                    self._geom_columns[k] = type(col)


    def __setitem__(self, key, value):
        """
        Overrides Pandas' data frame `__setitem__` method to store
        information about geometry series.
        """
        super().__setitem__(key, value)
        if isinstance(value, GeoSeries):
            self._geom_columns[key] = type(value)
 

    @property
    def _constructor(self):
        """
        Return such GIS data frame constructor, so geometry columns
        information are preserved.
        """
        def f(*args, **kw):
            obj = self.__class__(*args, **kw)
            # copy the geometry columns information
            obj._geom_columns = self._geom_columns.copy()
            # do we need the below?
            #for col in obj.columns:
            #    if col not in obj.columns:
            #        del obj._geom_columns[col]
            return obj
        return f



#
# GIS data frames and series adaptation functions
#

def wrap_df_method(method):
    """
    Wrap GeoDataFrame method to support GIS data frames and series.
    """
    def f(self, key):
        v = method(self, key)
        if isinstance(v, pandas.DataFrame):
            df = GeoDataFrame(v, index=v.index)
            df._geom_columns = self._geom_columns.copy()
            return df
        elif isinstance(key, str) and key in self._geom_columns:
            cls = self._geom_columns[key]
            return cls(v, index=self.index)
        else:
            return v
    return f

 

def fetch_attr(series, name):
    """
    Create series using attribute value of each object stored in the
    GIS series.

    The function is used to adapt GIS series.

    :param series: GIS series.
    :param name: Attribute name.
    """
    data = [getattr(obj, name) for obj in series]
    return pandas.Series(data, index=series.index)
 
 
def adapt_attr(cls, gis, name):
    """
    Adapt GIS series to return series using attribute value of each object
    stored in the series.

    :param cls: GIS series class.
    :param gis: Shapely geometry class.
    :param name: Attribute name.
    """
    f = partial(fetch_attr, name=name)
    f.__doc__ = 'Vectorized version of :py:attr:`{}.{}` property.'.format(
        gis.__qualname__, name
    )
    setattr(cls, name, property(f))

 
def create_series_method(cls, gis, method, meta):
    """
    Create GIS series method to return series of values returned by method
    call on each object in the series.

    :param cls: GIS series class.
    :param gis: Shapely geometry class.
    :param method: Method name to be adapted.
    :param meta: Method metadata.

    :seealso:: :py:class:`geocoon.meta.Meta`
    """
    first_is_geom = meta.first_is_geom
    returns_geom = meta.returns_geom

    # determine series class returned by method
    # - pandas.Series if returned value is non-geom object
    # - return the same series if returns_geom is true
    # - otherwise returns_geom is class - the series class
    if returns_geom == True:
        series_cls = cls
    elif returns_geom == False:
        series_cls = pandas.Series
    else:
        series_cls = MAP_GEOM[meta.returns_geom]

    # Shapely geometry method call to be adapted
    mcall = getattr(gis, method)

    def f_geom(self, other, *args, **kw):
        data = (mcall(s, o, *args, **kw) for s, o in zip(self, other))
        return series_cls(data, index=self.index)

    def f_non_geom(self, *args, **kw):
        data = (mcall(s, *args, **kw) for s in self)
        return series_cls(data, index=self.index)

    doc = 'Vectorized version of :py:meth:`{}.{}` method.'.format(
        cls.__qualname__, method
    )
    if first_is_geom:
        f = f_geom
        f.__doc__ = doc + '\n\n' \
            + 'The `other` parameter of the method is GIS series object.'
    else:
        f = f_non_geom
        f.__doc__ = doc
    return f
 
 
def adapt_series(cls, gis, gis_meta):
    """
    Adapt GIS series to return data stored in GIS object.

    :param cls: GIS series class.
    :param gis: GIS object class.
    :param gis_meta: GIS object class metadata.
    """
    for name, meta in gis_meta.items():
        attr = getattr(gis, name)
        if meta.is_property:
            adapt_attr(cls, gis, name)
        else:
            wrapper = create_series_method(cls, gis, name, meta)
            setattr(cls, name, wrapper)


#
# perform GIS data frames and series adaptation
#
 
# adapt GIS data frame methods to return GIS data frames and methods
df_methods = ('__getitem__', 'sort')
for m in df_methods:
    mt = getattr(GeoDataFrame, m)
    setattr(GeoDataFrame, m, wrap_df_method(mt))

# adapt GIS series

# geometry to gis series mapping
MAP_GEOM = {
    Point: PointSeries,
    LineString: LineStringSeries,
    Polygon: PolygonSeries,
}

adapt_series(PointSeries, Point, META_POINT)
adapt_series(LineStringSeries, LineString, META_LINE_STRING)
adapt_series(PolygonSeries, Polygon, META_POLYGON)
 

# vim: sw=4:et:ai
