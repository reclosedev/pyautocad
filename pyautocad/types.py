#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
import array
import operator
import math


class APoint(array.array):
    def __new__(cls, x_or_seq, y=0.0, z=0.0):
        if isinstance(x_or_seq, (array.array, list, tuple)) and len(x_or_seq) == 3:
            return super(APoint, cls).__new__(cls, 'd', x_or_seq)
        return super(APoint, cls).__new__(cls, 'd', (x_or_seq, y, z))

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
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

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
    return math.sqrt((p1[0] - p2[0]) ** 2 +
                     (p1[1] - p2[1]) ** 2 +
                     (p1[2] - p2[2]) ** 2)


def aDouble(*seq):
    return _sequence_to_comtypes('d', *seq)


def aInt(*seq):
    return _sequence_to_comtypes('l', *seq)


def aShort(*seq):
    return _sequence_to_comtypes('h', *seq)


def _sequence_to_comtypes(typecode='d', *sequence):
    if len(sequence) == 1:
        return array.array(typecode, sequence[0])
    return array.array(typecode, sequence)
