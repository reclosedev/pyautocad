#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyautocad import Autocad, APoint
from pyautocad.contrib.tables import Table

acad = Autocad()
p1 = APoint(0, 0)
for i in range(5):
    obj = acad.model.AddText(u'Hi %s!' % i, p1, 2.5)
    p1.y += 10

table = Table()
for obj in acad.iter_objects('Text'):
    x, y, z = obj.InsertionPoint
    table.writerow([obj.TextString, x, y, z])
table.save('data.xls', 'xls')

data = Table.data_from_file('data.xls')

