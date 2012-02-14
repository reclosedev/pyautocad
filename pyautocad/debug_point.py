#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
import array
import math

from pyautocad.types import APoint

def echo(arg):
    import inspect
    import re
    frame = inspect.currentframe()
    try:
        context = inspect.getframeinfo(frame.f_back).code_context
        caller_lines = ''.join([line.strip() for line in context])
        m = re.search(r'echo\s*\((.+?)\)$', caller_lines)
        if m:
            caller_lines = m.group(1)
        print '%s -> %s' % (caller_lines, arg)
    finally:
        del frame

if __name__ == '__main__':
    import timeit

    def points_add_loop():
        p = APoint(1, 1, 1)
        for i in xrange(1000):
            p = p + i
    
    def points_iadd_loop():
        p = APoint(1, 1, 1)
        for i in xrange(1000):
            p += i
            
    def points_piadd_loop():
        p = APoint(1, 1, 1)
        p2 = APoint(2, 2, 2)
        for i in xrange(1000):
            p += p2
                    
    def int_add_loop():
        n = 1.12345
        for i in xrange(1000):
            n += i
            
    def int_iadd_loop():
        n = 1.12345
        for i in xrange(1000):
            n = n + i
    
    #p = APoint(0, 0, 0)
    #dis.dis(p.__iadd__)
    def benchmark():
        print timeit.timeit(int_add_loop, number=1000)
        print timeit.timeit(int_iadd_loop, number=1000)
        print timeit.timeit(points_iadd_loop, number=1000)
        print timeit.timeit(points_piadd_loop, number=1000)
        print timeit.timeit(points_add_loop, number=1000)
    
    a1 = array.array('d', (10, 10, 10))
    p1 = APoint(1, 1)
    p2 = APoint(2, 2)
    p2.x = 3
    echo((1, 1, 0) + p1)
    echo(p1 + (1, 1, 0))
    
    echo(p1.distance_to(p2))
    echo(p1 + p2)
    echo(p1 * 5)
    echo(p1 + 1 * p2)
    echo((p1 + 1) * p2)
    echo(p1 / 5)
    echo(p2 - p2)
    echo(p2 - p1)
    echo(p1 + 10)
    echo(p1[0])
    echo((p1.x, p1.y, p1.z))
    