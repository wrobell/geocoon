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


SQL/MM Database Access
~~~~~~~~~~~~~~~~~~~~~~
GeoCoon supports SQL/MM databases, i.e. PostgreSQL with PostGIS extension.
To load GIS data frame from SQL database, use :py:func:`geocoon.read_sql`
function.

For example, to load time series of GPS location data::

    >>> db = psycopg.connect(...) # doctest: +SKIP
    >>> sql = 'select timestamp, location, speed, heading, error from position' # doctest: +SKIP
    >>> data = geocoon.read_sql(sql, db, 'location', index_col='timestamp') # doctest: +SKIP

Other Sources of Data
~~~~~~~~~~~~~~~~~~~~~
Data from any other source can be converted to GIS series using
:py:func:`geocoon.from_wkb` function assuming the data is provided or can
be easily converted into WKB format.

Vectorized Data Access
----------------------
The need for custom GIS data frames and GIS series pays off with vectorized
access to GIS data and vectorized GIS methods.

To access point `x` coordinate::

    >>> data.location.x
    0    1
    1    2
    2    3
    dtype: float64

To calculate buffer of each point::

    >>> pt_buffer = data.location.buffer(0.3)
    >>> pt_buffer
    0    POLYGON ((1.3 1, 1.298555418001659 0.970594857...
    1    POLYGON ((2.3 2, 2.298555418001659 1.970594857...
    2    POLYGON ((3.3 3, 3.298555418001659 2.970594857...
    dtype: object

Vectorized methods return GIS series. For example, it is possible to
calculate area of each buffer of each point::

    >>> pt_buffer.area
    0    0.282289
    1    0.282289
    2    0.282289
    dtype: float64

The method vectorization works when first parameter of a GIS method is
another GIS object. For example, to calculate distance between two points::

    >>> points = geocoon.PointSeries([Point(1.1, 1.0), Point(2.2, 2.), Point(3.3, 3.0)])
    >>> data.location.distance(points)
    0    0.1
    1    0.2
    2    0.3
    dtype: float64


Selecting Data
--------------
GeoCoon library supports basic Pandas operations for data selection.

Given the data frame::

    >>> from shapely.geometry import Point
    >>> import geocoon
    >>> series = geocoon.PointSeries([Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)])
    >>> data = geocoon.GeoDataFrame({
    ...     'location': series,
    ...     'cat': ['a', 'b', 'b', 'a'],
    ...     'time': [1, 2, 3, 4],
    ... })
    >>> data
      cat     location  time
    0   a  POINT (1 1)     1
    1   b  POINT (2 2)     2
    2   b  POINT (3 3)     3
    3   a  POINT (4 4)     4
    <BLANKLINE>
    [4 rows x 3 columns]

Select the data for category `a`::

    >>> data[data.cat == 'a']
      cat     location  time
    0   a  POINT (1 1)     1
    3   a  POINT (4 4)     4
    <BLANKLINE>
    [2 rows x 3 columns]

Select data for points, which `x` coordinate is greater than `1.5`::

    >>> data[data.location.x > 1.5]
      cat     location  time
    1   b  POINT (2 2)     2
    2   b  POINT (3 3)     3
    3   a  POINT (4 4)     4
    <BLANKLINE>
    [3 rows x 3 columns]


Split-Apply-Combine
-------------------
GeoCoon GIS data frame and GIS series support
`Pandas split-apply-combine idioms <http://pandas.pydata.org/pandas-docs/stable/groupby.html>`_.

Given the data frame from pervious section, we can split data by category::

    >>> g_data = data.groupby('cat')

Convert points to line string objects using
:py:func:`geocoon.as_line_string` function::

    >>> routes = geocoon.as_line_string(g_data.location)

Calculate time of first and last points of each line::

    >>> start = g_data.time.first()
    >>> end = g_data.time.last()

And finally compose the data into a report::

    >>> report = geocoon.GeoDataFrame({
    ...     'start': start,
    ...     'end': end,
    ...     'route': routes,
    ... })
    >>> report
         end                  route  start
    cat                                   
    a      4  LINESTRING (1 1, 4 4)      1
    b      3  LINESTRING (2 2, 3 3)      2
    <BLANKLINE>
    [2 rows x 3 columns]


.. vim: sw=4:et:ai
