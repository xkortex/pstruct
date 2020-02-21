#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import errno
import stat
from ._compat import filename_to_ui, get_filesystem_encoding, text_type
from .exceptions import BadFilePath, BadParameter

FileNotFoundError = getattr(__builtins__, "FileNotFoundError", IOError)


class ParamType(object):
    """Helper for converting values through types.  The following is
    necessary for a valid type:

    *   it needs a name
    *   it needs to pass through None unchanged
    *   it needs to convert from a string
    *   it needs to convert its result type through unchanged
        (eg: needs to be idempotent)
    *   it needs to be able to deal with param and context being `None`.
        This can be the case when the object is used with prompt
        inputs.
    """

    #: the descriptive name of this type
    name = None

    def __call__(self, value, param=None, ctx=None):
        if value is not None:
            return self.convert(value, param, ctx)

    def convert(self, value, param=None, ctx=None):
        # type: (str, str, Any) -> Any
        """Converts the value from string to its type.
        This is not invoked for values that are `None` (the missing value).
        """
        return value

    def fail(self, message, param=None, ctx=None):
        """Helper method to fail with an invalid value message."""
        raise BadParameter(message, ctx=ctx, param=param)


class Path(ParamType):
    """The path type is similar to the :class:`File` type but it performs
    different checks.  First of all, instead of returning an open file
    handle it returns just the filename.  Secondly, it can perform various
    basic checks about what the file or directory should be.

    .. versionchanged:: 6.0
       `allow_dash` was added.

    :param exists: if set to true, the file or directory needs to exist for
                   this value to be valid.  If this is not required and a
                   file does indeed not exist, then all further checks are
                   silently skipped.
    :param file_okay: controls if a file is a possible value.
    :param dir_okay: controls if a directory is a possible value.
    :param writable: if true, a writable check is performed.
    :param readable: if true, a readable check is performed.
    :param resolve_path: if this is true, then the path is fully resolved
                         before the value is passed onwards.  This means
                         that it's absolute and symlinks are resolved.  It
                         will not expand a tilde-prefix, as this is
                         supposed to be done by the shell only.
    :param allow_dash: If this is set to `True`, a single dash to indicate
                       standard streams is permitted.
    :param path_type: optionally a string type that should be used to
                      represent the path.  The default is `None` which
                      means the return value will be either bytes or
                      unicode depending on what makes most sense given the
                      input data Click deals with.
    """

    envvar_list_splitter = os.path.pathsep

    def __init__(
        self,
        exists=False,
        file_okay=True,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=False,
        allow_dash=False,
        path_type=None,
    ):
        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.writable = writable
        self.readable = readable
        self.resolve_path = resolve_path
        self.allow_dash = allow_dash
        self.type = path_type

        if self.file_okay and not self.dir_okay:
            self.name = "file"
            self.path_type = "File"
        elif self.dir_okay and not self.file_okay:
            self.name = "directory"
            self.path_type = "Directory"
        else:
            self.name = "path"
            self.path_type = "Path"

    def coerce_path_result(self, rv):
        if self.type is not None and not isinstance(rv, self.type):
            if self.type is text_type:
                rv = rv.decode(get_filesystem_encoding())
            else:
                rv = rv.encode(get_filesystem_encoding())
        return rv

    def convert(self, value, param=None, ctx=None):
        rv = value

        is_dash = self.file_okay and self.allow_dash and rv in (b"-", "-")
        if is_dash:
            return self.coerce_path_result(rv)

        if self.resolve_path:
            rv = os.path.realpath(rv)

        try:
            st = os.stat(rv)
        except OSError:
            if not self.exists:
                return self.coerce_path_result(rv)
            reason = "Could not stat {}, it does not exist".format(self.path_type)
            raise BadFilePath(filename_to_ui(value), param, reason)

        ui_filename = filename_to_ui(value)

        if not self.file_okay and stat.S_ISREG(st.st_mode):
            reason = "is a path, wanted {}".format(self.path_type)
            raise BadFilePath(ui_filename, param, reason)

        if not self.dir_okay and stat.S_ISDIR(st.st_mode):
            reason = "is a directory, wanted {}".format(self.path_type)
            raise BadFilePath(ui_filename, param, reason)

        if self.writable and not os.access(value, os.W_OK):
            reason = "{} is not writable".format(self.path_type)
            raise BadFilePath(ui_filename, param, reason)

        if self.readable and not os.access(value, os.R_OK):
            reason = "{} is not readable".format(self.path_type)
            raise BadFilePath(ui_filename, param, reason)

        return self.coerce_path_result(rv)
