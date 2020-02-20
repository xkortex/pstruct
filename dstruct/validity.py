#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from keyword import kwlist

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3

dict_list = [x for x in dict.__dict__]
kwset = set(kwlist + dict_list)  # this is faster than iskeyword()

pat_identifier = re.compile(r"^[a-zA-Z_]\w*$")


def is_invalid_key(s):
    # type: (str) -> Bool
    """
    Check if a string is not a valid identifier and thus unsuitable for use as a
    Dstruct key.
    Invalid

    :param s: string to check
    :type s: str
    :return: True if string is invalid
    :rtype: bool

    >>> is_invalid_key('aoeu')
    False
    >>> is_invalid_key('[aoeu')
    True
    >>> is_invalid_key('2aoeu')
    True
    >>> is_invalid_key('_2aoeu')
    False
    >>> is_invalid_key('ao.eu')
    True
    >>> is_invalid_key('items')
    True

    """
    if s in kwset:
        return True
    return re.match(pat_identifier, s) is None


class InvalidKeyName(Exception):
    """Key is not a valid identifier"""

    def __init__(self, key_or_keys):
        msg = (
            "The following keys cannot be used as a key because either it is a "
            "builtin method, or is not a valid identifier: {}".format(key_or_keys)
        )

        super(InvalidKeyName, self).__init__(msg)
