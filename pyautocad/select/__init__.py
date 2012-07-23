#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. versionadded:: 0.2.0

    pyautocad.select
    ~~~~~~~~~~~~~~~~

    Add objects to Selection sets in Django-ORM like fashion
"""
import array
import comtypes
from comtypes import partial

from .converter import convert_tree, ConverterError
from .query_tree import Q

__all__ = ['Q', 'ConverterError']

try:
    from comtypes.gen import AutoCAD
except ImportError:
    AutoCAD = None

# add select method to IAcadDocument
if AutoCAD is not None:  # 
    class _(partial.partial, AutoCAD.IAcadDocument):
        def select(self, *args, **kwargs):
            tree = Q(*args, **kwargs)
            types, data = convert_tree(tree)
            return _ssget(self.SelectionSets, types, data)


    def _ssget(selection_sets, filter_type, filter_data,
               selection=AutoCAD.acSelectionSetAll, name="SS_1__"):
        try:
            selection_sets.Item(name).Delete()
        except Exception:
            pass
        sset = selection_sets.Add(name)
        try:
            sset.Select(
                selection,
                FilterType=array.array('h', filter_type),
                FilterData=filter_data,
            )
        except comtypes.COMError as e:
            print e.details[0]
            raise
        return sset






