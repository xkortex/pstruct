#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dstruct.validity import is_invalid_key, InvalidKeyName


class Dstruct(dict):
    """
    A dict-compatible data structure with attributes defined by slots.
    Keys are checked for compatibility with namespaces and identifiers.
    This means keys that are keywords like `def`, `class`, `with`, `in` etc are
    forbidden, as are dunder methods like __iter__, and any methods which collide with
    dict methods, such as `items` and `keys`. Why? Cause that's the rules.
    Running with -O (disabling __debug__) disables the checks.
    """

    __slots__ = ["_dstruct"]

    def __init__(self, *args, **kwargs):
        """
        Dstruct() -> new empty dictionary
        Dstruct(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        Dstruct(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        Dstruct(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  Dstruct(one=1, two=2)
                """
        tmp = dict(*args, **kwargs)
        if __debug__ and any(map(is_invalid_key, tmp)):
            bad_keys = [k for k in tmp if is_invalid_key(k)]
            raise InvalidKeyName(bad_keys)
        super(Dstruct, self).__init__(tmp)

    def __getattr__(self, name):
        if name in self.__slots__:
            return self[name]
        return self.__getattribute__(name)

    def __setattr__(self, key, value):
        print("__setattr__({}, {})".format(key, value))
        if key in self.__slots__:
            self[key] = value
            return
        if key in type(self).__dict__:
            self[key] = value
            return
        raise AttributeError(
            "type object '{}' has no attribute '{}'".format(type(self).__name__, key)
        )
