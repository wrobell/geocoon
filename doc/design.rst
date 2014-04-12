Library Design
==============
Data Model
----------
The GeoCoon data model and its context is shown on the diagram below.

.. code::
   :class: diagram

   +-------------------+     0..* +----------------+
   | pandas::DataFrame |--------->| pandas::Series |.-.-.-.
   +-------------------+          +----------------+      |
          /_\                            /_\              .
           |                              |               | <<derive>>
           |                              |               .
   +--------------+                 +--------------+      |
   | GeoDataFrame |                 | <<abstract>> |<-.-.-.
   +--------------+                 |  GeoSeries   |
                                    +--------------+
                                           |
                                           |
                                           | 0..*
                                          \|/
                           +---------------------------------+
                           | shapely::geometry::BaseGeometry |
                           +---------------------------------+

The GeoCoon follows Pandas model. GIS data frame inherits from Pandas data
frame and contains multiple series and GIS series columns.

The rationale behind each of the classes is as follows

#. Pandas data frame lacks support for custom Series objects (see
   `issue 6751 <https://github.com/pydata/pandas/issues/6751>`_). The
   custom data frame class - GeoDataFrame - is required to support GIS
   series and Pandas operations like data selection and grouping, so the
   type information of columns being GIS series is not lost.
#. The custom series classes, starting with abstract GeoSeries class, are
   required to support vectorized versions of attribute access and method
   calls mimicking those provided by Shapely GIS geometries.

GIS series object contains a collection of Shapely geometries. GIS series
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
values and therefore their calls are expensive. For example, given GIS data
frame `data` with GIS series of points `data.points`, the `data.points`
attribute access is cheap, but `data.points.x` is expensive.

This might be optimized in the future.

.. vim: sw=4:et:ai
