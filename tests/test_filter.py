#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from pyautocad import Autocad, aDouble, aShort, aInt, APoint
import pyautocad.filter
from pyautocad.filter.query import UnknownOperation

pyautocad.filter.install()


class ApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.acad = Autocad(True)
        cls.doc = cls.acad.app.Documents.Add()
        print 'Current', cls.doc.Name

        model = cls.acad.model
        p1 = APoint(0, 0, 0)
        p2 = APoint(10, 10, 0)
        cls.n_lines = n_lines = 10
        cls.n_texts = n_texts = 15
        for i in range(n_lines):
            model.AddLine(p1, p2)
            p1.y += 10
        for i in range(n_texts):
            model.AddMText(p2, 10, u'Dummy %s' % i)
            p2.x += 10

    @classmethod
    def tearDownClass(cls):
        #pass
        cls.doc.Close(False)

    def test_count_objects(self):
        model = self.acad.model
        self.assertEqual(model.filter(ObjectName__contains='Line').count(), self.n_lines)
        self.assertEqual(model.filter(ObjectName__contains='MText').count(), self.n_texts)
        self.assertEqual(model.filter(ObjectName__in_part=['Line', 'MText']).count(), self.n_lines + self.n_texts)

    def test_operations(self):
        model = self.acad.model
        test_set = [
            ({'InsertionPoint__x__lt': 15}, 1),
            ({'InsertionPoint__x__lt': 15}, 1),
            ({'InsertionPoint__z__gt': 0}, 0),
            ({'InsertionPoint__x__gt': 10}, self.n_texts - 1),
            ({'StartPoint__y__ge': 0}, self.n_lines),
            ({'StartPoint__y__gt': 0}, self.n_lines - 1),
            ({'InsertionPoint__x__range': (20, 40)}, 3),
            ({'InsertionPoint__x__in': (20, 40)}, 2),
            ({'TextString__contains': u'Dummy'}, self.n_texts),
            ({'TextString__icontains': u'DuMmy'}, self.n_texts),
            ({'TextString__startswith': u'Dummy'}, self.n_texts),
            ({'TextString__rem': ur'Dummy \d+'}, self.n_texts),
            ({'TextString__re': ur'\d+'}, self.n_texts),
            ({'TextString__rem': ur'\d+'}, 0),
            ({'TextString__endswith': u'9'}, 1),
            ({'TextString__len': 7}, 10),
            ({'TextString__0': u'D'}, self.n_texts),
        ]
        for dct, result in test_set:
            self.assertEqual(model.filter(**dct).count(), result)

    def test_exceptions(self):
        model = self.acad.model
        with self.assertRaises(UnknownOperation):
            model.filter(InsertionPoint__awesome=True).first()

    def test_iteration_and_cache(self):
        model = self.acad.model
        qs = model.filter()
        qs.first()
        with self.assertRaises(AssertionError):
            qs.all()
        qs = model.filter()
        n = qs.count()
        for _ in qs:
            n -= 1
        self.assertEqual(n, 0)
        self.assertEqual(len(qs), qs.count())
        qs.first()
        qs = model.filter(ObjectName__contains='Line')
        self.assertEqual(qs.filter(Length__gt=15).count(), 7)
        qs = model.filter(ObjectName__contains='Line').best_interface()
        for obj in qs:
            self.assert_(hasattr(obj, 'StartPoint'))

if __name__ == '__main__':
    unittest.main()
