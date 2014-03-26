Examples
========
Create points

.. doctest::

    >>> from shapely.geometry import Point
    >>> import geocoon
    >>> shapes = Point(1, 1), Point(2, 2)
    >>> points = geocoon.from_shapes(shapes)
    >>> points
    0    POINT (1 1)
    1    POINT (2 2)
    dtype: object
    >>> points.x
    0    1
    1    2
    dtype: float64

Create data frame

.. doctest::

    >>> ends = ['a', 'b']
    >>> data = geocoon.GeoDataFrame({'point': points, 'end': ends})
    >>> data
     end        point
    0   a  POINT (1 1)
    1   b  POINT (2 2)
    <BLANKLINE>
    [2 rows x 2 columns]

Query a data frame

.. doctest::

    >>> data[data.end == 'a']
    0   a  POINT (1 1)
    <BLANKLINE>
    [1 rows x 2 columns]

.. vim: sw=4:et:ai
