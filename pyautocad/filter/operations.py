#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
import re

from pyautocad.types import APoint


def _custom_operations():
    # TODO icontains, re, distance
    # a - object.value
    # b - user value
    def op_in(a, b):
        return a in b

    def op_in_part(a, b):
        return any(s in a for s in b)

    def op_re(a, b):
        return re.search(b, a)

    def op_rem(a, b):
        return re.match(b, a)

    def op_icontains(a, b):
        return b.lower() in a.lower()

    def op_startswith(a, b):
        return a.startswith(b)

    def op_endswith(a, b):
        return a.endswith(b)

    def op_range(a, b):
        return b[0] <= a <= b[1]

    def op_x(a, b):
        return a[0]

    def op_y(a, b):
        return a[1]

    def op_z(a, b):
        return a[2]

    def op_len(a, b):
        return len(a)

    def op_distance(a, b): # eq check
        distance = APoint(a).distance_to(b[0])
        return distance == b[1]

    op_dist = op_distance

    func_map = {name.lstrip('op_'): value
                for name, value in list(locals().items())
                if name.startswith('op_')}

    def _create_dist_compare_func(name):
        op = getattr(operator, name)
        def dist_compare(a, b):
            distance = APoint(a).distance_to(b[0])
            print distance, op
            return op(distance, b[1])
        dist_compare.__name__ = 'distance_%s' % name
        return dist_compare

    for name in _standard_operator_names:
        func = _create_dist_compare_func(name)
        func_map['distance_%s' % name] = func_map['dist_%s' % name] = func

    return func_map

_standard_operator_names = ('eq', 'ne', 'lt', 'le', 'gt', 'ge', 'contains')
operations = _custom_operations()
operations.update({name: getattr(operator, name)
                  for name in _standard_operator_names})

extractors_as_operation = frozenset(['x', 'y', 'z', 'len'])

