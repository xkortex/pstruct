#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hashlib import md5 as hasher


def hash_a_container(obj, truncate=False):
    # type: (dict, bool) -> int
    """
    Hashes a container which is iterable and its outputs are hashable.
    Getting this method so output is stable across python2 and python3 is
    tricky, due to differences in the way encodings are handled.
    Also, python2 has different int value lengths than py3, so if we just pass
    the hexdigest to int(x, 16), results diverge between py2 and py3. This
    makes doctests complicated. To make doctests match, you have to truncate
    so that the output of hash() lines up in py2 and py3.

    todo: make this better and faster
    :param obj: Container of hashables
    :param truncate:
    :return:
    """
    #
    hashval = hasher()
    for key, val in sorted(obj.items()):
        hashval.update(str(hash(key)).encode())
        hashval.update(str(hash(val)).encode())

    hash_hex = hashval.hexdigest()
    hash_hex = hash_hex[:14] if truncate else hash_hex

    return int(hash_hex, 16)


class HashaDictMixin(dict):
    def __hash__(self):
        # type: () -> int

        return hash_a_container(self)
