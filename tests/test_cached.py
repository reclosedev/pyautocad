#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
import unittest
import mock

from pyautocad.cache import Cached


class C(object):
    def __init__(self):
        self._x = None

    def getx(self):
        print "get x"
        return self._x

    def setx(self, value):
        print "set x", value
        self._x = value

    x = property(lambda self: self.getx(), lambda self, x: self.setx(x))

    def modify(self, val):
        print "modify", val
        self._x = val


class CachedTestCase(unittest.TestCase):
    def test_caching_attributes(self):
        a = C()

        a.x = 1
        ac = Cached(a)
        self.assertEqual(ac.x, 1)
        a.modify(2)
        self.assertEqual(ac.x, 1)
        a.x = 2

        self.assertEqual(ac.x, 1)
        ac.modify(2)
        self.assertEqual(ac.x, 1)

        ac.x = 3
        self.assertEqual(ac.x, 3)
        self.assertEqual(a.x, 3)
        with self.assertRaises(AttributeError):
            y = ac.y
        ac.y = 10
        self.assertEqual(a.y, ac.y)
        self.assert_('y' in ac._storage)
        del ac.y
        with self.assertRaises(AttributeError):
            y = ac.y
        with self.assertRaises(AttributeError):
            del ac.z

        self.assertIs(ac.get_original(), a)

        a = C()
        ac = Cached(a)
        a.getx = mock.Mock(name='getx', return_value=1)
        for i in range(5):
            _ = ac.x
        self.assertEqual(a.getx.call_count, 1)
        ac.switch_caching(False)
        for i in range(5):
            _ = ac.x
        self.assertEqual(a.getx.call_count, 5 + 1)

    def test_caching_off(self):
        a = C()
        a.x = 1
        ac = Cached(a)
        a.x = 3
        self.assertEqual(ac.x, 3)
        a.x = 5
        self.assertEqual(ac.x, 3)
        ac.x = 5
        self.assertEqual(ac.x, 5)
        self.assertEqual(a.x, 5)
        ac.switch_caching(False)
        a.x = 7
        self.assertEqual(ac.x, 7)
        a.x = 8
        self.assertEqual(ac.x, 8)
        ac.switch_caching(True)
        a.x = 9
        self.assertEqual(ac.x, 8)


if __name__ == '__main__':
    unittest.main()
