#!python
#-*- coding: utf-8 -*-
import time
import re
import codecs

from pyautocad import Autocad
from pyautocad.utils import distance
from pyautocad.point import APoint


file = codecs.open("names.txt", "w", encoding='utf-8')
acad = Autocad()

def test_layouts():
    for doc in acad.app.Documents:
        print doc.Name
        file.write(u"\n%s----------------->\n\n" % doc.Name)
        get_drawings_names(doc)

def get_drawings_names(doc):
    for layout in sorted(doc.Layouts, key=lambda x: x.TabOrder):
        if not layout.TabOrder:
            continue  # skip Model space
            
        print ">%s\t%s\t%s" % (layout.TabOrder, layout.Block.Count, layout.Name)
                       
        # first we need to find our main stamp
        block_pos = None
        for block in acad.iter_objects("blockreference", layout.Block):
            if block and "f4" in block.EffectiveName:
                block_pos = APoint(block.InsertionPoint)
                break
        
        if not block_pos:
            continue
        # aproximate position of drawing name        
        name_pos = block_pos + APoint(-90, 12)
        for mt in acad.iter_objects("mtext", layout.Block):
            if name_pos.distance_to(mt.InsertionPoint) < 5.0:
                text = mt.TextString
                print text
                file.write(u"%s\n" % text.replace(" \\P", " ").replace("\\P", " "))
     
begin_time = time.time()
test_layouts()
print "Elapsed: %.4f" % (time.time() - begin_time)