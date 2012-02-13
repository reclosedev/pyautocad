#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 13.02.12
import time
import re
import xlrd

from pyautocad import Autocad, ACAD
from pyautocad.point import APoint


HEADER_TEXT_HEIGHT = 3.5
TEXT_HEIGHT = 3.0
ROW_HEIGHT = 8.0
TABLE_WIDTH = 287
FIRST_TABLE_ROWS = 22
NEXT_TABLE_ROWS = 25


acad = Autocad()
def convert_cables_xls_to_autocad(filename):
    data = list(read_cables_from_xls(filename))
    block = acad.iter_layouts().next().Block
    insert_point = APoint(20, 0)
    create_and_fill(block, data[:FIRST_TABLE_ROWS], APoint(20, 0))
    for chunk in chunks(data[FIRST_TABLE_ROWS:], NEXT_TABLE_ROWS):
        insert_point.x += TABLE_WIDTH + 5
        create_and_fill(block, chunk, insert_point)

def read_cables_from_xls(filename):
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)
    for row in xrange(sheet.nrows):
        columns = []
        for col in xrange(min(9, sheet.ncols)):
            text = val = sheet.cell(row, col).value
            try:
                text = unicode(int(val))
            except ValueError:
                text = unicode(val)
            columns.append(text)
        yield columns

def create_and_fill(block, entries, pos):
    table = create_cables_table(block, pos, len(entries))
    table.RegenerateTableSuppressed = True  # speedup edit operations
    try:
        for row, row_data in enumerate(entries, 3):
            for col, text in enumerate(row_data):
                table.SetCellTextHeight(row, col, TEXT_HEIGHT)
                if text:
                    table.SetText(row, col, text)
    finally:
        table.RegenerateTableSuppressed = False

def create_cables_table(block, pos, rows):
    table = block.AddTable(pos, rows+5, 9, ROW_HEIGHT, 15.0)
    table.RegenerateTableSuppressed = True
    table.DeleteRows(0, 2)
    table.SetAlignment(ACAD.acDataRow, ACAD.acMiddleCenter)
    table.VertCellMargin = 0.5
    table.HorzCellMargin = 0.5

    content = ((u"Обозначение кабеля, провода",u"Трасса","",u"Кабель, провод","","","","",),
               ("",u"Начало",u"Конец",u"По проекту","","",u"Проложен","", ),
               ("","","",u"Марка",u"Кол., число и сечение жил",u"Длина, м",u"Марка",u"Кол., число и сечение жил",u"Длина, м"))

    merged = ((1, 1, 6, 8), (0, 2, 0, 0), (1, 2, 1, 1), (0, 0, 3, 8),
              (0, 0, 0, 0), (1, 2, 2, 2), (1, 1, 3, 5), (0, 0, 1, 2))

    col_widths = [25, 60, 60, 20, 35, 16, 20, 35, 16]

    for col, width in enumerate(col_widths):
        table.SetColumnWidth(col, width)
    table.SetRowHeight(2, 20)

    # Merge cells before inserting text
    for merge in merged:
        table.MergeCells(*merge)
    for row, lst in enumerate(content):
        for col, text in enumerate(lst):
            table.SetCellTextHeight(row, col, HEADER_TEXT_HEIGHT)
            if text:
                table.SetText(row, col, text)
    table.RegenerateTableSuppressed = False
    return table

def chunks(thing, chunk_length):
    for i in xrange(0, len(thing), chunk_length):
        yield thing[i:i+chunk_length]

def main():
    convert_cables_xls_to_autocad('cables2.xls')

if __name__ == "__main__":
    begin_time = time.time()
    main()
    print "Elapsed: %.4f" % (time.time() - begin_time)

