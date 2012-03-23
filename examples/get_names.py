#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys

from pyautocad import Autocad, APoint, utils


def iter_drawings_names(acad, doc):
    num_layouts = doc.Layouts.Count - 2
    for layout_number, layout in enumerate(acad.iter_layouts(doc)):
        utils.dynamic_print('  Layout %02d/%02d' % (layout_number, num_layouts))
        # first we need to find our main stamp with name 'f4'
        block = acad.find_one('blockreference', layout.Block, lambda x: 'f4' in x.EffectiveName)
        if not block:
            continue
        block_pos = APoint(block.InsertionPoint)
        # approximate position of drawing name
        name_pos = block_pos + APoint(-90, 12)
        for mt in acad.iter_objects("mtext", layout.Block):
            if name_pos.distance_to(mt.InsertionPoint) < 5.0:
                text = mt.TextString
                yield text.replace(" \\P", " ").replace("\\P", " ")
                break
    print

def main():
    filename = sys.argv[1] if sys.argv[1:] else 'names.txt'
    output = codecs.open(filename, "w", encoding='utf-8')
    acad = Autocad()
    for doc in acad.app.Documents:
        print doc.Name
        output.write(u'%s\n' % ('-' * 50))
        output.write(u"    %s\n" % doc.Name)
        output.write(u'%s\n' % ('-' * 50))
        for drawing_name in iter_drawings_names(acad, doc):
            output.write(u'%s\n' % drawing_name)


if __name__ == "__main__":
    with utils.timing():
        main()
