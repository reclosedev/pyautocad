#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
from _ctypes import COMError
from pprint import pprint
import unittest
import timeit
import inspect
import comtypes.client
import time

from pyautocad import Autocad, aDouble, aShort, aInt

import comtypes.gen._851A4561_F4EC_4631_9B0C_E7DC407512C9_0_1_0 as r
from pyautocad.point import APoint

NPASS = 3000


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.acad = Autocad(True)
        #self.doc = self.acad.app.Documents.Add()
        self.doc = self.acad.doc
        print 'Current', self.doc.Name

    def tearDown(self):
        pass
        #self.doc.Close(False)

    def test_points_arguments(self):
        model = self.acad.model
        p1 = APoint(0, 0, 0)
        for i in range(10):
            model.AddCircle(p1 * i, i + 1)
            p1 += i

        for circle in self.acad.iter_objects('circle'):
            cp = APoint(circle.Center)
            model.AddCircle(-cp, circle.Radius)
            print -cp
        #print c1.Center

    def test_types(self):
        model = self.acad.model
        p1 = (0, 0, 0)
        p2 = (10, 10, 0)
        p3 = tuple(p+10 for p in p2)

        model.AddLine(aDouble(p1), aDouble(p2))
        model.AddLine(aDouble(p2), aDouble(p3))
        lines = list(self.acad.iter_objects())
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].StartPoint, p1)
        self.assertEqual(lines[0].EndPoint, p2)
        self.assertEqual(lines[1].StartPoint, p2)
        self.assertEqual(lines[1].EndPoint, p3)
        with self.assertRaises(COMError):
            model.AddLine(aDouble(0, 0), aDouble(0, 0, 0))

    def test_text(self):
        model = self.acad.model
        text1 = u'Русский текст'
        text2 = u'With paragraph \PYes'

        t1 = model.AddText(text1, aDouble(0, 0, 0), 10)
        t2 = model.AddText(text2, aDouble(10, 10, 0), 10)

        self.assertEqual(type(t1.TextString), unicode)
        self.assertEqual(t1.TextString, text1)
        self.assertEqual(t2.InsertionPoint, (10, 10, 0))
        self.assertNotEqual(t2.InsertionPoint, (10, 10, 1))

    def test_multitext(self):
        model = self.acad.model
        text1 = 'Line1\nLine2\nLine3\\'
        text2 = 'Line1\\PLine2\\PLine3\\P'

        t1 = model.AddMText(aDouble(0,0,0), 10, text1)
        t2 = model.AddMText(aDouble(10,10,0), 10, text2)
        print t1.TextString
        print t2.TextString
        #self.acad.doc.Utility.GetString(True, u'\nEnter something')



if __name__ == '__main__':
    unittest.main()
