#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import unittest
import comtypes

from pyautocad import Autocad, aDouble, aShort, aInt, APoint
from pyautocad.filter import UnknownOperation


# this functions used in another tests
def setUpClass(cls):
    cls.acad = Autocad(True)
    cls.doc = cls.acad.app.Documents.Add()
    print 'Current', cls.doc.Name

    model = cls.acad.model
    p1 = APoint(0, 0, 0)
    p2 = APoint(10, 10, 0)
    cls.n_lines = cls.n_circles = n_lines = 10
    cls.n_texts = n_texts = 15
    for i in range(n_lines):
        model.AddLine(p1, p2)
        model.AddCircle(p1, (i + 1) * 10)
        p1.y += 10
    cls.texts = []
    for i in range(n_texts):
        text = u'Dummy %s' % i
        cls.texts.append(text)
        model.AddMText(p2, 10, text)
        p2.x += 10

    cls.layouts_names = []
    for i in range(5):
        name = u'TESTLayout %s' % i
        cls.layouts_names.append(name)
        cls.doc.Layouts.Add(name)
    cls.n_layouts = cls.doc.Layouts.Count

def tearDownClass(cls):
    #pass
    cls.doc.Close(False)


class FilterTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setUpClass(cls)

    @classmethod
    def tearDownClass(cls):
        tearDownClass(cls)

    def test_count_objects(self):
        m = self.acad.model
        self.assertEqual(m.filter(ObjectName__contains='Line').count(),
                         self.n_lines)
        self.assertEqual(m.filter(ObjectName__contains='MText').count(),
                         self.n_texts)
        self.assertEqual(m.filter(ObjectName__in_part=['Line', 'MText']).count(),
                         self.n_lines + self.n_texts)

    def test_operations(self):
        model = self.acad.model
        self.assertEqual(model.filter('AcDbMText').count(), self.n_texts)
        self.assertEqual(model.filter('AcDbLine').count(), self.n_lines)
        self.assertEqual(model.filter('AcDbLine', 'AcDbMText').count(),
                         self.n_lines + self.n_texts)
        test_set = [
            ({'InsertionPoint__dist': ((10, 10, 0), 30.0)}, 1),
            ({'InsertionPoint__dist_lt': ((10, 10, 0), 30.0)}, 3),
            ({'InsertionPoint__dist_gt': ((10, 10, 0), 50.0)}, 9),
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

        qs = model.filter()
        self.assertEqual(len(qs[5:10]), 5)
        with self.assertRaises(AssertionError):
            print qs[10].ObjectName

        qs = model.filter()
        n = self.n_lines + self.n_texts + self.n_circles
        self.assertEqual(len(qs[5:]), n - 5)
        qs = model.filter(ObjectName__ne="AcDbCircle").best_interface()
        self.assertEqual(qs[1].StartPoint, (0, 10, 0))
        self.assertEqual(qs[2].StartPoint, (0, 20, 0))

        qs = model.filter()
        self.assertEqual(len(qs[:100]), n)

        qs = model.filter()
        self.assertEqual(len(qs[100:]), 0)
        self.assertEqual(len(qs[n - 5:]), 5)
        qs = model.filter()
        self.assertEqual(len(qs[100:n]), 0)
        qs = model.filter()
        self.assertEqual(len(qs[n - 5:n]), 5)

    def test_order_by(self):
        doc = self.doc
        model = self.acad.model
        qs = doc.Layouts.filter(TabOrder__ne=0, Name__startswith=u"TESTLayout")
        qs = qs.best_interface().order_by('-TabOrder')
        res = [obj.Name for obj in qs.all()]
        self.assertEqual(res, list(reversed(self.layouts_names)))

        qs = model.filter(ObjectName__icontains="dbmtext")
        qs = qs.best_interface().order_by('TextString__len', '-InsertionPoint__x')
        self.assertEqual(qs.all()[-1].TextString, u'Dummy 10')
        self.assertEqual(qs.all()[0].TextString, u'Dummy 9')

        def bad_attr1(strict):
            qs = model.filter(ObjectName__icontains="dbmtext")
            qs.best_interface().order_by('-InsertionPoint__x',
                                         'TextStringBAD', strict=strict)
            return True
        def bad_attr2(strict):
            qs = model.filter(ObjectName__icontains="dbmtext")
            qs.best_interface().order_by('TextString',
                                         '-InsertionBADPoint__x', strict=strict)
            return True

        self.assert_(bad_attr1(False) and bad_attr2(False))
        with self.assertRaises(AttributeError):
            bad_attr1(True)
        with self.assertRaises(AttributeError):
            bad_attr2(True)

    def test_issue_not_patched_dynamic(self):
        doc = self.doc
        layout = doc.Layouts.Item(1)
        self.assert_(hasattr(layout, 'filter'))
        layout = comtypes.client.GetBestInterface(layout)
        self.assert_(hasattr(layout, 'filter'))


if __name__ == '__main__':
    unittest.main()
