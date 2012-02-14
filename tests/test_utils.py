#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
import unittest

from pyautocad.utils import unformat_mtext, mtext_to_string, string_to_mtext

class UtilsTestCase(unittest.TestCase):
    def test_unformat(self):
        texts = [ur'{\fGOST type A|b0|i0|c204|p34;ЩО\fGOST type A|b0|i0|c0|p34;2-8}',
             ur'text\Pwith {\fWide Latin|b0|i0|c0|p18;multi} {\fVerdana|b0|i0|c0|p34;format}',
             ur'test\P\pxi-3,l3,t3;1.	list1\P2.	list2\P\pi0,l0,tz;\P\pi-3,l3,t3;{\fSymbol|b0|i0|c2|p18;·	}bullet1\P{\fSymbol|b0|i0|c2|p18;·	}bullet2\P\pi0,l0,tz;\P{\fVani|b0|i0|c0|p34;another font} {\fVerdana|b1|i0|c0|p34;and bold}',
             ]
        desired1 = [u'ЩО2-8', u'text\Pwith multi format', u'test\P1.	list1\P2.	list2\P\P·	bullet1\P·	bullet2\P\Panother font and bold']
        desired2 = [u'ЩО2-8', u'text\nwith multi format',
                    u"""test
1.	list1
2.	list2

·	bullet1
·	bullet2

another font and bold"""]
        result1 = map(unformat_mtext, texts)
        result2 = map(mtext_to_string, texts)

        self.assertEqual(result1, desired1)
        self.assertEqual(result2, desired2)

    def test_format(self):
        text = u'Line1\nLine2\nLine3\n\n\nBackslash\\ and \\P'
        desired = u'Line1\PLine2\PLine3\P\P\PBackslash\\\\ and \\\\P'

        self.assertEqual(string_to_mtext(text), desired)


if __name__ == '__main__':
    unittest.main()
