API
===

This part of the documentation covers all the interfaces of `pyautocad`

``api`` - Main Autocad interface
--------------------------------------------

.. automodule:: pyautocad.api
   :members:

.. data:: ACAD

   Constants from AutoCAD type library, for example::

       text.Alignment = ACAD.acAlignmentRight

-----------------------------------------------------------------------------

``types`` - 3D Point and other AutoCAD data types
-------------------------------------------------

.. automodule:: pyautocad.types
   :members:

-----------------------------------------------------------------------------

``utils`` - Utility functions
-------------------------------------------------------------

.. automodule:: pyautocad.utils
   :members:
   :exclude-members: timing, suppressed_regeneration_of

   .. autofunction:: timing(message)
   .. autofunction:: suppressed_regeneration_of(table)





-----------------------------------------------------------------------------

``contrib.tables`` - Import and export tabular data from popular formats
------------------------------------------------------------------------

.. automodule:: pyautocad.contrib.tables
    :synopsis: test
    :members:

-----------------------------------------------------------------------------

``cache`` - Cache all object's attributes
------------------------------------------
.. versionadded:: 0.1.2

.. automodule:: pyautocad.cache
   :members: