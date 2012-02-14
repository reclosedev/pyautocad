#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs

from pyautocad import Autocad, APoint
from pyautocad.utils import timing


def iter_drawings_names(acad, doc):
    for layout in acad.iter_layouts(doc):
        print ">%s\t%s\t%s" % (layout.TabOrder, layout.Block.Count, layout.Name)
        # first we need to find our main stamp
        block_pos = None
        for block in acad.iter_objects("blockreference", layout.Block):
            if "f4" in block.EffectiveName:
                block_pos = APoint(block.InsertionPoint)
                break
        if not block_pos:
            continue
        # approximate position of drawing name
        name_pos = block_pos + APoint(-90, 12)
        for mt in acad.iter_objects("mtext", layout.Block):
            if name_pos.distance_to(mt.InsertionPoint) < 5.0:
                text = mt.TextString
                print text
                yield text.replace(" \\P", " ").replace("\\P", " ")
                break

def main():
    output = codecs.open("names.txt", "w", encoding='utf-8')
    acad = Autocad()
    for doc in acad.app.Documents:
        print doc.Name
        output.write(u'%s\n' % ('-' * 50))
        output.write(u"    %s\n" % doc.Name)
        output.write(u'%s\n' % ('-' * 50))
        for drawing_name in iter_drawings_names(acad, doc):
            output.write(u'%s\n' % drawing_name)


if __name__ == "__main__":
    with timing():
        main()
