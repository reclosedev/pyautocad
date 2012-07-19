#!/usr/bin/env python
# -*- coding: utf-8 -*-
import array

from .query_tree import Q
from .dxf_codes import name_to_dxf_code

def convert_tree(node):
    conditions = flatten_sset_tree(node, [])
    return convert_to_filter_type_and_data(conditions)

def flatten_sset_tree(node, result, level=0):

    def show(*items):
        print '  ' * level, ' '.join(map(unicode, items))

    connector = node.connector if not node.negated else 'NOT'
    op = '<%s' % connector
    show(op)
    result.append((-4, op))
    show('<%s' % connector)
    for child in node.children:
        if isinstance(child, tuple):
            show('append', child)
            result.append(child)
        else:
            flatten_sset_tree(child, result, level + 1)
    op = '>%s' % connector
    show(op)
    result.append((-4, op))
    return result


def convert_condition_to_dxf_code(condition):
    return condition


def convert_to_filter_type_and_data(conditions):
    for cond in conditions:
        print cond
        print convert_condition_to_dxf_code(cond)