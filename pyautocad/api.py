#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12

import re
import math
import array

#import win32com
import comtypes
import comtypes.gen.AutoCAD as ACAD
#import comtypes.gen._851A4561_F4EC_4631_9B0C_E7DC407512C9_0_1_0 as r
import pyautocad.types


class Autocad(object):

    def __init__(self, create_if_not_exists=False, visible=True):
        self._open_if_not_run = create_if_not_exists
        self._visible = True
        self._app = None
        self._doc = None
        self._model = None

    @property
    def app(self):
        if self._app is None:
            #self._app = win32com.client.Dispatch('AutoCAD.Application')
            try:
                self._app = comtypes.client.GetActiveObject('AutoCAD.Application')
            except WindowsError:
                if not self._open_if_not_run:
                    raise
                self._app = comtypes.client.CreateObject('AutoCAD.Application')
                self._app.Visible = self._visible


        return self._app

    @property
    def doc(self):
        if self._doc is None:
            self._doc = self.app.ActiveDocument
        return self._doc

    @property
    def model(self):
        if self._model is None:
            self._model = self.doc.ModelSpace
        return self._model

    def iter_objects(self, object_name_or_list=None, container=None, limit=None, fast=False):
        if not container:
            container = self.doc.ActiveLayout.Block
        object_names = object_name_or_list
        if object_names:
            if isinstance(object_names, basestring):
                object_names = [object_names]
            object_names = [n.lower() for n in object_names]
                
        count = container.Count
        for i in xrange(count):
            item = container.Item(i)
            if limit and i >= limit:
                return
            if object_names:
                object_name = item.ObjectName.lower()
                if not any(possible_name in object_name for possible_name in object_names):
                    continue
            if not fast:
                item = self.best_interface(item)
            yield item
    

    def iter_objects_fast(self, object_name=None, container=None, limit=None):
        return self.iter_objects(object_name, container, limit, fast=True)

    def best_interface(self, obj):
        return comtypes.client.GetBestInterface(obj)

    def prompt(self, text):
        print text
        self.doc.Utility.Prompt(u"%s\n" % text)
        
    def get_selection(self, text):
        self.prompt(text)
        try:
            self.doc.SelectionSets.Item("SS1").Delete()
        except Exception: 
            print 'Delete failed'
            pass
        selection = self.doc.SelectionSets.Add("SS1")
        selection.SelectOnScreen()
        return selection

    aDouble = staticmethod(pyautocad.types.aDouble)
    aInt = staticmethod(pyautocad.types.aInt)
    aShort = staticmethod(pyautocad.types.aShort)

if __name__ == '__main__':
    acad = Autocad()
    text = 'Line1\nLine2\nLine3\n\n\nBackslash\\ and \\P {}'
    from pyautocad.utils import string_to_mtext
    acad.model.AddMText(acad.aDouble(0,0,0), 10, string_to_mtext(text))

    for t in acad.iter_objects('mtext'):
        print t.TextString


