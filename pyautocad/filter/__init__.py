#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comtypes.partial import partial
from .query import QuerySet, UnknownOperation

__all__ = ['UnknownOperation']

try:
    from comtypes.gen import AXDBLib
except ImportError:
    AXDBLib = None
try:
    from comtypes.gen import AutoCAD
except ImportError:
    AutoCAD = None


# wee need to add filter to two libraries
for lib in (AutoCAD, AXDBLib):
    if lib is not None:
        class _(partial, lib.IAcadObject):
            def filter(self, *object_names, **kwargs):
                assert hasattr(self, 'Count'),\
                "Object %r is not iterable" % self
                return QuerySet(object_names, kwargs, self)
