#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 13.02.12
import unittest

from pyautocad import Autocad


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

def main():
    acad = Autocad()
    layout = acad.iter_layouts().next()
    table = acad.iter_objects('table', layout.Block).next()
    merged = set()
    for row in range(3):
        for col in range(table.Columns):
            minRow, maxRow, minCol, maxCol, is_merged = table.IsMergedCell(row, col)
            if is_merged:
                merged.add((minRow, maxRow, minCol, maxCol,))
            print is_merged
            # print row, col, table.GetText(row, col), table.GetColumnWidth(col), table.GetDataFormat(row, col, 1000)
        print
    print merged

if __name__ == '__main__':
    unittest.main()
