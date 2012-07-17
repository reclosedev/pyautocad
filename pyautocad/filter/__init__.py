#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comtypes.partial import partial

import pyautocad
from .query import QuerySet


def install():
    """ Add method ``filter`` to IAcadObject and all its children
    """
    class AcadObjectAdditions(partial, pyautocad.ACAD.IAcadObject):
        def filter(self, **kwargs):
            assert hasattr(self, 'Count'), "Object %r is not iterable" % self
            return QuerySet(kwargs, self)

    return AcadObjectAdditions