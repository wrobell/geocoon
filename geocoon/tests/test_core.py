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
from shapely.geometry import Point

from geocoon.core import PointSeries, GeoDataFrame, fetch_attr

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
    def test_pt_adaptation_coordinates(self):
        """
        Test adaptation of point coordinates in GIS series
        """
        data = [Point(v, v * 2, v * 3) for v in [1, 2]]
        series = PointSeries(data)
        self.assertTrue([1, 2, 3], series.x)
        self.assertTrue([2, 4, 6], series.y)
        self.assertTrue([3, 6, 9], series.z)


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
 
 
# vim: sw=4:et:ai
