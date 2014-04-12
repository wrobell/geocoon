Using GeoCoon Library
=====================

Creating Data Frame and Series Objects
--------------------------------------
To analyze GIS data with GeoCoon library, it is required to create GIS data
frame and GIS series objects

* GIS series object is a collection of point, line string or other GIS
  objects supported by Shapely library
* GIS data frame references GIS series objects and enables programmer to
  analyze the data

GeoCoon supports various Shapely geometries. The mapping of Shapely classes
and GIS series is presented in the table below

    =============== ===================
     Shapely Class    GIS Series Class
    =============== ===================
     Point           PointSeries
     LineString      LineStringSeries
     Polygon         PolygonSeries
    =============== ===================

For example, to process point geometries, we create point series object::

    >>> from shapely.geometry import Point
    >>> import geocoon
    >>> series = geocoon.PointSeries([Point(1, 1), Point(2, 2), Point(3, 3)])
    >>> series
    0    POINT (1 1)
    1    POINT (2 2)
    2    POINT (3 3)
    dtype: object

and GIS data frame containing the point series object::

    >>> data = geocoon.GeoDataFrame({'location': series})
    >>> data
          location
    0  POINT (1 1)
    1  POINT (2 2)
    2  POINT (3 3)
    <BLANKLINE>
    [3 rows x 1 columns]

Adding GIS series to exisiting data frame is supported as well::

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
GeoCoon allows to load GIS data from SQL/MM databases like
`PostgreSQL <http://www.postgresql.org/>`_ with
`PostGIS <http://postgis.org/>`_ extension.

Data stored in SQL/MM database can be retrieved as a GIS data frame using
:py:func:`geocoon.read_sql` function.

For example, we might need to analyze GPS positions data as a time series
data.

Given the SQL table definition::

    create table position (
        timestamp timestamp,
        heading float,
        speed float,
        error float,
        primary key (timestamp)
    );

    select AddGeometryColumn('position', 'location', 4326, 'POINT', 3);

We can fetch the data as GIS data frame with time series index::

    >>> db = psycopg.connect(...) # doctest: +SKIP
    >>> sql = 'select timestamp, location, speed, heading, error from position' # doctest: +SKIP
    >>> data = geocoon.read_sql(sql, db, 'location', index_col='timestamp') # doctest: +SKIP

Other Sources of Data
~~~~~~~~~~~~~~~~~~~~~
Having any source of GIS data, GeoCoon allows to convert a collection of
geometries stored in WKB format into a GIS series using
:py:func:`geocoon.from_wkb` function.

Vectorized Data Access
----------------------
The purpose of GIS series classes is to provide vectorized access to
attributes and vectorized method calls - the attributes and methods mimic
Shapely geometries API.

Using the GIS data frame example from previous section, to access point `x`
coordinate::

    >>> data.location.x
    0    1
    1    2
    2    3
    dtype: float64

We can calculate buffer of each point::

    >>> pt_buffer = data.location.buffer(0.3)
    >>> pt_buffer
    0    POLYGON ((1.3 1, 1.298555418001659 0.970594857...
    1    POLYGON ((2.3 2, 2.298555418001659 1.970594857...
    2    POLYGON ((3.3 3, 3.298555418001659 2.970594857...
    dtype: object

As in the buffer example above, the vectorized methods can return GIS
series. Having buffer of each point, it is possible to calculate its area::

    >>> pt_buffer.area
    0    0.282289
    1    0.282289
    2    0.282289
    dtype: float64

The method vectorization works when first parameter of a GIS method is
another GIS object. For example, to calculate distance between two points::

    >>> points = geocoon.PointSeries([Point(1.1, 1.0), Point(2.2, 2.0), Point(3.3, 3.0)])
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
`Pandas split-apply-combine idioms <http://pandas.pydata.org/pandas-docs/stable/groupby.html>`_
allow to split data into various groups and analyze data within each group.
GeoCoon library integrates these Pandas operations.

The example below uses GIS data frame from previos section.

We can split data by category::

    >>> g_data = data.groupby('cat')

The points of each category can be converted to a line string geometries
using :py:func:`geocoon.as_line_string` function::

    >>> route = geocoon.as_line_string(g_data.location)

Time of first and last points of each line can be calculated using standard
Pandas methods::

    >>> start = g_data.time.first()
    >>> end = g_data.time.last()

Finally, we compose analyzed data into a report with start time, end time
and line length for each category::

    >>> report = geocoon.GeoDataFrame({})
    >>> report['start'] = start
    >>> report['end'] = end
    >>> report['length'] = route.length
    >>> report
         start  end    length
    cat                      
    a        1    4  4.242641
    b        2    3  1.414214
    <BLANKLINE>
    [2 rows x 3 columns]


.. vim: sw=4:et:ai
