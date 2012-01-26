#/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import re
#import codecs

from pyautocad.api import Autocad
#from pyautocad.utils import distance
#from pyautocad.point import APoint
from pyautocad import utils

acad = Autocad()

# существующие светильники\P2х36
# \A1;2ARCTIC SMC/SAN 254 \S2х54/2,5;\P300 лк
def main():
    #objects = acad.get_selection('Select objects')
    objects = None
    for obj in acad.iter_objects(('MText', 'MLeader'), container=objects):
        try:        
            text = obj.TextString
        except Exception:
            continue
        
        text = utils.unformat_text(obj.TextString)
        m = re.search(ur'(?P<num>\d+)(?P<mark>.*?)\\S(?P<num_power>.*?)/.*?;', text)
        if not m:
            continue
        
        print m.group('num'), m.group('mark'), m.group('num_power')

begin_time = time.time()
main()
print "Elapsed: %.4f" % (time.time() - begin_time)