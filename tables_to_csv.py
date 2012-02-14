#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import time
import csv

from pyautocad import Autocad
from pyautocad.utils import mtext_to_string

def convert_tables_from_layouts(acad, writer):
    for layout in acad.iter_layouts():
        table = None
        for obj in acad.iter_objects("table", layout.Block):
            if obj.Columns == 9:
                table = obj
                break
        if not table:
            continue
        print 'Processing', layout.Name
        ncols = table.Columns
        for row in xrange(3, table.Rows):
            columns = [mtext_to_string(table.GetText(row, col)).encode('cp1251') for col in xrange(ncols)]
            writer.writerow(columns)
def main():
    acad = Autocad()
    filename = sys.argv[1] if sys.argv[1:] else 'kab_list.csv'
    writer = csv.writer(open(filename, "wb"), delimiter=';')
    convert_tables_from_layouts(acad, writer)

if __name__ == '__main__':
    begin_time = time.time()
    main()
    print "Elapsed: %.4f" % (time.time() - begin_time)