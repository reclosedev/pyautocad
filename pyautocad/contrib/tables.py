#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 15.02.12
import csv
from cStringIO import StringIO

import tablib

class FormatNotSupported(Exception):
    pass

class Table(object):
    _write_formats = set(['csv', 'xls', 'xlsx', 'yaml', 'json'])
    _read_formats = _write_formats

    def __init__(self, ):
        self.dataset = tablib.Dataset()

    def writerow(self, row):
        self.dataset.append(row)

    def append(self, row):
        self.writerow(row)

    def clear(self):
        self.dataset = tablib.Dataset()

    def save(self, filename, format, encoding=None):
        with open(filename, 'wb') as output:
            converted = self.convert(format)
            if format == 'csv' and encoding:
                converted = converted.decode('utf8').encode(encoding)
            output.write(converted)

    def convert(self, format):
        if format not in self._write_formats:
            raise FormatNotSupported('Unknown format: %s' % format)
        return getattr(self.dataset, format)

    @staticmethod
    def available_formats():
        return Table._write_formats



available_formats = Table.available_formats  # backward compatibility

# TODO better interface
# TODO xls reader
# TODO use tablib
