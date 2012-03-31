#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    pyautocad.contrib.tables
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Import and export tabular data from popular formats.

    :copyright: (c) 2012 by Roman Haritonov.
    :license: BSD, see LICENSE.txt for more details.
"""

import csv
import json
import os

import tablib
import xlrd

class FormatNotSupported(Exception):
    pass

class Table(object):
    """ Represents table with ability to import and export data to following formats:

    - csv
    - xls
    - xlsx (write only)
    - json

    When you need to store some data, it can be done as follows::

        table = Table()
        for i in range(5):
            table.writerow([i, i, i])

        table.save('data.xls', 'xls')

    To import data from file, use :meth:`data_from_file`::

        data = Table.data_from_file('data.xls')

    """

    _write_formats = set(['csv', 'xls', 'xlsx', 'json'])
    _read_formats = _write_formats - set(['xlsx'])

    def __init__(self):
        self.dataset = tablib.Dataset()

    def writerow(self, row):
        """ Add `row` to table

        :param row: row to add
        :type row: list or tuple
        """
        self.dataset.append(row)

    def append(self, row):
        """ Synonym for :meth:`writerow`
        """
        self.writerow(row)

    def clear(self):
        """ Clear current table
        """
        self.dataset = tablib.Dataset()

    def save(self, filename, fmt, encoding='cp1251'):
        """ Save data to file

        :param filename: path to file
        :param fmt: data format (one of supported, e.g. 'xls', 'csv'
        :param encoding: encoding for 'csv' format
        """
        self._raise_if_bad_format(fmt)
        with open(filename, 'wb') as output:
            if encoding is not None and fmt == 'csv':
                self.to_csv(output, encoding)
            else:
                output.write(self.convert(fmt))

    def convert(self, fmt):
        """ Return data, converted to format

        :param fmt: desirable format of data

        **Note**: to convert to `csv` format, use :meth:`to_csv`

        See also :meth:`available_write_formats`
        """
        self._raise_if_bad_format(fmt)
        return getattr(self.dataset, fmt)

    def _raise_if_bad_format(self, fmt):
        if fmt not in self._write_formats:
            raise FormatNotSupported('Unknown format: %s' % fmt)

    def to_csv(self, stream, encoding='cp1251', delimiter=';', **kwargs):
        """ Writes data in `csv` format to stream

        :param stream: stream to write data to
        :param encoding: output encoding
        :param delimiter: `csv` delimiter
        :param kwargs: additional parameters for :class:`csv.writer`
        """
        writer = csv.writer(stream, delimiter=delimiter, **kwargs)
        for row in self.dataset.dict:
            row = [c.encode(encoding) for c in row]
            writer.writerow(row)

    @staticmethod
    def data_from_file(filename, fmt=None, csv_encoding='cp1251', csv_delimiter=';'):
        """ Returns data in desired format from file

        :param filename: path to file with data
        :param fmt: format of file, if it's `None`, then it tries to guess format
                    from `filename` extension
        :param csv_encoding: encoding for `csv` data
        :param csv_delimiter: delimiter for `csv` data

        Format should be in :meth:`available_read_formats`
        """
        if fmt is None:
            fmt = os.path.splitext(filename)[1][1:]
        raw_data =  _TableImporter(csv_encoding=csv_encoding,
                                   csv_delimiter=csv_delimiter).import_table(filename, fmt)
        return raw_data

    @staticmethod
    def available_write_formats():

        return list(Table._write_formats)

    @staticmethod
    def available_read_formats():
        return list(Table._read_formats)


class _TableImporter(object):
    def __init__(self, csv_encoding='cp1251', csv_delimiter=';'):
        self.csv_encoding = csv_encoding
        self.csv_delimiter = csv_delimiter

    def import_table(self, filename, fmt):
        reader = getattr(self, 'read_%s' % fmt, None)
        if reader is None:
            raise FormatNotSupported('Unknown fmt: %s' % fmt)
        dataset = []
        with open(filename, 'rb') as stream:
            for row in reader(stream):
                dataset.append(row)
            return dataset

    def read_csv(self, stream):
        reader = csv.reader(stream, delimiter=self.csv_delimiter)
        for row in reader:
            yield [c.decode(self.csv_encoding) for c in row]

    def read_xls(self, stream):
        book = xlrd.open_workbook(file_contents=stream.read())
        sheet = book.sheet_by_index(0)
        for row in xrange(sheet.nrows):
            columns = []
            for col in xrange(sheet.ncols):
                val = sheet.cell(row, col).value
                columns.append(val)
            yield columns

    def read_json(self, stream):
        return json.load(stream)

available_write_formats = Table.available_write_formats  # backward compatibility
available_read_formats = Table.available_read_formats

