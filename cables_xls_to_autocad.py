#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 13.02.12
import time
import re
from collections import defaultdict
from pprint import pprint

import xlrd

from pyautocad import Autocad, ACAD
from pyautocad.point import APoint


HEADER_TEXT_HEIGHT = 3.5
TEXT_HEIGHT = 3.0
ROW_HEIGHT = 8.0
TABLE_WIDTH = 287
FIRST_TABLE_ROWS = 23
NEXT_TABLE_ROWS = 27


acad = Autocad()
def convert_cables_xls_to_autocad(data):
    block = acad.doc.ActiveLayout.Block
    insert_point = APoint(20, 0)
    distance = APoint(TABLE_WIDTH + 5, 0, 0)
    create_and_fill(block, data[:FIRST_TABLE_ROWS], APoint(20, 0))
    for chunk in chunks(data[FIRST_TABLE_ROWS:], NEXT_TABLE_ROWS):
        insert_point += distance
        create_and_fill(block, chunk, insert_point)
    pivot_cabels = pivot_table(data)
    create_pivot_table(block, insert_point + distance, pivot_cabels)
    pivot_dcount = pivot_table(data, count_double_pivot)
    create_pivot_table(block, insert_point + distance * 2, pivot_dcount)
    tips_table = list(pivot_tips(pivot_dcount))
    create_pivot_table(block, insert_point + distance * 3, tips_table)
    
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
        #table.SetRowHeight(row, ROW_HEIGHT)
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

def create_pivot_table(block, pos, pivot):
    table = block.AddTable(pos, len(pivot)+5, len(pivot[0]), ROW_HEIGHT, 20.0)
    table.RegenerateTableSuppressed = True
    table.SetColumnWidth(0, 35)
    table.DeleteRows(0, 2)
    table.SetAlignment(ACAD.acDataRow, ACAD.acMiddleCenter)
    table.VertCellMargin = 0.5
    table.HorzCellMargin = 0.5
    for row, columns in enumerate(pivot):
        for col, data in enumerate(columns):
            table.SetCellTextHeight(row, col, TEXT_HEIGHT)
            if data:
                table.SetText(row, col, unicode(data))
    table.RegenerateTableSuppressed = False
    return table

def length_pivot(value):
    return value

def count_pivot(value):
    return 1 if value else 0
    
def count_double_pivot(value):
    return count_pivot(value) * 2
    
def try_float(val):
    try:
        return float(val)
    except ValueError:
        return 0.0
        
def normalize_section(section):
    section = section.replace(u'х', u'x')  # replace russian h letter
    section = section.replace(',', '.')
    return section
        
def pivot_table(data, value_extractor=length_pivot):
    first_key = 4
    second_key = 3
    value_key = 5
    pivot = defaultdict(lambda : defaultdict(int))
    cable_types = set()
    
    def try_int(val):
        try:
            return int(val)
        except ValueError:
            return 0
            
    for columns in data:
        pivot[columns[first_key]][columns[second_key]] += value_extractor(try_int(columns[value_key]))
        cable_types.add(columns[second_key])
    cable_sections = sorted(pivot.keys())
    cable_types = sorted(cable_types)

    
    def sections_key(section):
        if '(' in section:  # it's hard to handle multicable feeders
            return section  # so return untouched (will be on top)
        section = normalize_section(section)
        return map(try_float, section.split('x'))
        
    cable_sections = sorted(cable_sections, key=sections_key, reverse=True)

    result = [[u'Cечение'] + list(cable_types)]
    for cable_section in cable_sections:
        columns = [cable_section]
        for cable_type in cable_types:
            columns.append(pivot[cable_section][cable_type])
        result.append(columns)
    return result

def pivot_tips(pivot_dcount):
    tip_counts = []
    for row in pivot_dcount[1:]:
        tip_counts.append((row[0], sum(row[1:])))
    
    result = defaultdict(int)
    for section, count in tip_counts:
        if '(' in section:
            result[section] += count
            continue
        section = normalize_section(section)
        col, sect = map(try_float, section.split('x'))  # TODO buggy
        result[sect] += int(count * col)
    
    yield u'Сечение', u'Кол-во наконечников'
    for sect in sorted(result.keys()):
        yield sect, result[sect]
    

def main():
    #data = list(read_cables_from_xls('test.xls')) # 
    data = list(read_cables_from_xls('cables_kommash.xls'))
    convert_cables_xls_to_autocad(data)
    #pivot_dcount = pivot_table(data, count_double_pivot)
    #tips_table = list(pivot_tips(pivot_dcount))
       

if __name__ == "__main__":
    begin_time = time.time()
    main()
    print "Elapsed: %.4f" % (time.time() - begin_time)

