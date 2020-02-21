#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import errno

FileNotFoundError = getattr(__builtins__, "FileNotFoundError", IOError)


class Dummy(object):
    def __str__(self):
        return ""


_default = Dummy()


class BadParameter(Exception):
    """An exception that formats out a standardized error message for a
    bad parameter.

    """

    def __init__(self, value=None, param=None, ctx=None, param_hint=None):
        msg = "Invalid value for parameter: {param_name}={value}".format(
            param_name=param, value=value
        )

        super(BadParameter, self).__init__(msg)
        self.param = param
        self.param_hint = param_hint


class BadFilePath(Exception):
    """Something invalid about a file/directory/path/etc.

    todo: should probably split out FileNotFoundError with unable to write etc
    e.g. FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
    """

    def __init__(
        self, value, param=_default, reason=_default, ctx=None, param_hint=None
    ):
        if reason is not _default:
            reason = " ({})".format(reason)

        if param is not _default:
            param = " for parameter '{}'".format(param)

        msg = "Bad path{param}{reason}: {value}".format(
            param=param, value=value, reason=reason
        )

        super(BadFilePath, self).__init__(msg)
        self.param = param
        self.param_hint = param_hint
