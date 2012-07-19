#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import unittest
import comtypes

from pyautocad import Autocad, aDouble, aShort, aInt, APoint, UnknownOperation, ConverterError, Q
from tests.test_filter import setUpClass, tearDownClass


class SelectTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setUpClass(cls)

    @classmethod
    def tearDownClass(cls):
        tearDownClass(cls)

    def test_operations(self):
        test_set = [
            #(Q(type='Circle', position_x=APoint(0)), 1),
            (Q(position=APoint(10, 10)), 1),
            #(Q(endpoint=APoint(10, 10)), 1),
            (Q(type='Circle', position=APoint(0, 0)), 1),
#            ({'InsertionPoint__x__lt': 15}, 1),
#            ({'InsertionPoint__z__gt': 0}, 0),
#            ({'InsertionPoint__x__gt': 10}, self.n_texts - 1),
#            ({'StartPoint__y__ge': 0}, self.n_lines),
#            ({'StartPoint__y__gt': 0}, self.n_lines - 1),
#            ({'InsertionPoint__x__range': (20, 40)}, 3),
#            ({'InsertionPoint__x__in': (20, 40)}, 2),
            ((Q(text="Dummy*"),  self.n_texts)),
            ((Q(text="Dummy #"),  10)),
            ((Q(text="Dummy ##"),  5)),
            ((Q(type="Circle", radius=10), 1)),
            ((Q(type="Circle", radius__lt=20), 1)),
            ((Q(type="Circle", radius__gt=20), self.n_circles - 2)),
            ((Q(type="Circle") | Q(type="Line"), self.n_circles + self.n_lines)),
            ((~Q(type="Mtext"), self.n_circles + self.n_lines)),
            ((Q(type="Mtext"), self.n_texts)),
        ]
        for q, result in test_set:
            self.assertEqual(self.doc.select(q).Count, result, q)

    def test_exceptions(self):

        with self.assertRaises(ConverterError):
            self.doc.select(unknown_field=1)

        with self.assertRaises(ConverterError):
            self.doc.select(center__asdf=1)



if __name__ == '__main__':
    unittest.main()
