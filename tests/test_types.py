#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 17.01.12
import unittest

from pyautocad.types import APoint, distance


class PointTestCase(unittest.TestCase):
    def test_point_ops(self):
        p1 = APoint(1, 1, 1)
        p2 = APoint(1, 1, 1)
        p3 = APoint(2, 2, 2)
        p4 = APoint(2, 2, 2)

        self.assertEqual(p1 + p2, (2, 2, 2))
        self.assertEqual(p1 - p3, (-1, -1, -1))
        self.assertEqual(p1 * p2, p1)
        self.assertEqual(p3 * p4, (4, 4, 4))
        self.assertEqual(p3 / p4, p1)

        self.assertEqual(p1 + 1, (2, 2, 2))
        self.assertEqual(p2 * 4, p3 * 2)
        self.assertEqual(p3 * 10, (20, 20, 20))
        self.assertEqual(p3 / 2, p1)
        self.assertEqual(p1 / 0.5, p3)

        self.assertEqual(-p1, (-1, -1, -1))

    def test_point_iops(self):
        p1 = APoint(1, 1, 1)
        p2 = APoint(2, 2, 2)
        p3 = APoint(3, 3, 3)

        p1 += 2
        p2 += p3
        self.assertEqual(p1, p3)
        self.assertEqual(p2, (5, 5, 5))

        p1 = APoint(1, 1, 1)
        p2 = APoint(2, 2, 2)
        p1 -= 2
        p2 -= p3
        self.assertEqual(p1, (-1, -1, -1))
        self.assertEqual(p2, (-1, -1, -1))
        p = APoint(5, 5, 5)
        p /= 2.0
        self.assertEqual(p, (2.5, 2.5, 2.5))
        p *= 2
        self.assertEqual(p, (5, 5, 5))

    def test_args(self):
        wrong_args = ['123', (1,2), [1,2,3,4]]
        for arg in wrong_args:
            with self.assertRaises(TypeError):
                p = APoint(arg)
                print arg

        p = APoint(0, 0, 0)
        for arg in wrong_args:
            try:
                p += arg
                self.fail('Wrong arg passed')
            except Exception:
                pass

    def test_attributes(self):
        p1 = APoint(1, 1, 1)
        p1.x += 1
        p1.y += 1
        p1.z += 1
        self.assertEqual(p1, (2, 2, 2))

    def test_distance(self):
        p1 = APoint(10, 10, 10)
        p2 = APoint(15, 15, 15)
        self.assertAlmostEqual(p1.distance_to(p2), 8.660254037844387)
        self.assertEqual(distance(p1, p2), distance(p2, p1))


if __name__ == '__main__':
    unittest.main()
