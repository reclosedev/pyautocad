#!/usr/bin/env python
#-*- coding: utf-8 -*-
import optparse

from pyautocad import Autocad, utils
from pyautocad.contrib.tables import Table, available_write_formats


def iter_cable_tables(acad, block):
    for table in acad.iter_objects("table", block):
        if table.Columns != 9:
            continue
        ncols = table.Columns  # store in local, Automation is expensive
        for row in xrange(3, table.Rows):
            yield [utils.mtext_to_string(table.GetText(row, col))
                   for col in xrange(ncols)]


def extract_tables_from_dwg(acad, writer, skip_model=True):
    for layout in acad.iter_layouts(skip_model=skip_model):
        for row in iter_cable_tables(acad, layout.Block):
            writer.writerow(row)


def main():
    parser = optparse.OptionParser()
    parser.add_option('-f', '--format',
                      choices=available_write_formats(), dest='format',
                      metavar='FMT', default='xls',
                      help=u"Формат файла (%s) по умолчанию - %%default" %
                           ', '.join(available_write_formats()))
    parser.add_option('-m', '--model',
                      dest='include_model', default=False, action='store_true',
                      help=u"Включить пространство Модели в область поиска")

    options, args = parser.parse_args()
    acad = Autocad()
    filename = args[0] if args else u"exported_%s.%s" % (acad.doc.Name,
                                                         options.format)
    output_table = Table()
    extract_tables_from_dwg(acad, output_table, not options.include_model)
    output_table.save(filename, options.format)

if __name__ == '__main__':
    with utils.timing():
        main()
