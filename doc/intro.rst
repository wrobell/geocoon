Introduction
============
Installation
------------
To install GeoCoon use `pip`::

    pip install --user geocoon

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
Start processing GIS data with GeoCoon import data frame, relevant series
and Shapely geometry classes.

For example, to process point data::

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

*NOTE:*

    *GeoDataFrame constructor works with GIS series when data is provided
    via dictionary like above.*

Or add new column to existing GIS data frame::

    >>> data = GeoDataFrame({'classifier': ['a', 'b']})
    >>> data['points'] = points
    >>> data
      classifier       points
    0          a  POINT (1 1)
    1          b  POINT (2 2)
    <BLANKLINE>
    [2 rows x 2 columns]

Access `x` coordinate of each point::

    >>> points.x
    0    1
    1    2
    dtype: float64

Select points by classifier::

    >>> data[data.classifier == 'b'].points
    1    POINT (2 2)
    Name: points, dtype: object

.. vim: sw=4:et:ai
