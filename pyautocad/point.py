#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
import array
import operator
import math


class APoint(array.array):
    def __new__(cls, x_or_seq, y=0.0, z=0.0):
        if isinstance(x_or_seq, (array.array, list, tuple)) and len(x_or_seq) == 3:
            return super(APoint, cls).__new__(cls,'d', x_or_seq)
        return super(APoint, cls).__new__(cls,'d', (x_or_seq, y, z))

    def distance_to(self, other):
        return distance(self, other)
        
    @property
    def x(self):
        return self[0]
        
    @x.setter
    def x(self, value):
        self[0] = value
        
    @property
    def y(self):
        return self[0]
        
    @y.setter
    def y(self, value):
        self[0] = value
        
    @property
    def z(self):
        return self[2]
        
    @z.setter
    def z(self, value):
        self[2] = value
    
    def __add__(self, other):
        return self.__left_op(self, other, operator.add)

    def __sub__(self, other):
        return self.__left_op(self, other, operator.sub)
    
    def __mul__(self, other):
        return self.__left_op(self, other, operator.mul)
        
    def __div__(self, other):
        return self.__left_op(self, other, operator.div)
    
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rdiv__ = __div__

    def __neg__(self):
        return self.__left_op(self, -1, operator.mul)
    
    def __left_op(self, p1, p2, op):
        if isinstance(p2, (float, int)):
            return APoint(op(p1[0], p2), op(p1[1], p2), op(p1[2], p2))
        return APoint(op(p1[0], p2[0]), op(p1[1], p2[1]), op(p1[2], p2[2]))
    
    def __iadd__(self, p2):
        return self.__iop(p2, operator.add)
    
    def __isub__(self, p2):
        return self.__iop(p2, operator.sub)
        
    def __imul__(self, p2):
        return self.__iop(p2, operator.mul)

    def __idiv__(self, p2):
        return self.__iop(p2, operator.div)

    def __iop(self, p2, op):
        if isinstance(p2, (float, int)):
            self[0] = op(self[0], p2)
            self[1] = op(self[1], p2)
            self[2] = op(self[2], p2)
        else:
            self[0] = op(self[0], p2[0])
            self[1] = op(self[1], p2[1])
            self[2] = op(self[2], p2[2])
        return self

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return 'APoint(%.2f, %.2f, %.2f)' % tuple(self)

    def __eq__(self, other):
        if not isinstance(other, (array.array, list, tuple)):
            return False
        return tuple(self) == tuple(other)


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + 
                      (p1[1] - p2[1])**2 + 
                      (p1[2] - p2[2])**2)

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
    import dis
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
    