#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from argparse import Namespace
import json
from pstruct.core import Pstruct, NestedPStruct
from pstruct.hashable import HashaDictMixin
from pstruct import functions


class TestConversions(unittest.TestCase):
    def test_from_dict(self):
        d1 = {"foo": 2, "bar": 3, "spam": {"a": 22, "b": 33}}
        ps1 = Pstruct(d1)
        assert dict(ps1) == d1

    def test_with_slots(self):
        class MyStruct(Pstruct):
            __slots__ = ("foo", "bar", "spam")

        d1 = {"foo": 2, "bar": 3, "spam": {"a": 22, "b": 33}}
        ps1 = MyStruct(d1)
        assert d1["foo"] == ps1.foo
        assert d1["spam"]["a"] == ps1.spam["a"]

        s1 = json.dumps(ps1)
        assert s1 == '{"foo": 2, "bar": 3, "spam": {"a": 22, "b": 33}}'
        ps2 = MyStruct(json.loads(s1))
        assert ps1 == ps2

    def test_with_slots_nested(self):
        class MyStruct(NestedPStruct):
            __slots__ = ("foo", "bar", "spam", "eggs", "a", "b")

        d1 = {"foo": 2, "bar": 3, "spam": {"a": {"eggs": 22}, "b": 33}}
        ps1 = MyStruct(d1)
        assert d1["spam"]["a"]['eggs'] == ps1.spam.a.eggs
        assert type(ps1.spam.a) == MyStruct

        s1 = json.dumps(ps1)
        assert s1 == '{"foo": 2, "bar": 3, "spam": {"a": {"eggs": 22}, "b": 33}}'
        ps2 = MyStruct(json.loads(s1))
        assert ps1 == ps2

    def test_from_namespace(self):
        ns1 = Namespace(foo=2, bar=3)
        test1 = Pstruct(vars(ns1))
        assert dict(test1) == {"foo": 2, "bar": 3}

        ns2 = Namespace(foo=2, bar=3, spam={"a": 22, "b": 33})
        test2 = Pstruct(vars(ns2))
        assert dict(test2) == {"foo": 2, "bar": 3, "spam": {"a": 22, "b": 33}}


if __name__ == "__main__":
    unittest.main()
