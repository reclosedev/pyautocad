Getting started
===============

Installation
------------

If you have pip_ or easy_install_, you can just::

    pip install upgrade pyautocad

or::

    easy_install -U pyautocad

Also, you can download Windows installer from PyPI pyautocad_ page.

.. _pyautocad: http://pypi.python.org/pypi/pyautocad/
.. _pip: http://pypi.python.org/pypi/pip/
.. _easy_install: http://pypi.python.org/pypi/setuptools

Requirements
------------

If you are using pip_ or easy_install_, then all required modules are installed automatically,
if not, then you should manually setup comtypes_ package.

For working with tables, xlrd_ and tablib_ are required.

.. _comtypes: http://pypi.python.org/pypi/comtypes/
.. _xlrd: http://pypi.python.org/pypi/xlrd
.. _tablib: http://pypi.python.org/pypi/tablib

AutoCAD documentation
----------------------

A copy of the AutoCAD ActiveX guide and reference can be found the ``help`` directory of your AutoCAD install.


- ``acad_aag.chm`` - ActiveX and VBA Developer's Guide
- ``acadauto.chm`` - ActiveX and VBA Reference

Reference can also be found in ``C:\Program Files\Common Files\Autodesk Shared\acadauto.chm``

Usage
-----

.. module:: pyautocad.api


For our first example, we will use :class:`Autocad` (main Automation object) and
:class:`pyautocad.types.APoint` for operations with coordinates::

    from pyautoacd import Autocad, APoint

Let's create AutoCAD application or connect to already running application::

    acad = Autocad(create_if_not_exists=True)
    acad.prompt("Hello, Autocad from Python\n")

To work with AutoCAD documents and objects we can use ActiveX interface,
:class:`Autocad` contains some methods to simplify common Automation tasks, such as
object iteration and searching, getting objects from user's selection, printing messages.

There are shortcuts for current ``ActiveDocument`` :attr:`Autocad.doc`
and ``ActiveDocument.ModelSpace`` :attr:`Autocad.model`

Let's add some objects to document::

    p1 = APoint(0, 0)
    p2 = APoint(50, 25)
    for i in range(5):
        text = acad.model.AddText(u'Hi %s!' % i, p1, 2.5)
        acad.model.AddLine(p1, p2)
        acad.model.AddCircle(p1, 10)
        p1.y += 10

Now our document contains some ``Texts``, ``Lines`` and ``Circles``, let's iterate them all::

    for obj in acad.iter_objects():
        print obj.ObjectName

Wea also can iterate objects of concrete type::

    for mtext in acad.iter_objects('MText'):
        print mtext.TextString, mtext.InsertionPoint

Or multiple types::

    for obj in acad.iter_objects(['Text', 'Line']):
        print obj.ObjectName

Also we can find first object with some conditions (common task). For example, let's find text item which contains ``3``::

    def text_contains_3(text_obj):
        return '3' in text_obj.TextString

    text = acad.find_one('Text', predicate=text_contains_3)

To modify objects in document, we need to find interesting objects, and change it properties.
Some properties are described with constants, e.g. text alignment. These constants can be accessed through
:data:`ACAD`. Let's change all text objects text alignment::

    from pyautocad import ACAD

    for text in acad.iter_objects('Text'):
        old_insertion_point = APoint(text.InsertionPoint)
        text.Alignment = ACAD.acAlignmentRight
        text.TextAlignmentPoint = old_insertion_point

In previous code we have converted text.InsertionPoint to :class:`APoint` because
we can't just use default ``tuple`` when setting another properties such as ``text.TextAlignmentPoint``.

If wee need to change position of some object, we should use :class:`APoint`, for example let's
change lines end position::

    for line in acad.iter_objects('Line'):
        p1 = APoint(line.StartPoint)
        line.EndPoint = p1 - APoint(20, 0)

