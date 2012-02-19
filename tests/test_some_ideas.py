#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 13.02.12
import unittest

from pyautocad import Autocad
import tablib


def sort_by_correct_order(messed_order, correct_order):
    return [x for x in correct_order if x in messed_order] + \
           [x for x in messed_order if x not in correct_order]

class MyTestCase(unittest.TestCase):
    def test_sort_by_correct(self):
        correct = ['TP', 'VRU', 'SHR', 'SHO', 'LAMP']
        new_seq = ['SHR', 'VRU', 'LAMP', 'SHO', 'STANOK']
        print sort_by_correct_order(new_seq, correct)

    def test_tablib(self):
        d = tablib.Dataset([1,2,3], [4,5,6])
        with self.assertRaises(tablib.InvalidDimensions):
            d.append([1,2,3,4,5])


if __name__ == '__main__':
    unittest.main()
