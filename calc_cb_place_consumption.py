#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re
import codecs

from pyautocad import Autocad
from pyautocad.utils import distance, mtext_to_string
from pyautocad.point import APoint

acad = Autocad()

def convert_tables_from_layouts():
    print '%-15s| %s' % (u'Имя щита', u'Общее число модулей')
    for layout in sorted(acad.doc.Layouts, key=lambda x: x.TabOrder):
        if not layout.TabOrder:
            continue  # skip Model space
        table = None
        for obj in acad.iter_objects("table", layout.Block):
            if obj.Columns == 5:
                table = obj
                break
        if not table:
            continue
 
        total_modules = 0
        for row in xrange(table.Rows):
            item_str = mtext_to_string(table.GetText(row, 2))
            m = re.match(ur'(\d)[PР].*', item_str)
            if not m:
                continue
            n_modules = int(m.group(1))
            quantity = int(mtext_to_string(table.GetText(row-1, 3)))
            total_modules += n_modules * quantity
        print '%-15s| %s' % (layout.Name, total_modules)

begin_time = time.time()
convert_tables_from_layouts()
print "Elapsed: %.4f" % (time.time() - begin_time)