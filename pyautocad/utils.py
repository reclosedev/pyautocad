#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
import sys
import re
import time
from contextlib import contextmanager


def unformat_mtext(s, exclude_list=('P', 'S')):
    """Remove format information from string

    `s` - string with multitext
    `exclude_list` - don't touch tagse from this list. Default ('P', 'S') for
    newline and fractions
    """
    s = re.sub(r'\{?\\[^%s][^;]+;' % ''.join(exclude_list), '', s)
    s = re.sub(r'\}', '', s)
    return s


def mtext_to_string(s):
    """Remove all format from string, replace P (paragraphs) with newlines
    """
    return unformat_mtext(s).replace(u'\\P', u'\n')


def string_to_mtext(s):
    """Format string in Autocad multitext format
    """
    return s.replace('\\', '\\\\').replace(u'\n', u'\P')


def text_width(text_item):
    """Calculate width of Autocad `Text` or `MultiText`
    """
    bbox_min, bbox_max = text_item.GetBoundingbox()
    return bbox_max[0] - bbox_min[0]


@contextmanager
def timing(message=u'Elapsed'):
    begin = time.time()
    try:
        yield begin
    finally:
        elapsed = (time.time() - begin)
        print u'%s: %.3f s' % (message, elapsed)


def dynamic_print(text):
    """Prints text dynamically in one line
    """
    sys.stdout.write('\r%s' % text)
    sys.stdout.flush()
