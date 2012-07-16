#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comtypes.partial import partial

import pyautocad
from .query import Query


def install():
    """ Add method ``filter`` to IAcadBlock and all its children
    """
    print 'registering PartialBlock'
    class PartialBlock(partial, pyautocad.ACAD.IAcadBlock):
        def filter(self, **kwargs):
            q = Query(kwargs)
            count = self.Count
            for i in xrange(count):
                obj = self.Item(i)
                matches, obj = q.execute(obj)
                if matches:
                    yield obj

    return PartialBlock