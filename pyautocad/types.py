#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
import array

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
