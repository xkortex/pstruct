#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Mapping, Iterable
from ._compat import is_nonstring_iterable
from typing import Any, TypeVar

_default = dict()

JsonAble = TypeVar('JsonAble', Mapping, Iterable)


def deep_update(old, new, inplace=False):
    # type: (JsonAble, JsonAble, bool) -> JsonAble
    """Merge values of 'new' into 'old', updating in a nested fashion.
     Chainmap is probably better, but I need to support some python2 stuff
    :param old: Initial nested data structure to be updated
    :param new: Nested data structure with new values to be added into 'old'

    Note: doctest/xdoctest on python2 is not maintained.

    >>> d1 = {'a':2, 'b': {'bb': 33}, 'c': [{}, {}]}
    >>> d2 = {'a':4, 'b': {'bb': 66}}
    >>> d3 = {'a':4, 'b': {'bb': 33}, 'c': [{'c2': 5}]}
    >>> do1 = deep_update(d1, d2)
    >>> print(do1)
    {'a': 4, 'b': {'bb': 66}, 'c': [{}, {}]}
    >>> deep_update(d1, d3)
    {'a': 4, 'b': {'bb': 33}, 'c': [{'c2': 5}]}
    """

    if old is _default:
        return new

    is_map = isinstance(old, Mapping)
    is_iter = is_nonstring_iterable(old) and not is_map

    # leaf case
    if not (is_map or is_iter):
        return new

    if is_iter:
        return [deep_update(_default, x) for x in new]

    if inplace:
        out = old
    else:
        out = old.copy()

    # not sure if this is the best check for mappable types, works for now
    if is_map:
        for key, value in new.items():
            out[key] = deep_update(old.get(key, _default), value)
        return out
    raise NotImplementedError("not ready")
