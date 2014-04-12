Introduction
============
GeoCoon is GIS data analysis Python library, which integrates Pandas data
frames with Shapely GIS geometries.

The library provides means to load GIS data in a form of Shapely objects
into Pandas data frame and analyze data using Pandas idioms. It allows to
access attributes and call methods on Shapely geometries in a vectorized
manner.

GeoCoon library supports

#. Point, line string and polygon geometries (more to come).
#. Vectorized GIS object attribute access and method execution.
#. Pandas data selection and split-apply-combine idioms.
#. SQL/MM databases, i.e. `PostgreSQL <http://www.postgresql.org/>`_ with
   `PostGIS <http://postgis.org/>`_ extension.
#. Multiple geometry columns in a data frame.

The library API is driven by
`Simple Feature Access OGC standard <http://www.opengeospatial.org/standards/sfa>`_
and `Shapely API <http://toblerity.org/shapely/manual.html>`_, which design
is guided by OGC standard as well.

Installation
------------
To install GeoCoon use `pip <http://www.pip-installer.org/>`_::

    pip install --user geocoon

GeoCoon requires Shapely 1.3.0, Pandas 0.13.0 and Python 3.3 or later.

.. vim: sw=4:et:ai
