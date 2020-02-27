#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Mapping
from pstruct.validity import is_invalid_key, InvalidKeyName


class Pstruct(dict):
    """
    A dict-compatible data structure with attributes defined by slots.
    """

    __slots__ = ["_pstruct"]

    def __init__(self, *args, **kwargs):
        """
        Pstruct() -> new empty dictionary
        Pstruct(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        Pstruct(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        Pstruct(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  Pstruct(one=1, two=2)
                """
        super(Pstruct, self).__init__(*args, **kwargs)

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


class ValidatedPstruct(Pstruct):
    """
        A dict-compatible data structure with attributes defined by slots.
        Keys are checked for compatibility with namespaces and identifiers.
        This means keys that are keywords like `def`, `class`, `with`, `in` etc are
        forbidden, as are dunder methods like __iter__, and any methods which collide with
        dict methods, such as `items` and `keys`. Why? Cause that's the rules.
        Running with -O (disabling __debug__) disables the checks.
        """

    def __init__(self, *args, **kwargs):
        tmp = dict(*args, **kwargs)
        if __debug__ and any(map(is_invalid_key, tmp)):
            bad_keys = [k for k in tmp if is_invalid_key(k)]
            raise InvalidKeyName(bad_keys)
        super(ValidatedPstruct, self).__init__(tmp)


class NestedPStruct(Pstruct):
    def __init__(self, *args, **kwargs):
        """EXPERIMENTAL - automatically generate nested Pstruct attr-gettable
        data structures
        """
        tmp = dict(*args, **kwargs)
        for k, v in tmp.items():
            if isinstance(v, Mapping):
                tmp[k] = self.__class__(v)
        super(NestedPStruct, self).__init__(tmp)
