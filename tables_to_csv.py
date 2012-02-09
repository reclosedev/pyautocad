#!python
#-*- coding: utf-8 -*-
import time
import re
import codecs

from pyautocad import Autocad
from pyautocad.utils import distance, mtext_to_string
from pyautocad.point import APoint


file = codecs.open("kab_zhurnal.csv", "w", encoding='cp1251')
acad = Autocad()

def convert_tables_from_layouts():
    for layout in sorted(acad.doc.Layouts, key=lambda x: x.TabOrder):
        if not layout.TabOrder:
            continue  # skip Model space
        table = None
        for obj in acad.iter_objects("table", layout.Block):
            if obj.Columns == 9:
                table = obj
                break
        if not table:
            continue
        print 'Processing', layout.Name
        ncols = table.Columns
        nrows = table.Rows

        for row in xrange(3, nrows):
            for col in xrange(ncols):
                file.write('%s;' % mtext_to_string(table.GetText(row, col)))
            file.write('\n')

begin_time = time.time()
convert_tables_from_layouts()
print "Elapsed: %.4f" % (time.time() - begin_time)