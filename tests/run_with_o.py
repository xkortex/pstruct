#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pstruct.core import Pstruct, ValidatedPstruct
from pstruct.hashable import HashaDictMixin


def test_crazy_dict_as_key_nonsense():
    """Since HashaDictMixin is hashable, you can use it as a key in a dict!"""
    class MyStruct(ValidatedPstruct, HashaDictMixin):
        pass

    d = MyStruct(a=2, b=3)
    e = MyStruct({d: 'wow'})
    print(hash(e))


if __name__ == "__main__":
    # this will fail without -O
    d = {"a": 2, "items": "oops"}
    d2 = Pstruct(d)
    test_crazy_dict_as_key_nonsense()
