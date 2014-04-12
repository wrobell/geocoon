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

from shapely.geometry import Point

from geocoon.sql import read_sql
from geocoon.core import GeoDataFrame, PointSeries

import unittest
from unittest import mock

class SQLTestCase(unittest.TestCase):
    """
    Test SQL GeoCoon SQL routines.
    """
    @mock.patch('pandas.io.sql.read_sql')
    def test_read_sql(self, f_sql):
        """
        Test SQL data frame read
        """
        points = Point(1, 1), Point(2, 2), Point(3, 3)
        data = {
            'a': PointSeries([p.wkb for p in points]),
            'b': list(range(3)),
        }
        data = GeoDataFrame(data)
        data = data[['a', 'b']]
        f_sql.return_value = data

        result = read_sql('query', 'con', geom_col='a')

        self.assertEqual(PointSeries, type(result.a))
        self.assertEqual(Point, type(result.a[0]))

        self.assertEqual(3, len(result.index))
        self.assertTrue(all([1, 2, 3] == result.a.x))
        self.assertTrue(all([1, 2, 3] == result.a.y))


# vim: sw=4:et:ai
