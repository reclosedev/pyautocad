#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 13.02.12
import sys
from collections import defaultdict

import xlrd

from pyautocad import Autocad, ACAD, APoint
from pyautocad.utils import timing
from pyautocad.contrib.tables import Table


HEADER_TEXT_HEIGHT = 3.5
TEXT_HEIGHT = 3.0
ROW_HEIGHT = 8.0
TABLE_WIDTH = 287
TABLE_GAP = 100
FIRST_TABLE_ROWS = 23
NEXT_TABLE_ROWS = 27


def add_cables_list_to_autocad(block, data):
    insert_point = APoint(20, 0)
    distance = APoint(TABLE_WIDTH + TABLE_GAP, 0, 0)

    add_cables_table(block, data[:FIRST_TABLE_ROWS], APoint(20, 0))
    for chunk in chunks(data[FIRST_TABLE_ROWS:], NEXT_TABLE_ROWS):
        insert_point += distance
        add_cables_table(block, chunk, insert_point)

    # TODO names of pivot tables
    margin = APoint(0, TEXT_HEIGHT, 0)
    insert_point += distance
    block.AddText(u'Сводная таблица длин кабелей', insert_point + margin, TEXT_HEIGHT)
    add_pivot_table(block, insert_point, list(calc_pivot_table(data)))

    insert_point += distance
    block.AddText(u'Сводная таблица кабельных разделок', insert_point + margin, TEXT_HEIGHT)
    pivot_dcount = list(calc_pivot_table(data, count_double_pivot))
    add_pivot_table(block, insert_point, pivot_dcount)

    insert_point += distance
    block.AddText(u'ВНИМАНИЕ! У кабелей со сложным сечением (например 4х(5х70)'
                  u' и т.п.) указано количество разделок',
                  insert_point + margin * 4, TEXT_HEIGHT)
    block.AddText(u'Сводная таблица наконечников', insert_point + margin, TEXT_HEIGHT)
    add_pivot_table(block, insert_point, list(calc_pivot_tips(pivot_dcount)))


def read_cables_from_table(filename):
    data = Table.data_from_file(filename)
    for row in data:
        columns = []
        for col in row:
            try:
                col = unicode(int(float(col))) # TODO HACK manipulate table format
            except ValueError:
                pass
            columns.append(col)
        yield columns


def add_cables_table(block, entries, pos):
    table = prepare_cables_table(block, pos, len(entries))
    table.RegenerateTableSuppressed = True  # speedup edit operations
    try:
        for row, row_data in enumerate(entries, 3):
            for col, text in enumerate(row_data):
                table.SetCellTextHeight(row, col, TEXT_HEIGHT)
                if text:
                    table.SetText(row, col, text)
    finally:
        table.RegenerateTableSuppressed = False


def prepare_cables_table(block, pos, rows):
    table = block.AddTable(pos, rows + 5, 9, ROW_HEIGHT, 15.0)
    table.RegenerateTableSuppressed = True
    table.DeleteRows(0, 2)
    table.SetAlignment(ACAD.acDataRow, ACAD.acMiddleCenter)
    table.VertCellMargin = 0.5
    table.HorzCellMargin = 0.5

    content = ((u"Обозначение кабеля, провода", u"Трасса", "", u"Кабель, провод", "", "", "", "",),
               ("", u"Начало", u"Конец", u"По проекту", "", "", u"Проложен", "", ),
               ("", "", "", u"Марка", u"Кол., число и сечение жил", u"Длина, м", u"Марка", u"Кол., число и сечение жил", u"Длина, м"))

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
        yield thing[i:i + chunk_length]


def add_pivot_table(block, pos, pivot):
    table = block.AddTable(pos, len(pivot) + 5, len(pivot[0]), ROW_HEIGHT, 20.0)
    table.RegenerateTableSuppressed = True
    table.SetColumnWidth(0, 35)
    table.DeleteRows(0, 2)  # delete Header and Title. SuppressHeader and SuppressTitle is not working.
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


def try_convert(val, val_type):
    try:
        return val_type(val)
    except ValueError:
        return val_type()


def normalize_section(section):
    section = section.replace(u'х', u'x')  # replace russian h letter
    section = section.replace(',', '.')
    return section


def calc_pivot_table(data, value_extractor=length_pivot):
    first_key = 4
    second_key = 3
    value_key = 5
    pivot = defaultdict(lambda: defaultdict(int))
    cable_types = set()

    for columns in data:
        pivot[columns[first_key]][columns[second_key]] += value_extractor(try_convert(columns[value_key], int))
        cable_types.add(columns[second_key])
    cable_sections = sorted(pivot.keys())

    def sections_key(section):
        if '(' in section:  # it's hard to handle multicable feeders
            return section  # so return untouched (will be on top)
        section = normalize_section(section)
        return map(lambda x: try_convert(x, float), section.split('x'))
    cable_sections = sorted(cable_sections, key=sections_key)

    yield [u'Cечение'] + list(sorted(cable_types))
    for cable_section in cable_sections:
        columns = [cable_section]
        for cable_type in cable_types:
            columns.append(pivot[cable_section][cable_type])
        yield columns


def calc_pivot_tips(pivot_dcount):
    tip_counts = []
    for row in pivot_dcount[1:]:
        tip_counts.append((row[0], sum(row[1:])))
    result = defaultdict(int)
    for section, count in tip_counts:
        if '(' in section:
            result[section] += count
            continue
        section = normalize_section(section)
        count_sect = map(lambda x: try_convert(x, float), section.split('x', 2))  # TODO buggy
        if len(count_sect) == 2:
            result[count_sect[1]] += int(count_sect[0] * count)

    yield u'Сечение', u'Кол-во наконечников'
    for sect in sorted(result.keys()):
        yield sect, result[sect]


def main():
    filename = sys.argv[1] if sys.argv[1:] else 'cables_list.xls'
    acad = Autocad()
    data = list(read_cables_from_table(filename))
    add_cables_list_to_autocad(acad.doc.ActiveLayout.Block, data)


if __name__ == "__main__":
    with timing():
        main()
