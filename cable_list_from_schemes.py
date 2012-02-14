#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import csv
import logging

from pyautocad import Autocad
from pyautocad.utils import unformat_mtext, timing


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
    patterns = [re.compile(ur"(?P<cable>.*?)-(?P<section>[\dxх,\(\)]+)\s+(?P<length>\d+)\s*[мm]\\P\s*(?P<name>[^-]+)-(?P<source>.+)\s*"),
                re.compile(ur"(?P<name>.*?)-(?P<source>.*?)\s*\\P\s*(?P<cable>.*?)-(?P<section>[\dxх,\(\)]+)\s+(?P<length>\d+)\s*[мm]")]

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
        yield (cable_name, m['source'], target, m['cable'], m['section'], m['length'])

def main():
    acad = Autocad()
    known_targets_file = "cables_known.csv"
    output_file = "cables_from_scheme.csv"
    if len(sys.argv) > 1:  # TODO optparse
        output_file = sys.argv[1]
    elif len(sys.argv) == 3:
        known_targets_file = sys.argv[2]
    cables = get_cables(acad, get_known_targets(known_targets_file))
    sorted_cables = sorted(cables, key=lambda x: (x[1], x[0])) # TODO sort based on known targets

    # TODO save to .xls (option)
    writer = csv.writer(open(output_file, "wb"), delimiter=';')
    for row in sorted_cables:
        writer.writerow([s.encode("cp1251") for s in row])
            
if __name__ == "__main__":
    with timing():
        main()