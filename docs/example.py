#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyautocad import Autocad, APoint

acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello, Autocad from Python\n")
print acad.doc.Name

p1 = APoint(0, 0)
p2 = APoint(50, 25)
for i in range(5):
    text = acad.model.AddText(u'Hi %s!' % i, p1, 2.5)
    acad.model.AddLine(p1, p2)
    acad.model.AddCircle(p1, 10)
    p1.y += 10

for obj in acad.iter_objects():
    print obj.ObjectName

for text in acad.iter_objects('Text'):
    print text.TextString, text.InsertionPoint

for obj in acad.iter_objects(['Text', 'Line']):
    print obj.ObjectName

def text_contains_3(text_obj):
    return '3' in text_obj.TextString

text = acad.find_one('Text', predicate=text_contains_3)
print text.TextString

from pyautocad import ACAD

for text in acad.iter_objects('Text'):
    old_insertion_point = APoint(text.InsertionPoint)
    text.Alignment = ACAD.acAlignmentRight
    text.TextAlignmentPoint = old_insertion_point

for line in acad.iter_objects('Line'):
    p1 = APoint(line.StartPoint)
    line.EndPoint = p1 - APoint(20, 0)