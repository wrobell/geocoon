Introduction
============
Installation
------------
To install GeoCoon use `pip`::

    pip install geocoon

GeoCoon requires Shapely 1.3.0, Pandas 0.13.0 and Python 3.

Features
--------
GeoCoon supports

#. Point, line string and polygon geometries (more to come).
#. Vectorized GIS object properties access and method execution.
#. Pandas data selection and split-apply-combine idioms.
#. SQL/MM databases (i.e. PostgreSQL + Postgis).
#. Multiple geometry columns in a data frame.

Quick Start
-----------
To quickly start with GeoCoon data structrues from GeoCoon package and
Shapely geometries::

   >>> from geocoon import GeoDataFrame, PointSeries
   >>> from shapely.geometry import Point

Create GIS series of points::

    >>> points = PointSeries([Point(1, 1), Point(2, 2)])
    >>> points
    0    POINT (1 1)
    1    POINT (2 2)
    dtype: object

Create GIS data frame::

    >>> data = GeoDataFrame({'points': points, 'classifier': ['a', 'b']})
    >>> data
      classifier       points
    0          a  POINT (1 1)
    1          b  POINT (2 2)
    <BLANKLINE>
    [2 rows x 2 columns]

or::

    >>> data = GeoDataFrame({'classifier': ['a', 'b']})
    >>> data['points'] = points
    >>> data
      classifier       points
    0          a  POINT (1 1)
    1          b  POINT (2 2)
    <BLANKLINE>
    [2 rows x 2 columns]

*NOTE:* GeoDataFrame constructor works with GIS series only when data is
provided via dictionary.

Access point `x` coordinate::

    >>> points.x
    0    1
    1    2
    dtype: float64

Select points by classifier::

    >>> data[data.classifier == 'b'].points
    1    POINT (2 2)
    Name: points, dtype: object

.. vim: sw=4:et:ai
