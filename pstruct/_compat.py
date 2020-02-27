import re
import os
import sys
import collections


PY2 = sys.version_info[0] == 2
CYGWIN = sys.platform.startswith("cygwin")
MSYS2 = sys.platform.startswith("win") and ("GCC" in sys.version)
# Determine local App Engine environment, per Google's own suggestion
APP_ENGINE = "APPENGINE_RUNTIME" in os.environ and "Development/" in os.environ.get(
    "SERVER_SOFTWARE", ""
)
WIN = sys.platform.startswith("win") and not APP_ENGINE and not MSYS2
DEFAULT_COLUMNS = 80


_ansi_re = re.compile(r"\033\[[;?0-9]*[a-zA-Z]")


def get_filesystem_encoding():
    return sys.getfilesystemencoding() or sys.getdefaultencoding()


if PY2:
    text_type = unicode
    raw_input = raw_input
    string_types = (str, unicode)
    primitive_iterable = (str, unicode, bytes)  # i.e. non-list iterables
    int_types = (int, long)
    iteritems = lambda x: x.iteritems()
    range_type = xrange

    def is_bytes(x):
        return isinstance(x, (buffer, bytearray))

    _identifier_re = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

    def is_nonstring_iterable(x):
        """This is needed to differentiate strings from list-like containers"""
        if isinstance(x, primitive_iterable):
            return False
        return isinstance(x, collections.Iterable)

    def isidentifier(x):
        return _identifier_re.search(x) is not None

    def filename_to_ui(value):
        if isinstance(value, bytes):
            value = value.decode(get_filesystem_encoding(), "replace")
        return value


else:
    text_type = str
    raw_input = input
    string_types = (str,)
    primitive_iterable = (str, bytes)  # i.e. non-list iterables
    int_types = (int,)
    range_type = range
    isidentifier = lambda x: x.isidentifier()
    iteritems = lambda x: iter(x.items())

    def is_nonstring_iterable(x):
        if isinstance(x, primitive_iterable):
            return False
        return isinstance(x, collections.Iterable)

    def is_bytes(x):
        return isinstance(x, (bytes, memoryview, bytearray))

    def filename_to_ui(value):
        if isinstance(value, bytes):
            value = value.decode(get_filesystem_encoding(), "replace")
        else:
            value = value.encode("utf-8", "surrogateescape").decode("utf-8", "replace")
        return value
