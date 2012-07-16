#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import pyautocad
from pyautocad import Autocad, APoint
import time
from pyautocad import filter
filter.install()  # TODO change API


acad = Autocad()


def entity_fields():
    res = []
    for obj in acad.model.filter():
        for attr in dir(obj):
            if attr.startswith('_'):
                continue
            val = getattr(obj, attr)
            if not callable(val):
                res.append(attr)
        break
    print(res)


def main():
    gen = acad.model.filter(
        ObjectName__in=['AcDbMText', 'AcDbText'],
        TextString__contains=u'с',
        InsertionPoint__gt=(0, -182135.6516, 0)
    )
    for i, obj in enumerate(gen):
        print i, obj.ObjectName, obj.TextString


def main1():
    for obj in acad.iter_objects('MText'):
        if u'сизу' in obj.TextString:
            print obj.ObjectName, obj.TextString


def main():
    gen = acad.model.filter(
        ObjectName__in=['AcDbMText', 'AcDbText'],
        #TextString__contains=u'с',
        TextString__len__lt=3,
        TextString__startswith=u'5',
        #TextString__0=u'5',
        #TextString__1=u'0',
        #InsertionPoint__0__range=(11206, 11211)
        #InsertionPoint__x=100, InsertionPoint__y__lt=100.1,
        #InsertionPoint__y__range=(50, 110)
    )
    for i, obj in enumerate(gen):
        print i, obj.ObjectName, obj.InsertionPoint, obj.TextString

if __name__ == '__main__':
    t = time.time()
    main()
    print "Elapsed %0.3f" % (time.time() - t)
