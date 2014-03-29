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
GeoCoon core unit tests.
"""

import pandas
from shapely.geometry import Point, LineString, Polygon

from geocoon.core import GeoDataFrame, PointSeries, LineStringSeries, \
    PolygonSeries, fetch_attr
from geocoon.meta import META_POINT, META_LINE_STRING, META_POLYGON

import unittest


class GeoDataFrameTestCase(unittest.TestCase):
    """
    Basic GIS data frame tests.
    """
    def test_dict_constructor(self):
        """
        Test GIS data frame constructor with dictionary
        """
        data = [Point(v, v * 2) for v in [1, 2]]
        series = PointSeries(data)

        df = GeoDataFrame({'a': series})
        self.assertEquals(PointSeries, type(df.a))


    def test_assign_new_col(self):
        """
        Test assigning GIS series as column to GIS data frame
        """
        data = [Point(v, v * 2) for v in [1, 2]]
        series = PointSeries(data)

        df = GeoDataFrame({})
        df['a'] = series
        self.assertEquals(PointSeries, type(df.a))


    def test_grouping(self):
        """
        Test GIS data frame grouping
        """
        data = [Point(v, v * 2) for v in range(5)]
        series = PointSeries(data)

        data = {
            'a': series,
            'b': [4, 5, 5, 4, 5],
        }
        df = GeoDataFrame(data)

        gdf = df.groupby('b')

        df = gdf.get_group(4)
        self.assertEquals(PointSeries, type(df.a))
        self.assertTrue(all([0, 3] == df.a.x))
        self.assertTrue(all([0, 6] == df.a.y))

        df = gdf.get_group(5)
        self.assertEquals(PointSeries, type(df.a))
        self.assertTrue(all([1, 2, 4] == df.a.x))
        self.assertTrue(all([2, 4, 8] == df.a.y))


    def test_select(self):
        """
        Test selecting from GIS data frame
        """
        data = [Point(v, v * 2) for v in range(5)]
        series = PointSeries(data)

        data = {
            'a': series,
            'b': [4, 5, 5, 4, 5],
        }
        df = GeoDataFrame(data)
        df = df[df.b == 4]
        self.assertEquals(PointSeries, type(df.a))
        self.assertTrue(all([4] * 2 == df.b))



class GeoSeriesTestCase(unittest.TestCase):
    """
    Basic GIS series tests.
    """
    def test_create(self):
        """
        Test GIS series creation
        """
        data = [Point(v, v * 2) for v in [1, 2]]
        series = PointSeries(data)
        self.assertEquals(PointSeries, type(series))


    def test_fetch_attr(self):
        """
        Test fetch GIS properties from GIS series
        """
        data = [Point(v, v * 2) for v in [1, 2]]
        series = PointSeries(data)
        y = fetch_attr(series, name='y')
        self.assertTrue(all(y == [2, 4]))


    def test_select(self):
        """
        Test selecting from GIS series
        """
        data = [Point(v, v * 2) for v in [1, 2, 3, 4, 5, 6]]
        series = PointSeries(data)

        sub = series[(series.x < 4) & (series.y > 2)]

        self.assertEquals(PointSeries, type(sub))
        self.assertTrue(all([2, 3] == sub.x))
        self.assertTrue(all([4, 6] == sub.y))


    def test_select_single(self):
        """
        Test selecting single GIS object
        """
        data = [Point(v, v * 2) for v in [1, 2, 3, 4, 5, 6]]
        series = PointSeries(data)

        p = series[1]
        self.assertEquals(Point, type(p))


    def test_slice(self):
        """
        Test slicing GIS series
        """
        data = [Point(v, v * 2) for v in [1, 2, 3, 4, 5, 6]]
        series = PointSeries(data)

        sub = series[:3]

        self.assertEquals(PointSeries, type(sub))
        self.assertTrue(all([1, 2, 3] == sub.x))
        self.assertTrue(all([2, 4, 6] == sub.y))


class PointSeriesTestCase(unittest.TestCase):
    """
    Point GIS series unit tests.
    """
    def test_property_adapt(self):
        """
        Test adaptation of point properties
        """
        data = [Point(v, v * 2, v * 3) for v in [5, 2, 4]]
        series = PointSeries(data)
        attrs = (k for k, v in META_POINT.items() if v.is_property)
        for attr in attrs:
            value = getattr(series, attr) # no error? good
            self.assertEquals(3, len(value))


    def test_method_adapt_buffer(self):
        """
        Test adaptation of point buffer method
        """
        data = [Point(v, v * 2, v * 3) for v in [5, 2, 4]]
        series = PointSeries(data)
        value = series.buffer(0.2, resolution=3) # no error? good
        self.assertEquals(3, len(value))


    def test_method_adapt_geom(self):
        """
        Test adaptation of point methods (first param is geometry)
        """
        p1 = [Point(v, v * 2, v * 3) for v in [5, 2, 4]]
        p2 = [Point(v, v * 2, v * 3) for v in [5, 2]] + [Point(4.1, 1, 1)]
        s1 = PointSeries(p1)
        s2 = PointSeries(p2)
        methods = (k for k, v in META_POINT.items() if v.first_is_geom)
        for method in methods:
            mcall = getattr(s1, method) # no error? good
            value = mcall(s2)
            self.assertEquals(3, len(value))
            self.assertTrue(all(not callable(v) for v in value))

        # just in case
        value = s1.equals(s2)
        self.assertTrue(all([True, True, False] == value), value)



class LineStringSeriesTestCase(unittest.TestCase):
    """
    Line string GIS series unit tests.
    """
    def test_property_adapt(self):
        """
        Test adaptation of line string properties
        """
        d1 = tuple((v, v * 1, v * 4) for v in (5, 2, 4))
        d2 = tuple((v, v * 2, v * 5) for v in [5, 2, 4])
        d3 = tuple((v, v * 3, v * 6) for v in [5, 2, 4])

        l1 = LineString(d1)
        l2 = LineString(d2)
        l3 = LineString(d3)

        series = LineStringSeries([l1, l2, l3])

        attrs = (k for k, v in META_LINE_STRING.items() if v.is_property)
        for attr in attrs:
            value = getattr(series, attr) # no error? good
            self.assertEquals(3, len(value))
            self.assertTrue(all(not callable(v) for v in value))


    def test_method_adapt(self):
        """
        Test adaptation of line string methods
        """
        d1 = tuple((v, v * 1, v * 4) for v in (5, 2, 4))
        d2 = tuple((v, v * 2, v * 5) for v in [5, 2, 4])
        d3 = tuple((v, v * 3, v * 6) for v in [5, 2, 4])
        d4 = tuple((v, v * 4, v * 7) for v in [5, 2, 4])

        l1 = LineString(d1)
        l2 = LineString(d2)
        l3 = LineString(d3)
        l4 = LineString(d4)

        s1 = LineStringSeries([l1, l2, l3])
        s2 = LineStringSeries([l2, l3, l4])

        methods = (k for k, v in META_LINE_STRING.items() if v.first_is_geom)
        for method in methods:
            mcall = getattr(s1, method) # no error? good
            value = mcall(s2)
            self.assertEquals(3, len(value))
            self.assertTrue(all(not callable(v) for v in value))


    def test_group_points(self):
        """
        Test creating line string series from grouped points
        """
        data = {
            'device': ['dev1', 'dev1', 'dev2', 'dev2', 'dev2'],
            'location': PointSeries([
                Point(1, 11), # dev1
                Point(1, 13),
                Point(2, 21), # dev2
                Point(2, 23),
                Point(2, 25),
            ])
        }
        data = GeoDataFrame(data).groupby('device')
        series = LineStringSeries.group_points(data.location)

        self.assertTrue(isinstance(series, LineStringSeries))
        self.assertEquals(2, len(series))
        self.assertEquals(2, series[0].length) # dev1
        self.assertEquals(4, series[1].length) # dev2



class PolygonSeriesTestCase(unittest.TestCase):
    """
    Polygon GIS series unit tests.
    """
    def test_property_adapt(self):
        """
        Test adaptation of polygon properties
        """
        poly = lambda v: Polygon(((v, v), (v + 0.1, v), (v + 0.2, v + 0.2), (v, v)))
        data = [poly(v) for v in [5, 2, 4]]
        series = PolygonSeries(data)
        attrs = (k for k, v in META_POLYGON.items() if v.is_property)
        for attr in attrs:
            value = getattr(series, attr) # no error? good
            self.assertEquals(3, len(value))


    def test_method_adapt_buffer(self):
        """
        Test adaptation of polygon buffer method
        """
        poly = lambda v: Polygon(((v, v), (v + 0.1, v), (v + 0.2, v + 0.2), (v, v)))
        data = [poly(v) for v in [5, 2, 4]]
        series = PolygonSeries(data)
        value = series.buffer(0.2, resolution=3) # no error? good
        self.assertEquals(3, len(value))


    def test_method_adapt_geom(self):
        """
        Test adaptation of polygon methods (first param is geometry)
        """
        poly = lambda v: Polygon(((v, v), (v + 0.1, v), (v + 0.2, v + 0.2), (v, v)))
        p1 = [poly(v) for v in [5, 2, 4]]
        p2 = [poly(v) for v in [6, 2, 3]]
        s1 = PolygonSeries(p1)
        s2 = PolygonSeries(p2)
        methods = (k for k, v in META_POLYGON.items() if v.first_is_geom)
        for method in methods:
            mcall = getattr(s1, method) # no error? good
            value = mcall(s2)
            self.assertEquals(3, len(value))
            self.assertTrue(all(not callable(v) for v in value))

        # just in case
        value = s1.equals(s2)
        self.assertTrue(all([False, True, False] == value), value)


# vim: sw=4:et:ai
