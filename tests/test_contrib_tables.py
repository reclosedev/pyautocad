#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 13.02.12
import os
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
        t.append([3]*3)
        with self.assertRaises(tablib.InvalidDimensions):
            t.writerow([4]*4)
        self.assertEqual(t.dataset.dict, [[1]*3, [2]*3, [3]*3])
        t.clear()
        t.writerow([1]*3)
        self.assertEqual(t.dataset.dict, [[1]*3])

    def test_table_unknown_format(self):
        t = tables.Table()
        t.writerow([1]*3)
        with self.assertRaises(tables.FormatNotSupported):
            t.save('tst', 'any_nonexistent')
        with self.assertRaises(tables.FormatNotSupported):
            t = tables.Table.data_from_file('tst', 'any_nonexistent')

    def test_write_read_encoding(self):
        t = tables.Table()
        row = [u'Привет, мир', u'мирtabbed', 'some']
        data = [row]
        t.writerow(row)
        #for fmt in tables.available_write_formats():
        for fmt in tables.available_read_formats():
            filename = 'test_hello.%s' % fmt
            t.save(filename, fmt)
            t2 = tables.Table.data_from_file(filename, fmt)
            self.assertEqual(t2, data)
            t2 = tables.Table.data_from_file(filename)
            self.assertEqual(t2, data)
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
