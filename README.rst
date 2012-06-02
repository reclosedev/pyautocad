pyautoacad - AutoCAD Automation for Python
------------------------------------------

This library aimed to simplify writing ActiveX_ Automation_ scripts for AutoCAD_ with Python

Requires:
----------

- comtypes_


Optional:
    
- xlrd_, tablib_


Feautures:
-----------

- Simplifies work with coordinates (3D points)
- Efficient objects iteration and searching (with casting to correct type)
- Excel/csv/json import and export (xlrd_ and tablib_ required)

Simple usage example:
---------------------

::

    from pyautocad import Autocad, APoint


    acad = Autocad()
    acad.prompt("Hello, Autocad from Python\n")
    print acad.doc.Name

    p1 = APoint(0, 0)
    p2 = APoint(50, 25)
    for i in range(5):
        text = acad.model.AddText('Hi %s!' % i, p1, 2.5)
        acad.model.AddLine(p1, p2)
        acad.model.AddCircle(p1, 10)
        p1.y += 10

    dp = APoint(10, 0)
    for text in acad.iter_objects('Text'):
        print('text: %s at: %s' % (text.TextString, text.InsertionPoint))
        text.InsertionPoint = APoint(text.InsertionPoint) + dp

    for obj in acad.iter_objects(['Circle', 'Line']):
        print(obj.ObjectName)

See more examples_ in source distribution.

Links
-----

- **Documentation** at `readthedocs.org <http://readthedocs.org/docs/pyautocad/>`_

- **Source code and issue tracking** at `GitHub <https://github.com/reclosedev/pyautocad>`_.

.. _ActiveX: http://wikipedia.org/wiki/ActiveX
.. _Automation: http://en.wikipedia.org/wiki/OLE_Automation
.. _AutoCAD: http://wikipedia.org/wiki/AutoCAD
.. _comtypes: http://pypi.python.org/pypi/comtypes
.. _xlrd: http://pypi.python.org/pypi/xlrd
.. _tablib: http://pypi.python.org/pypi/tablib
.. _examples: https://github.com/reclosedev/pyautocad/tree/master/examples
.. _documentation: http://readthedocs.org/docs/pyautocad/
