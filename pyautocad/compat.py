import sys

IS_PY3 = sys.version_info[0] == 3

if IS_PY3:
    unicode = str
    bytes = bytes
    basestring = str
    xrange = range
else:
    unicode = unicode
    _orig_bytes = bytes
    bytes = lambda s, *a: _orig_bytes(s)
    basestring = basestring
    xrange = xrange