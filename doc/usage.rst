Using GeoCoon Library
=====================

Creating Data Frame and Series Objects
--------------------------------------
To process data with GeoCoon library, it is required to create

* GIS series of point, line string or other GIS objects supported by
  Shapely library
* GIS data frame :py:func:`geocoon.GeoDataFrame`

for example::

    >>> from shapely.geometry import Point
    >>> import geocoon
    >>> series = geocoon.PointSeries([Point(1, 1), Point(2, 2), Point(3, 3)])
    >>> series
    0    POINT (1 1)
    1    POINT (2 2)
    2    POINT (3 3)
    dtype: object

    >>> data = geocoon.GeoDataFrame({'location': series})
    >>> data
          location
    0  POINT (1 1)
    1  POINT (2 2)
    2  POINT (3 3)
    <BLANKLINE>
    [3 rows x 1 columns]

The mapping of GIS series and Shapely classes is presented in the table
below

    =============== ===================
     Shapely Class    GIS Series Class
    =============== ===================
     Point           PointSeries
     LineString      LineStringSeries
     Polygon         PolygonSeries
    =============== ===================

*NOTE:*

    #. The need for custom GIS series classes is to support different methods
       implemented by different GIS classes.
    #. The need for GIS data frame is lack of support for custom Series objects
       in Pandas library, see `issue 6751 <https://github.com/pydata/pandas/issues/6751>`_.

Creating a GIS data frame and adding a GIS series to the data frame is supported as well::

    >>> data = geocoon.GeoDataFrame({'time': range(4, 7)})
    >>> data['location'] = series
    >>> data
       time     location
    0     4  POINT (1 1)
    1     5  POINT (2 2)
    2     6  POINT (3 3)
    <BLANKLINE>
    [3 rows x 2 columns]


Vectorized Data Access
----------------------

Split, Apply, Combine
---------------------

.. vim: sw=4:et:ai
