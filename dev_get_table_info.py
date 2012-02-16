#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 13.02.12
import sys
import pprint

from pyautocad import Autocad, utils


def main():
    acad = Autocad()
    layout = acad.doc.ActiveLayout
    table = acad.find_one('table', layout.Block)
    if not table:
        return
        
    merged = set()
    column_widths = [0] * table.Columns
    row_heights = [0] * table.Rows
    widths_gathered = False
    
    for row in range(table.Rows):
        row_heights[row] = round(table.GetRowHeight(row), 2)
        for col in range(table.Columns):
            if not widths_gathered:
                column_widths[col] = round(table.GetColumnWidth(col), 2)
            minRow, maxRow, minCol, maxCol, is_merged = table.IsMergedCell(row, col)
            if is_merged:
                merged.add((minRow, maxRow, minCol, maxCol,))
        widths_gathered = True
    
    print 'row_heights = %s' % str(row_heights)
    print 'column_widths = %s' % str(column_widths)
    print 'merged_cells = %s' % pprint.pformat(list(merged))

if __name__ == '__main__':
    with utils.timing():
        main()
