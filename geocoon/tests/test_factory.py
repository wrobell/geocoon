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

import binascii

from shapely.geometry import Point

from geocoon.factory import from_shapes, from_wkb
from geocoon.core import PointSeries

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
        self.assertEquals(PointSeries, type(series))


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
        self.assertEquals(PointSeries, type(series))


# vim: sw=4:et:ai
