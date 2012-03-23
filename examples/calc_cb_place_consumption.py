#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from pyautocad import Autocad
from pyautocad.utils import mtext_to_string, timing


def main():
    acad = Autocad()
    print u'Примерный подсчет занимаемого места'
    print '%-20s| %s' % (u'Имя щита', u'Общее число модулей')
    for layout in acad.iter_layouts():
        table = acad.find_one('table', layout.Block, lambda x: x.Columns == 5)
        if not table:
            continue

        total_modules = 0
        row = -1
        while row < table.Rows:
            row += 1
            item_str = mtext_to_string(table.GetText(row, 2))
            item_str = item_str.replace(u'четырехполюсный', u'4-х')\
                               .replace(u'трехполюсный', u'3-х')\
                               .replace(u'двухполюсный', u'2-х')\
                               .replace(u'однополюсный', u'1-но')
            m = re.match(ur'.*(\d)-([xх]|но).*', item_str)
            if m:
                n_modules = int(m.group(1))
                quantity = int(mtext_to_string(table.GetText(row, 3)))
                row += 1  # skip next row
            else:
                m = re.match(ur'(\d)[PР].*', item_str)
                if not m:
                    continue
                n_modules = int(m.group(1))
                quantity = int(mtext_to_string(table.GetText(row - 1, 3)))
            total_modules += n_modules * quantity
        print '%-20s| %s' % (layout.Name, total_modules)


if __name__ == "__main__":
    with timing():
        main()
    raw_input(u'\nPress enter to exit...')
