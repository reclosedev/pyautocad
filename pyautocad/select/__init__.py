import array
import comtypes
from comtypes.partial import partial

from .converter import convert_tree, ConverterError
from .query_tree import Q

__all__ = ['Q', 'ConverterError']

try:
    from comtypes.gen import AutoCAD
except ImportError:
    AutoCAD = None


class _(partial, AutoCAD.IAcadDocument):
    def select(self, *args, **kwargs):
        tree = Q(*args, **kwargs)
        types, data = convert_tree(tree)
        return _ssget(self.SelectionSets, types, data)


def _ssget(selection_sets, filter_type, filter_data,
           selection=AutoCAD.acSelectionSetAll, name="SS_1__"):
    try:
        selection_sets.Item(name).Delete()
    except Exception:
        pass
    sset = selection_sets.Add(name)
    try:
        sset.Select(
            selection,
            FilterType=array.array('h', filter_type),
            FilterData=filter_data,
        )
    except comtypes.COMError as e:
        print e.details[0]
        raise
    return sset






