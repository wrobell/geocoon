#!/usr/bin/env python3
#
# GeoCoon - GIS data analysis library based on Pandas and Shapely
#
# Copyright (C) 2013 by Artur Wroblewski <wrobell@pld-linux.org>
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

import sys
import os.path

from setuptools import setup, find_packages

setup(
    name='geocoon',
    version='0.2.0',
    description='GIS data analysis library based on Pandas and Shapely',
    long_description="""\
GeoCoon is GIS data analysis Python library, which integrates Pandas data
frames with Shapely GIS geometries.
""",
    author='Artur Wroblewski',
    author_email='wrobell@pld-linux.org',
    url='http://wrobell.it-zone.org/geocoon/',
    setup_requires = ['setuptools_git >= 1.0'],
    packages=find_packages('.'),
    classifiers=[
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
    ],
    keywords='gis',
    license='GPL',
    install_requires = ['shapely >= 1.3', 'pandas >= 0.14.0'],
    test_suite='nose.collector',
)

# vim: sw=4:et:ai
