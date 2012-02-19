#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 15.02.12
import csv
from cStringIO import StringIO

import tablib


class Table(object):

    def __init__(self, ):
        self._dataset = tablib.Dataset()

    def writerow(self, row):
        self._dataset.append(row)

    def save(self, filename, format, encoding=None):
        with open(filename, 'wb') as output:
            output.write(getattr(self._dataset, format))

_write_formats = set(['csv', 'xls', 'xlsx'])
_read_formats = _write_formats

def available_formats():
    return _write_formats

# TODO better interface
# TODO xls reader
# TODO use tablib
