#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
import re


def _custom_operations():
    # TODO icontains, re, etc.
    # a - object.value
    # b - user value
    def op_in(a, b):
        return a in b

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
        return a >= b[0] and a <= b[1]

    def op_x(a, b):
        return a[0]

    def op_y(a, b):
        return a[1]

    def op_z(a, b):
        return a[2]

    def op_len(a, b):
        return len(a)

    return {name.lstrip('op_'): value for name, value in list(locals().items())}


operations = _custom_operations()
operations.update({name: getattr(operator, name)
                  for name in ('eq', 'ne', 'lt', 'le', 'gt', 'ge', 'contains')})