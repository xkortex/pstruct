#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pstruct.core import Dstruct, ValidatedDstruct
from pstruct.hashable import HashaDictMixin


def test_crazy_dict_as_key_nonsense():
    """Since HashaDictMixin is hashable, you can use it as a key in a dict!"""
    class MyStruct(ValidatedDstruct, HashaDictMixin):
        pass

    d = MyStruct(a=2, b=3)
    e = MyStruct({d: 'wow'})
    print(hash(e))


if __name__ == "__main__":
    # this will fail without -O
    d = {"a": 2, "items": "oops"}
    d2 = Dstruct(d)
    test_crazy_dict_as_key_nonsense()
