#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

