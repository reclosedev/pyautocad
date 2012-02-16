#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 13.02.12
import pprint

from pyautocad import Autocad, utils


def print_table_info(table, print_rows=0):
    merged = set()
    column_widths = [round(table.GetColumnWidth(col), 2) for col in xrange(table.Columns)]
    row_heights = [round(table.GetRowHeight(row), 2) for row in xrange(table.Rows)]
    row_texts = []
    for row in range(table.Rows):
        columns = []
        for col in range(table.Columns):
            if print_rows > 0:
                columns.append(table.GetText(row, col))
            minRow, maxRow, minCol, maxCol, is_merged = table.IsMergedCell(row, col)
            if is_merged:
                merged.add((minRow, maxRow, minCol, maxCol,))
        if print_rows > 0:
            print_rows -= 1
            row_texts.append(columns)

    print 'row_heights = %s' % str(row_heights)
    print 'column_widths = %s' % str(column_widths)
    print 'merged_cells = %s' % pprint.pformat(list(merged))
    if row_texts:
        print 'content = ['
        for row in row_texts:
            print u"        [%s]," % u", ".join("u'%s'" % s for s in row)
        print ']'


def main():
    acad = Autocad()
    layout = acad.doc.ActiveLayout
    table = acad.find_one('table', layout.Block)
    if not table:
        return
    print_table_info(table, 3)


if __name__ == '__main__':
    with utils.timing():
        main()
