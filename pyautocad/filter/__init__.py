#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comtypes.partial import partial

import pyautocad
from .query import QuerySet


def install():
    """ Add method ``filter`` to IAcadBlock and all its children
    """
    print 'registering PartialBlock'
    class PartialBlock(partial, pyautocad.ACAD.IAcadBlock):
        def filter(self, **kwargs):
            return QuerySet(kwargs, self)

    return PartialBlock