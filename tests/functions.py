#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pstruct import functions


class TestDeepUpdate(unittest.TestCase):
    def test_typical(self):
        test1 = {
            "foo": 2,
            "bar": 4,
            "a": "things",
            "b": "stuff",
            "alist": [1, 2, {"x": 8}],
        }
        test2 = {
            "bar": 44,
            "a": {"l1": 1, "k1": {"l2": 2}},
            "b": "stuffstuff",
            "c": {"c1": "v1"},
            "alist": [1, 2, {"x": 9}],
        }
        test3 = {"foo": -22, "a": {"k1": "kx"}, "b": "bx", "c": "cx"}

        result1 = {
            "foo": 2,
            "bar": 44,
            "a": {"l1": 1, "k1": {"l2": 2}},
            "b": "stuffstuff",
            "alist": [1, 2, {"x": 9}],
            "c": {"c1": "v1"},
        }

        assert functions.deep_update(test1, test2) == result1

        result2 = {"foo": 5, "a": {"k1": "kx"}, "b": "bx", "c": "cx"}
        assert functions.deep_update(test3, {"foo": 5}) == result2

        result3 = {
            "foo": -22,
            "bar": 44,
            "a": {"k1": {"l2": 2}, "l1": 1},
            "b": "stuffstuff",
            "c": {"c1": "v1"},
            "alist": [1, 2, {"x": 9}],
        }

        assert functions.deep_update(test3, test2) == result3

        functions.deep_update(test3, test2, inplace=True)
        assert test3 == result3


if __name__ == "__main__":
    unittest.main()
