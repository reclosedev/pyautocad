#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
import logging

import comtypes
import comtypes.gen.AutoCAD as ACAD
import pyautocad.types

__all__ = ['Autocad', 'ACAD']

logger = logging.getLogger(__name__)


class Autocad(object):
    """Main AutoCAD Automation object
    """

    def __init__(self, create_if_not_exists=False, visible=True):
        self._open_if_not_run = create_if_not_exists
        self._visible = visible
        self._app = None

    @property
    def app(self):
        """active `AutoCAD.Application`

        if `Autocad` was created with `create_if_not_exists=True`,
        it will create`AutoCAD.Application` if there is no active one
        """
        if self._app is None:
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
        """ `ActiveDocument` """
        return self.app.ActiveDocument
        

    @property
    def model(self):
        """ `ModelSpace` from active document """
        return self.doc.ModelSpace
        

    def iter_layouts(self, doc=None, skip_model=True):
        """Iterate layouts from `doc`

        If `doc=None` (default), `ActiveDocument` used
        `skip_model` omit `ModelSpace` if `True`
        """
        if doc is None:
            doc = self.doc
        for layout in sorted(doc.Layouts, key=lambda x: x.TabOrder):
            if skip_model and not layout.TabOrder:
                continue
            yield layout

    def iter_objects(self, object_name_or_list=None, block=None,
                     limit=None, dont_cast=False):
        """Iterate objects from `block`

          `object_name_or_list` - part of object type name, or list of it
          `block` - Autocad block, default - `ActiveLayout.Block`
          `limit` - max number of objects to return, default infinite
          `dont_cast` - Don't retrieve best interface for object, may speedup
                        iteration. Returned objects should be casted by caller
        """
        if block is None:
            block = self.doc.ActiveLayout.Block
        object_names = object_name_or_list
        if object_names:
            if isinstance(object_names, basestring):
                object_names = [object_names]
            object_names = [n.lower() for n in object_names]

        count = block.Count
        for i in xrange(count):
            item = block.Item(i)  # it's faster than `for item in block`
            if limit and i >= limit:
                return
            if object_names:
                object_name = item.ObjectName.lower()
                if not any(possible_name in object_name for possible_name in object_names):
                    continue
            if not dont_cast:
                item = self.best_interface(item)
            yield item

    def iter_objects_fast(self, object_name=None, container=None, limit=None):
        """Shortcut for `iter_objects(dont_cast=True)`
        """
        return self.iter_objects(object_name, container, limit, dont_cast=True)

    def find_one(self, object_name, container=None, predicate=None):
        if predicate is None:
            predicate = bool
        for obj in self.iter_objects(object_name, container):
            if predicate(obj):
                return obj
        return None

    def best_interface(self, obj):
        """ Retrieve best interface for object """
        return comtypes.client.GetBestInterface(obj)

    def prompt(self, text):
        print text
        self.doc.Utility.Prompt(u"%s\n" % text)

    def get_selection(self, text):
        self.prompt(text)
        try:
            self.doc.SelectionSets.Item("SS1").Delete()
        except Exception:
            logger.debug('Delete selection failed')

        selection = self.doc.SelectionSets.Add('SS1')
        selection.SelectOnScreen()
        return selection

    aDouble = staticmethod(pyautocad.types.aDouble)
    aInt = staticmethod(pyautocad.types.aInt)
    aShort = staticmethod(pyautocad.types.aShort)


if __name__ == '__main__':
    acad = Autocad()
    text = 'Line1\nLine2\nLine3\n\n\nBackslash\\ and \\P {}'
    from pyautocad.utils import string_to_mtext
    acad.model.AddMText(acad.aDouble(0, 0, 0), 10, string_to_mtext(text))

    for t in acad.iter_objects('mtext'):
        print t.TextString
