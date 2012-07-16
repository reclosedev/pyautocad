#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
import functools
from collections import namedtuple
from pprint import pprint
import comtypes.client

from .operations import operations

BaseMatcher = namedtuple('BaseMatcher', 'extractor, name, operation, value')


class Matcher(BaseMatcher):
    def __repr__(self):
        return '<%s %s %r>' % (self.extractor.__name__, self.operation.__name__, self.value)


class Query(object):
    """ Parses kwargs with Django-ORM-like query and check object for match
    """
    _sentinel = object()
    _acad_entity_fields = frozenset([
        'Application', 'Database', 'Document', 'EntityName', 'EntityType',
        'Handle', 'HasExtensionDictionary', 'Layer', 'Linetype', 'LinetypeScale',
        'Lineweight', 'Material', 'ObjectID', 'ObjectName', 'OwnerID', 'PlotStyleName',
        'TrueColor', 'Visible', 'color', 'value'
    ])
    _name_as_op = frozenset(['x', 'y', 'z'])  # TODO str

    def __init__(self, query_dict):
        self._matchers = self._parse_query(query_dict)

    def _parse_query(self, query_dict):
        # parse 'and' queries
        matchers = []
        for field, value in query_dict.items():
            extractor, name, operation = self._parse_field(field, value)
            matchers.append(Matcher(extractor, name, operation, value))
        pprint(matchers)

        def smart_key(matcher):
            """ First sort by general methods """
            return matcher.name not in ('ObjectName', 'EntityName', 'EntityType'), matcher.name

        return sorted(matchers, key=smart_key)

    def need_best_interface(self):
        return any(m.name not in self._acad_entity_fields
                   for m in self._matchers)

    def execute(self, obj, got_best_interface=False):
        # TODO maybe all()?
        # TODO delegate to Matcher?
        for matcher in self._matchers:
            # if GetBestInterface is very expensive, so we check it in last moment
            # if all other conditions are meet
            if not got_best_interface and matcher.name not in self._acad_entity_fields:
                obj = comtypes.client.GetBestInterface(obj)
                got_best_interface = True
            obj_value = matcher.extractor(obj)
            try:
                if not matcher.operation(obj_value, matcher.value):
                    return False, obj
            except Exception as e:
                print e
                return False, obj
        return True, obj

    def _parse_field(self, field, value=None):
        # TODO value can be callable, in this case we should extract attributes and call func against them
        name = field
        operation = operator.eq
        if '__' in field:
            fields = field.split('__')
            name = fields[0]
            # if field is ending with property or digit like InsertionPoint__x, add eq op
            if fields[-1] in self._name_as_op or fields[-1].isdigit():
                fields.append('eq')
            if len(fields) == 2:
                operation = self._get_operation(fields[1])
            elif len(fields) > 2:
                chain = [self._get_operation(op) for op in fields[1:]]
                operation = _ChainedOp(chain)

        extractor, name = self._get_extractor(name)
        operation = _check_sentinel(operation)
        return extractor, name, operation

    def _get_operation(self, name):
        if name.isdigit():
            n = int(name)
            def operation(a, b):
                return a[n]
            operation.__name__ = 'op_%s' % name
            return operation
        operation = operations.get(name)
        if not operation:
            raise Exception('Unknown operation %r' % name)
        return operation

    def _get_extractor(self, name):
        name = ''.join(name[:1].upper() + name[1:])
        def extractor(obj):
            return getattr(obj, name, self._sentinel)

        extractor.__name__ = 'Extract<%r>' % name
        return extractor, name

    def __str__(self):
        return '\n'.join(self._matchers)


def _check_sentinel(func):
    @functools.wraps(func)
    def wrapper(a, b):
        if a is Query._sentinel:
            return False
        return func(a, b)
    return wrapper


class _ChainedOp(object):
    def __init__(self, chain):
        self._chain = chain

    def __call__(self, a, b):
        r = a
        for op in self._chain:
            r = op(r, b)
        return r

    def __repr__(self):
        return 'Chain<%s>' % ' -> '.join(f.__name__ for f in self._chain)

    @property
    def __name__(self):
        return self.__repr__()
