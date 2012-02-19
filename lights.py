#/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import sys
from collections import namedtuple, defaultdict

from pyautocad import Autocad
from pyautocad import utils


LampEntry = namedtuple('LampEntry', 'number, mark, numxpower')

# \A1;2ARCTIC SMC/SAN 254 \S2х54/2,5;\P300 лк
def iter_lamps(acad, objects):
    for obj in acad.iter_objects(('MText', 'MLeader'), block=objects):
        try:
            text = obj.TextString
        except Exception:
            continue
        text = utils.unformat_mtext(text)
        m = re.search(ur'(?P<num>\d+)(?P<mark>.*?)\\S(?P<num_power>.*?)/.*?;', text)
        if not m:
            continue
        print m.group('num'), m.group('mark'), m.group('num_power')
        yield LampEntry(m.group('num'), m.group('mark'), m.group('num_power'))

def main():
    acad = Autocad()
    objects = None
    if 'i' in sys.argv[1:]:
        objects = acad.get_selection('Select objects')
    lamps = defaultdict(int)
    for lamp in iter_lamps(acad, objects):
        lamps[lamp.mark] += int(lamp.number)
    print '-' * 79
    for mark, number in sorted(lamps.iteritems()):
        print '%-20s | %s' % (mark, number)

if __name__ == "__main__":
    with utils.timing():
        main()
