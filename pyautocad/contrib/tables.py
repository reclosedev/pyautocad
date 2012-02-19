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

    def save(self, filename, format, encoding='cp1251'):
        with open(filename, 'wb') as output:
            if encoding is not None and format == 'csv':
                self.to_csv(output, encoding)
            else:
                output.write(self.convert(format))

    def convert(self, format):
        if format not in self._write_formats:
            raise FormatNotSupported('Unknown format: %s' % format)
        return getattr(self.dataset, format)

    def to_csv(self, stream, encoding='cp1251', delimiter=';', **kwargs):
        writer = csv.writer(stream, delimiter=delimiter, **kwargs)
        for row in self.dataset.dict:
            row = [c.encode(encoding) for c in row]
            writer.writerow(row)

    @staticmethod
    def available_formats():
        return list(Table._write_formats)



available_formats = Table.available_formats  # backward compatibility

# TODO better interface
# TODO xls reader
# TODO use tablib
