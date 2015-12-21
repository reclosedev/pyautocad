#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. versionadded:: 0.1.2

    pyautocad.cache
    ~~~~~~~~~~~~~~~

    Proxy to cache all object attributes.

    :copyright: (c) 2012 by Roman Haritonov.
    :license: BSD, see LICENSE.txt for more details.
"""
from __future__ import print_function


class Cached(object):
    """
    Proxy for caching object attributes.

    Consider external class `Foo` with expensive property (we can't change its code)::

        class Foo(object):
            @property
            def x(self):
                print 'consuming time'
                time.sleep(1)
                return 42

    Cache all attributes and test access::

        foo = Foo()
        cached_foo = Cached(foo)
        for i in range(10):
            print cached_foo.x

    Output::

        consuming time
        42
        42
        42
        42
        42
        
    It's possible to switch caching off with :meth:`switch_caching`
    and retrieve original instance with :meth:`get_original`
    """
    def __init__(self, instance):
        object.__setattr__(self, '_instance', instance)
        object.__setattr__(self, '_is_enabled', True)
        object.__setattr__(self, '_storage', {})

    def get_original(self):
        """ Returns original instance
        """
        return self._instance

    def switch_caching(self, is_enabled):
        """ Switch caching on or off

        :param is_enabled: caching status `True` or `False`
        :type is_enabled: bool
        """
        self._is_enabled = is_enabled
        if not is_enabled:
            self._storage = {}
    
    def __setattr__(self, key, value):
        if key in self.__dict__:
            return object.__setattr__(self, key, value)
        object.__setattr__(self._instance, key, value)
        if self._is_enabled:
            self._storage[key] = value
        
    def __getattr__(self, key):
        if key in self.__dict__:
            return object.__getattribute__(self, key)
        storage = self._storage
        if self._is_enabled and key in storage:
            return storage[key]
        value = getattr(self._instance, key)
        storage[key] = value
        return value

    def __delattr__(self, key):
        if key in self.__dict__:
            return object.__delattr__(self, key)
        if key in self._storage:
            del self._storage[key]
        object.__delattr__(self._instance, key)


if __name__ == "__main__":
    import time

    class Foo(object):
        @property
        def x(self):
            print('consuming time')
            time.sleep(1)
            return 42

    foo = Foo()
    cached_foo = Cached(foo)
    for i in range(5):
        print(cached_foo.x)
