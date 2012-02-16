#!/usr/bin/env python
# -*- coding: utf-8 -*-
import optparse
import os
import sys
import re
import csv
import logging

from pyautocad import Autocad
from pyautocad.utils import unformat_mtext, timing
from pyautocad.contrib.excel import get_writer, available_formats


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('cables_from_schemes.log', 'w'))


def get_known_targets(filename):
    if not os.path.exists(filename):
        logger.warning("Can't find file with known targets: %s", filename)
        return {}
    targets = {}
    reader = csv.reader(open(filename, "r"), delimiter=';')
    for row in reader:
        if len(row) < 3:
            continue
        row = [x.decode('cp1251') for x in row]
        targets[row[0]] = row[2]
    return targets


def get_cables(acad, known_targets):
    patterns = [ur"""(?P<cable>.*?)-(?P<section>[\dxх,\(\)]+)\s+
                     (?P<length>\d+)\s*[мm]\\P
                     \s*(?P<name>[^-]+)-(?P<source>.+)\s*""",

                ur"""(?P<name>.*?)-(?P<source>.*?)\s*\\P
                      \s*(?P<cable>.*?)-(?P<section>[\dxх,\(\)]+)\s+
                      (?P<length>\d+)\s*[мm]"""]
    patterns = [re.compile(pat, re.VERBOSE) for pat in patterns]

    for text in acad.iter_objects("dbmtext"):
        text = unformat_mtext(text.TextString)
        logger.info(text)
        m_cable = None
        for pattern in patterns:
            m_cable = pattern.match(text)
            if m_cable:
                break
        if not m_cable:
            continue

        logger.info("!!!%s\n", text)
        m = m_cable.groupdict()
        cable_name = "%s-%s" % (m['name'], m['source'])
        target = known_targets.get(cable_name, '')
        if not target:
            target = m['name']
        yield (cable_name, m['source'], target,
               m['cable'], m['section'], m['length'])


def main():
    acad = Autocad()
    parser = optparse.OptionParser(usage=u'%prog [опции] [файл]')
    parser.add_option('-f', '--format',
                      choices=available_formats(), dest='format',
                      metavar='FORMAT', default='xls',
                      help=u"Формат файла (%s) по умолчанию - %%default" %
                           ', '.join(available_formats()))
    parser.add_option('-k', '--known',
                      dest='known_targets', metavar='FILE',
                      default="cables_known.csv",action='store',
                      help=u'Файл с заполненым полем "Конец"')
    parser.add_option('-q', '--quiet', action='callback',
                      callback=lambda *x: logging.disable(logging.WARNING),
                      help=u'"Тихий" режим')

    options, args = parser.parse_args()
    output_file = args[0] if args else u"cables_from_%s.%s" % (acad.doc.Name, options.format)
    known_targets_file = options.known_targets
    cables = get_cables(acad, get_known_targets(known_targets_file))
    # TODO sort based on known targets
    sorted_cables = sorted(cables, key=lambda x: (x[1], x[0]))

    # TODO save to .xls (option)
    writer = get_writer(options.format)(output_file)
    for row in sorted_cables:
        writer.writerow([s for s in row])
    writer.close()


if __name__ == "__main__":
    with timing():
        main()

# TODO append option