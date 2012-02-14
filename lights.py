#/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import re
#import codecs
import sys

from pyautocad import Autocad
from pyautocad import utils


# \A1;2ARCTIC SMC/SAN 254 \S2х54/2,5;\P300 лк
def main():
    acad = Autocad()
    objects = None
    if 'i' in sys.argv[1:]:
        objects = acad.get_selection('Select objects')

    for obj in acad.iter_objects(('MText', 'MLeader'), container=objects):
        try:        
            text = obj.TextString
        except Exception:
            continue
        text = utils.unformat_mtext(text)
        m = re.search(ur'(?P<num>\d+)(?P<mark>.*?)\\S(?P<num_power>.*?)/.*?;', text)
        if not m:
            continue
        
        print m.group('num'), m.group('mark'), m.group('num_power')

begin_time = time.time()
main()
print "Elapsed: %.4f" % (time.time() - begin_time)