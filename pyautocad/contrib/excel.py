#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 15.02.12
import csv
from cStringIO import StringIO


import xlwt


class CsvWriter(object):

    def __init__(self, filename, encoding='cp1251', delimiter=';', **kwargs):
        self.encoding = encoding
        self.filename = filename
        self._stream = StringIO()
        self._real_writer = csv.writer(self._stream, delimiter=delimiter, **kwargs)

    def writerow(self, row):
        self._real_writer.writerow([col.encode(self.encoding) for col in row])

    def close(self):
        with open(self.filename, 'wb') as output:
            output.write(self._stream.getvalue())
        self._stream.close()


class XlsWriter(object):

    def __init__(self, filename):
        self.filename = filename
        self._workbook = xlwt.Workbook()
        self._sheet = self._workbook.add_sheet('Sheet1')
        self._current_row = 0

    def writerow(self, row):
        for col, data in enumerate(row):
            self._sheet.write(self._current_row, col, data)
        self._current_row += 1

    def close(self):
        with open(self.filename, 'wb') as output:
            self._workbook.save(output)


_writers = {'csv': CsvWriter, 'xls': XlsWriter}


def get_writer(format='csv', default=None):
    return _writers.get(format, default)


def available_formats():
    return _writers.keys()

# TODO better interface
# TODO xls reader
