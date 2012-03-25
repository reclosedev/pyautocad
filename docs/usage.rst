Usage
=====

Main interface and types
-------------------------

.. currentmodule:: pyautocad.api


For our first example, we will use :class:`Autocad` (main Automation object) and
:class:`pyautocad.types.APoint` for operations with coordinates

.. literalinclude:: example.py
   :lines: 3

Let's create AutoCAD application or connect to already running application:

.. literalinclude:: example.py
   :lines: 5-7

To work with AutoCAD documents and objects we can use ActiveX interface,
:class:`Autocad` contains some methods to simplify common Automation tasks, such as
object iteration and searching, getting objects from user's selection, printing messages.

There are shortcuts for current ``ActiveDocument`` - :attr:`Autocad.doc`
and ``ActiveDocument.ModelSpace`` - :attr:`Autocad.model`

Let's add some objects to document:

.. literalinclude:: example.py
   :lines: 9-15

Now our document contains some ``Texts``, ``Lines`` and ``Circles``, let's iterate them all:

.. literalinclude:: example.py
   :lines: 17-18

Wea also can iterate objects of concrete type:

.. literalinclude:: example.py
   :lines: 20-21

Or multiple types:

.. literalinclude:: example.py
   :lines: 23-24

Also we can find first object with some conditions (common task).
For example, let's find first text item which contains ``3``:

.. literalinclude:: example.py
   :lines: 26-30

To modify objects in document, we need to find interesting objects, and change its properties.
Some properties are described with constants, e.g. text alignment. These constants can be accessed through
:data:`ACAD`. Let's change all text objects text alignment:

.. literalinclude:: example.py
   :lines: 32-37

.. currentmodule:: pyautocad.types

In previous code we have converted text.InsertionPoint to :class:`APoint` because
we can't just use default ``tuple`` when setting another properties such as ``text.TextAlignmentPoint``.

If wee need to change position of some object, we should use :class:`APoint`, for example let's
change lines end position:

.. literalinclude:: example.py
   :lines: 39-41


Working with tables
-------------------

.. note::

    To work with tables, xlrd_ and tablib_ should be installed.

.. _xlrd: http://pypi.python.org/pypi/xlrd
.. _tablib: http://pypi.python.org/pypi/tablib

.. currentmodule:: pyautocad.contrib.tables

To simplify importing and exporting data there is :class:`Table` class exist.
It allows you to read and write tabular data in popular formats:

- csv
- xls
- xlsx (write only)
- json

Let's try to solve some basic task. We need to save text and position
from all text ojbects to Excel file, and then load it back.

First we need to add some objects to AutoCAD:

.. literalinclude:: example_tables.py
   :lines: 3-10

Now we can to iterate this objects and save them to Excel table:

.. literalinclude:: example_tables.py
   :lines: 12-16

To retrieve data from file:

.. literalinclude:: example_tables.py
   :lines: 18

``data`` will contain::

    [[u'Hi 0!', 0.0, 0.0, 0.0],
     [u'Hi 1!', 0.0, 10.0, 0.0],
     [u'Hi 2!', 0.0, 20.0, 0.0],
     [u'Hi 3!', 0.0, 30.0, 0.0],
     [u'Hi 4!', 0.0, 40.0, 0.0]]

Utility functions
-----------------

There is also some utility functions for work with AutoCAD text objects and more.
See :mod:`pyautocad.utils` documentation.

