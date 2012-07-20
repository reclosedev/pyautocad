#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. versionadded:: 0.2.0

    pyautocad.filter.query
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains man filter functions and classes
"""
import operator
import functools
from collections import namedtuple
from pprint import pprint
import comtypes.client

from .operations import operations, extractors_as_operation

__all__ = ['QuerySet']

class UnknownOperation(Exception):
    """ Raised when operation is unknown
    """

class QuerySet(object):
    """ Class which recieves user queries and act like iterator or list for results

    When QuerySet is used as iterator, it can't be used second time.
    After operations such as ``len(qs)`` or ``qs.all()`` results are cached and
    can be accessed many times.
    """
    def __init__(self, object_names, query_or_dict,
                 block=None, block_iterator=None, need_best_interface=False):
        """
        :param object_names:
            check this names against ObjectName property of object
        :param query_or_dict:
            dict in form {SomeProperty__qt: value} or already parsed Query object
        :param block:
            block which will be iterated to search objects
        :param block_iterator:
            custom iterator can be passed instead block
        :param need_best_interface:
            indicates that objects from blocks should be casted to best interface
            it needed if you want to use properties such as TextString
        """
        if block is not None:
            self._block_iterator = self._iterate_block(block)
        elif block_iterator is not None:
            self._block_iterator = block_iterator

        assert self._block_iterator, "Block or block_iterator should be provided"

        if isinstance(query_or_dict, Query):
            self._query = query_or_dict
        else:
            self._query = Query(object_names, query_or_dict)

        self._need_best_interface = need_best_interface
        self._iter_started = False
        self._cache = None

    def _iterator(self):
        assert not self._iter_started, "Can't iterate second time"
        self._iter_started = True
        query = self._query

        for obj in self._block_iterator:
            matches, got_best_interface, obj = query.execute(obj)
            if matches:
                if self._need_best_interface:
                    if not got_best_interface:
                        obj = comtypes.client.GetBestInterface(obj)
                yield obj

    def _iterate_block(self, block):
        count = block.Count
        for i in xrange(count):
            obj = block.Item(i)
            yield obj

    def __iter__(self):
        if self._cache:
            return iter(self._cache)
        return self._iterator()

    def __len__(self):
        """ used for ``len(qs)`` shortcut for :meth:`count`
        """
        return self.count()

    def __getitem__(self, k):
        """ list like ``__getitem__`` interface.

        Supports slices and random access. If slice has end bound, then results
        are fetched TODO... otherwise all results are first cached.
        """
        # checks are taken from Django
        if not isinstance(k, (slice, int, long)):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0))
                or (isinstance(k, slice) and (k.start is None or k.start >= 0)
                    and (k.stop is None or k.stop >= 0))),\
        "Negative indexing is not supported."

        if self._cache:
            return self._cache[k]

        if isinstance(k, slice):
            if k.stop is not None and k.step is None:
                stop = k.stop
                gen = self.__iter__()
                result = []
                if k.start:
                    start = k.start
                    for _ in gen:
                        start -= 1
                        if not start:
                            break
                for i, obj in enumerate(gen, k.start or 0):
                    if stop is not None and i >= stop:
                        break
                    result.append(obj)
                return result
            else:
                return [self[i] for i in range(*k.indices(len(self)))]
        return self.all()[k]

    def all(self):
        """ Returns list of all results
        """
        if not self._cache:
            # we are using __iter__ here, because list(self) can call self.__len__
            self._cache = list(self.__iter__())
        return self._cache

    def count(self):
        """ Returns number of objects for this QuerySet
        """
        return len(self.all())

    def first(self):
        """ Returns first matched object.
        """
        if self._cache:
            return self._cache[0]
        return next(self.__iter__(), None)

    def filter(self, *object_names, **kwargs):
        """ Can be used to additional filtering

        ::

            >>> acad.model.filter('AcDbMtext').filter(TextString__contains="1")

        """
        return QuerySet(object_names, kwargs, block_iterator=iter(self))

    def order_by(self, *fields, **kwargs):
        """ Order ``QuerySet`` by some fields

        Filter by InsertionPoint x value in ascend order: ::

            >>> acad.model.filter().order_by('-InsertionPoint__x')

        Filter by `TextString` `length` value in descend order and
        by `InsertionPoint` `x` value in ascend order: ::

            >>> acad.model.filter().order_by('TextString__len', '-InsertionPoint__x')

        """
        reverse = False
        strict = kwargs.pop('strict', False)
        if len(fields) == 1:
            # fast sort for one field
            sort_key, reverse = self._get_sort_key(fields[0], strict)
        else:
            # can be slow, because of Invert key and many function calls
            sort_keys = [self._get_sort_key(field, strict)
                         for field in fields]
            sort_keys, reverses = zip(*sort_keys)

            def sort_key(obj):
                return map(Inverter, [key_func(obj)
                                      for key_func in sort_keys], reverses)
        self.all() # prefetch
        self._cache.sort(key=sort_key, reverse=reverse)
        return QuerySet([], {}, block_iterator=iter(self._cache))

    def best_interface(self):
        """ Convert all matched objects to best interface

        ::

            >>> acad.model.filter('AcDbMText').best_interface().all()

        """
        return QuerySet([], {}, block_iterator=iter(self), need_best_interface=True)

    def _get_sort_key(self, field, strict=False):
        reverse = False
        if field.startswith('-'):
            reverse = True
            field = field.lstrip('-')

        if '__' in field:
            extractor, name, operation = self._query._parse_field(field, False)
            if not strict:
                def sort_key(obj):
                    return operation(extractor(obj), None)
            else:
                def sort_key(obj):
                    val = extractor(obj)
                    if val is _sentinel:
                        raise AttributeError(extractor.__name__)
                    return operation(extractor(obj), None)
        else:
            if not strict:
                def sort_key(obj):
                    return getattr(obj, field, '')
            else:
                sort_key = operator.attrgetter(field)

        return sort_key, reverse

        # TODO and maybe combine with filter
    #    def exclude(self, **kwargs):
    #        pass


class Inverter(namedtuple('Inverter', 'item, reverse')):
    def __lt__(self, other):
        if self.reverse:
            return other.item < self.item
        return self.item < other.item


BaseMatcher = namedtuple('BaseMatcher', 'extractor, name, operation, value')


class Matcher(BaseMatcher):
    def __repr__(self):
        return '<%s %s %r>' % (self.extractor.__name__,
                               self.operation.__name__,
                               self.value)


_sentinel = object()


class Query(object):
    """ Parses kwargs with Django-ORM-like query and check object for match
    """

    _acad_entity_fields = frozenset([
        'Application', 'Database', 'Document', 'EntityName', 'EntityType',
        'Handle', 'HasExtensionDictionary', 'Layer', 'Linetype',
        'LinetypeScale', 'Lineweight', 'Material', 'ObjectID', 'ObjectName',
        'OwnerID', 'PlotStyleName', 'TrueColor', 'Visible', 'color', 'value'
    ])

    def __init__(self, object_names, query_dict):
        self._matchers = self._parse_query(object_names, query_dict)

    def _parse_query(self, object_names, query_dict):
        # parse 'and' queries
        matchers = []
        if object_names:
            query_dict['ObjectName__in'] = object_names
        for field, value in query_dict.items():
            extractor, name, operation = self._parse_field(field)
            matchers.append(Matcher(extractor, name, operation, value))

        def smart_key(matcher):
            """ First sort by general methods """
            return matcher.name not in ('ObjectName',
                                        'EntityName',
                                        'EntityType'), matcher.name

        return sorted(matchers, key=smart_key)

    def execute(self, obj):
        got_best_interface = False

        for matcher in self._matchers:
            # because GetBestInterface is very expensive we call it in the
            # last moment if all other conditions are meet
            if not got_best_interface and matcher.name not in self._acad_entity_fields:
                obj = comtypes.client.GetBestInterface(obj)
                got_best_interface = True
            obj_value = matcher.extractor(obj)
            try:
                if not matcher.operation(obj_value, matcher.value):
                    return False, got_best_interface, obj
            except Exception as e:
                return False, got_best_interface, obj

        return True, got_best_interface, obj

    def _parse_field(self, field, add_eq_operation=True):
        # TODO value can be callable, in this case we should extract attributes and call func against them
        name = field
        operation = operator.eq
        if '__' in field:
            fields = field.split('__')
            name = fields[0]
            # if field is ending with property or digit like InsertionPoint__x, add eq op
            if add_eq_operation and fields[-1] in extractors_as_operation or fields[-1].isdigit():
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
            raise UnknownOperation('%r' % name)
        return operation

    def _get_extractor(self, name):
        name = ''.join(name[:1].upper() + name[1:])

        def extractor(obj):
            return getattr(obj, name, _sentinel)
        extractor.__name__ = 'Extract<%r>' % name
        return extractor, name

    def __repr__(self):
        return 'Query<%s>' % '\n'.join(self._matchers)


def _check_sentinel(func):
    @functools.wraps(func)
    def wrapper(a, b):
        if a is _sentinel:
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
