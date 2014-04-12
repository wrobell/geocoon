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

from shapely.geometry import Point, LineString, Polygon

from geocoon.factory import from_shapes, from_wkb, as_line_string, \
    as_polygon
from geocoon.core import GeoDataFrame, PointSeries, LineStringSeries, \
    PolygonSeries

import unittest

class FactoryTestCase(unittest.TestCase):
    """
    GIS series factory tests.
    """
    def test_from_shapes(self):
        """
        Test GIS series shapes factory (point)
        """
        points = Point(0, 0), Point(1, 0), Point(2, 0)

        series = from_shapes(points)
        self.assertEqual(PointSeries, type(series))


    def test_from_shapes_cls(self):
        """
        Test GIS series shapes factory (enforced class)
        """
        points = Point(0, 0), Point(1, 0), Point(2, 0)

        series = from_shapes(points, cls=PointSeries)
        self.assertEqual(PointSeries, type(series))


    def test_from_shapes_unsupported(self):
        """
        Test GIS series shapes factory (unsupported)

        Test with any non Shapely class.
        """
        class XY(object): pass

        data = XY(), XY(), XY()
        self.assertRaises(ValueError, from_shapes, data)


    def test_from_wkb(self):
        """
        Test GIS series WKB factory (point)
        """
        uhl = binascii.unhexlify
        points = [
            uhl(b'010100000000000000000000000000000000000000'),
            uhl(b'0101000000000000000000f03f0000000000000000'),
                 '010100000000000000000000400000000000000000', # support strings as well
        ]

        series = from_wkb(points)
        self.assertEqual(PointSeries, type(series))



class LineStringFactoryTestCase(unittest.TestCase):
    """
    GIS line string series factory tests.
    """

    def test_line_string_pt(self):
        """
        Test creating line string from series (points 2d)
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
        data = GeoDataFrame(data)
        series = as_line_string(data.location)

        self.assertTrue(isinstance(series, LineString))


    def test_grouped_series_pt(self):
        """
        Test creating line string series from grouped series (points 2d)
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
        series = as_line_string(data.location)

        self.assertTrue(isinstance(series, LineStringSeries))
        self.assertEqual(2, len(series))
        self.assertEqual(2, series[0].length) # dev1
        self.assertEqual(4, series[1].length) # dev2


    def test_grouped_series_pt_3d(self):
        """
        Test creating line string series from grouped series (points 3d)
        """
        data = {
            'device': ['dev1', 'dev1', 'dev2', 'dev2', 'dev2'],
            'location': PointSeries([
                Point(1, 11, 111), # dev1
                Point(1, 13, 113),
                Point(2, 21, 221), # dev2
                Point(2, 23, 223),
                Point(2, 25, 225),
            ])
        }
        data = GeoDataFrame(data).groupby('device')
        series = as_line_string(data.location)

        self.assertTrue(isinstance(series, LineStringSeries))
        self.assertEqual(2, len(series))
        self.assertTrue(series[0].has_z)



class PolygonFactoryTestCase(unittest.TestCase):
    """
    GIS polygon series factory tests.
    """

    def test_polygon_pt(self):
        """
        Test creating polygon from series (points 2d)
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
        data = GeoDataFrame(data)
        series = as_polygon(data.location)

        self.assertTrue(isinstance(series, Polygon))


    def test_grouped_series_pt(self):
        """
        Test creating polygon series from grouped series (points 2d)
        """
        data = {
            'device': ['dev1'] * 4 + ['dev2'] * 3,
            'location': PointSeries([
                Point(1, 11), # dev1
                Point(2, 12),
                Point(1, 13),
                Point(2, 14),
                Point(2, 21), # dev2
                Point(1, 23),
                Point(2, 25),
            ])
        }
        data = GeoDataFrame(data).groupby('device')
        series = as_polygon(data.location)

        self.assertTrue(isinstance(series, PolygonSeries))
        self.assertEqual(2, len(series))
        self.assertAlmostEqual(7.4049, series[0].length, 4) # dev1
        self.assertAlmostEqual(8.472, series[1].length, 3) # dev2


    def test_grouped_series_pt_3d(self):
        """
        Test creating polygon string series from grouped series (points 3d)
        """
        data = {
            'device': ['dev1'] * 4 + ['dev2'] * 3,
            'location': PointSeries([
                Point(1, 11, 111), # dev1
                Point(2, 12, 112),
                Point(1, 13, 113),
                Point(2, 14, 114),
                Point(2, 21, 211), # dev2
                Point(1, 23, 212),
                Point(2, 25, 213),
            ])
        }
        data = GeoDataFrame(data).groupby('device')
        series = as_polygon(data.location)

        self.assertTrue(isinstance(series, PolygonSeries))
        self.assertEqual(2, len(series))
        self.assertTrue(series[0].has_z)


# vim: sw=4:et:ai
