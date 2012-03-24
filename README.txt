pyautoacad - AutoCAD Automation for Python
------------------------------------------

Requires:
----------

- comtypes_


Optional:
    
- xlrd_, tablib_


Feautures:
-----------

- Simplifies work with coordinates (3D points)
- Efficient objects iteration (with casting to correct type)
- Excel/csv import and export (optional)

Usage:
------

::

    from pyautocad import Autocad
    from pyautocad import APoint

    acad = Autocad()
    acad.prompt("Hello, Autocad from Python\n")
    print acad.doc.Name

    p1 = APoint(0, 0)
    for i in range(5):
        acad.model.AddMText(p1, 10, u'Hi!')
        p1.y += 10
    p2 = APoint(0, 0)
    acad.model.AddLine(p2, p2 + APoint(0, 100))

    dp = APoint(10, 0)
    for mtext in acad.iter_objects('MText'):
        print mtext.TextString, mtext.InsertionPoint
        mtext.InsertionPoint = APoint(mtext.InsertionPoint) + dp
        # or
        # p = APoint(mtext.InsertionPoint)
        # p.x += 10
        # mtext.InsertionPoint = p

See more examples_ in source distribution. 

.. _comtypes: http://pypi.python.org/pypi/comtypes
.. _xlrd: http://pypi.python.org/pypi/xlrd
.. _tablib: http://pypi.python.org/pypi/tablib
.. _examples: https://bitbucket.org/reclosedev/pyautocad/src/tip/examples
