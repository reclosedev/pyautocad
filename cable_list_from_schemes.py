#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict, namedtuple
import optparse
import os
import re
import logging


from pyautocad import Autocad
from pyautocad.utils import unformat_mtext, timing
from pyautocad.contrib.tables import Table, available_write_formats


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('cables_from_schemes.log', 'w'))


CableEntry = namedtuple('CableEntry', 'name, source, target, cable, section, length')


def get_known_targets(filename):
    if not os.path.exists(filename):
        logger.warning("Can't find file with known targets: %s", filename)
        return {}
    targets = OrderedDict()
    data = Table.data_from_file(filename)
    for row in data:
        if len(row) < 3:
            continue
        targets[row[0]] = row[2]
    return targets


def get_cables(acad, block, known_targets):
    patterns = [ur"""(?P<cable>.*?)-(?P<section>[\dxх,\(\)]+)\s+
                     (?P<length>\d+)\s*[мm]\\P
                     \s*(?P<name>[^-]+)-(?P<source>.+)\s*""",

                ur"""(?P<name>.*?)-(?P<source>.*?)\s*\\P
                      \s*(?P<cable>.*?)-(?P<section>[\dxх,\(\)]+)\s+
                      (?P<length>\d+)\s*[мm]"""]
    patterns = [re.compile(pat, re.VERBOSE) for pat in patterns]

    for text in acad.iter_objects("dbmtext", block):
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
        yield CableEntry(cable_name, m['source'], target,
                         m['cable'], m['section'], m['length'])


def sort_by_correct_order(messed_order, correct_order):
    return [x for x in correct_order if x in messed_order] +\
           [x for x in messed_order if x not in correct_order]


def sort_cables_by_targets(cables, targets):
    presorted_cables = OrderedDict()
    for entry in sorted(cables, key=lambda x: (x.source, x.name)):
       presorted_cables[entry.name] = entry
    if not targets:
        return presorted_cables.itervalues()
    sorted_cable_names = sort_by_correct_order(presorted_cables, targets)
    return (presorted_cables[name] for name in sorted_cable_names)


def main():
    acad = Autocad()
    parser = optparse.OptionParser(usage=u'%prog [опции] [файл для результатов]')
    parser.add_option('-f', '--format',
                      choices=available_write_formats(), dest='format',
                      metavar='FORMAT', default='xls',
                      help=u"Формат файла (%s) по умолчанию - %%default" %
                           ', '.join(available_write_formats()))
    parser.add_option('-k', '--known', dest='known_targets',
                      metavar='FILE', default='', action='store',
                      help=u'Файл с заполненым полем "Конец" и очередностью '
                           u' записей. По умолчанию берется из существующего файла')
    parser.add_option('-q', '--quiet', action='callback',
                      callback=lambda *x: logging.disable(logging.WARNING),
                      help=u'"Тихий" режим (не печатать в консоль)')
    parser.add_option('-s', '--single', dest='single_doc', action='store_true',
                      default=False,
                      help=u'Собрать данные только из текущего документа '
                           u'(Собирает из всех по умолчанию)')
    parser.add_option('-c', '--no-known', dest='dont_use_known',
                      action='store_true', default=False,
                      help=u'Не использовать данные об очередности и поле "Конец"')
    options, args = parser.parse_args()

    output_file = args[0] if args else u"cables_from_%s.%s" % (acad.doc.Name, options.format)
    if not options.known_targets and not options.dont_use_known:
        options.known_targets = output_file
    known_targets = get_known_targets(options.known_targets)
    output_table = Table()
    if options.single_doc:
        documents = [acad.doc]
    else:
        documents = acad.app.Documents

    for doc in documents:
        try:
            cables = get_cables(acad, doc.Modelspace, known_targets)
            sorted_cables = sort_cables_by_targets(cables, known_targets)
            for row in sorted_cables:
                output_table.writerow([s for s in row])
        except Exception:
            logger.exception('Error while processing %s', doc.Name)
    output_table.save(output_file, options.format)


if __name__ == "__main__":
    with timing():
        main()

# TODO append to existent file option
# TODO atomic write
