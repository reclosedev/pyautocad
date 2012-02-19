#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 13.02.12
import unittest

from pyautocad.contrib import tables
import tablib


class TableTestCase(unittest.TestCase):

    def test_tablib(self):
        d = tablib.Dataset([1,2,3], [4,5,6])
        with self.assertRaises(tablib.InvalidDimensions):
            d.append([1,2,3,4,5])

    def test_table_create(self):
        t = tables.Table()
        t.writerow([1]*3)
        t.writerow([2]*3)
        t.writerow([3]*3)
        with self.assertRaises(tablib.InvalidDimensions):
            t.writerow([4]*4)
        self.assertEqual(t._dataset.dict, [[1]*3, [2]*3, [3]*3])


if __name__ == '__main__':
    unittest.main()
