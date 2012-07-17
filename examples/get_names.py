#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys

from pyautocad import Autocad, APoint, utils


acad = Autocad()


def iter_drawings_names(doc):
    num_layouts = doc.Layouts.Count - 2
    layouts = doc.Layouts.filter(TabOrder__ne=0).order_by('TabOrder')
    for layout_number, layout in enumerate(layouts):
        utils.dynamic_print('  Layout %02d/%02d' % (layout_number, num_layouts))
        # first we need to find our main stamp with name 'f4'
        block = layout.Block.filter(ObjectName='AcDbBlockReference',
                                    EffectiveName='f4').first()
        if not block:
            continue
        block_pos = APoint(block.InsertionPoint)
        # approximate position of drawing name
        name_pos = block_pos + APoint(-90, 12)
        mt = layout.Block.filter(ObjectName="AcDbMText",
                                 InsertionPoint__dist_lt=(name_pos, 5.0)).first()
        if mt is not None:
            text = mt.TextString
            yield text.replace(" \\P", " ").replace("\\P", " ")
    print

def main():
    filename = sys.argv[1] if sys.argv[1:] else 'names.txt'
    output = codecs.open(filename, "w", encoding='utf-8')

    for doc in acad.app.Documents:
        print doc.Name
        output.write(u'%s\n' % ('-' * 50))
        output.write(u"    %s\n" % doc.Name)
        output.write(u'%s\n' % ('-' * 50))
        for drawing_name in iter_drawings_names(doc):
            output.write(u'%s\n' % drawing_name)


if __name__ == "__main__":
    with utils.timing():
        main()
