Introduction
============
Installation
------------
To install GeoCoon use `pip`::

    pip install geocoon

GeoCoon requires Shapely 1.3.0, Pandas 0.13.0 and Python 3.

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


Data Model
----------
The GeoCoon data model and its context is shown on the diagram below.

The GeoCoon follows Pandas model. GIS data frame inherits from Pandas data
frame and contains multiple series and GIS series columns.

.. code::
   :class: diagram

   +-------------------+       +----------------+
   | pandas::DataFrame |------>| pandas::Series |.-.-.-.
   +-------------------+       +----------------+      |
          /_\                         /_\              .
           |                           |               | <<derive>>
           |                           |               .
   +--------------+              +--------------+      |
   | GeoDataFrame |------------->| <<abstract>> |<-.-.-.
   +--------------+         1..* |  GeoSeries   |
                                +--------------+
                                       |
                                       |
                                       | 0..*
                                      \|/
                       +---------------------------------+
                       | shapely::geometry::BaseGeometry |
                       +---------------------------------+


The GIS series contain a collection of Shapely geometries. Gis series
classes implement vectorized methods, which mimic Shapely geometries API.
The methods return Pandas series objects or even GIS series if Shapely
geometry computes other geometry.

For example, given GIS series of points::

    >>> from geocoon import PointSeries
    >>> from shapely.geometry import Point
    >>> points = PointSeries([Point(1, 1), Point(2, 2)])

the points `x` coordinate access returns series of float numbers::

    >>> points.x
    0    1
    1    2
    dtype: float64

and points buffer calculation returns GIS series of line polygons for each
point::

    >>> points.buffer(0.3, resolution=3)
    0    POLYGON ((1.3 1, 1.259807621135332 0.850000000...
    1    POLYGON ((2.3 2, 2.259807621135332 1.85, 2.15 ...
    dtype: object


Performance Notes
-----------------
It is important to remember that the vectorized methods always compute
values and therefore their calls are expensive. For example, given data
frame with GIS series of points::

    >>> from geocoon import GeoDataFrame
    >>> data = GeoDataFrame({'points': points})

the GIS column series access is cheap::

    >>> data.points
    0    POINT (1 1)
    1    POINT (2 2)
    Name: points, dtype: object

but the following calls are expensive::

    >>> data.points.x
    0    1
    1    2
    dtype: float64

    >>> points.x
    0    1
    1    2
    dtype: float64

This might be optimized in the future.

.. vim: sw=4:et:ai
