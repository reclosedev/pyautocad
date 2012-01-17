#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12

import math
import re


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def unformat_text(s):
    s = re.sub(r'\{?\\[^P][^;]+;', '', s)
    s = re.sub(r'\}', '', s)
    return s

def string_to_mtext(s):
    return s.replace('\\', '\\\\').replace(u'\n', u'\P')

def mtext_to_string(s):
    return unformat_text(s).replace(u'\\P', u'\n')

def text_width(text_item):
    bbox_min, bbox_max = text_item.GetBoundingbox()
    return bbox_max[0] - bbox_min[0]