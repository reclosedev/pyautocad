Getting started
===============

Installation
------------

If you have pip_ or easy_install_, you can just::

    pip install --upgrade pyautocad

or::

    easy_install -U pyautocad

Also, you can download Windows installer from PyPI pyautocad_ page.

.. _pyautocad: http://pypi.python.org/pypi/pyautocad/
.. _pip: http://pypi.python.org/pypi/pip/
.. _easy_install: http://pypi.python.org/pypi/setuptools

Requirements
------------

- comtypes_
    .. note::

        If you are using pip_ or easy_install_, then it will be installed automatically.
        Otherwise you should install comtypes_ package manually.

- Optional: xlrd_ and tablib_ for working with tables

.. _comtypes: http://pypi.python.org/pypi/comtypes/
.. _xlrd: http://pypi.python.org/pypi/xlrd
.. _tablib: http://pypi.python.org/pypi/tablib

Retrieving AutoCAD ActiveX documentation
----------------------------------------

A copy of the AutoCAD ActiveX guide and reference can be found in the ``help`` directory of your AutoCAD install.


- ``acad_aag.chm`` - ActiveX and VBA Developer's Guide
- ``acadauto.chm`` - ActiveX and VBA Reference

Reference can also be found in ``C:\Program Files\Common Files\Autodesk Shared\acadauto.chm``

What's next?
------------

Read the :doc:`usage` section, or look for real applications in examples_ folder of source distribution.

.. note::

    Applications in examples_ are Russian engineering specific, but anyway
    I hope you'll find something interesting in that code.

For more info on features see :doc:`api` documentation and sources_.

.. _examples: https://github.com/reclosedev/pyautocad/tree/master/examples
.. _sources: https://github.com/reclosedev/pyautocad

