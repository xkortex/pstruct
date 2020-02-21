import unittest
from pstruct import Dstruct
from pstruct.hashable import HashaDictMixin


class TestSimple(unittest.TestCase):
    def test_kwargs(self):
        d = Dstruct(a=2, b=3)

    def test_from_dict(self):
        d = dict(a=2, b=3)
        d2 = Dstruct(d)


class TestMixins(unittest.TestCase):
    def test_hash_mixin(self):
        class MyStruct(Dstruct, HashaDictMixin):
            pass

        d = MyStruct(a=2, b=3)
        print(hash(d))

    def test_crazy_dict_as_key_nonsense(self):
        """Since HashaDictMixin is hashable, you can use it as a key in a dict!"""

        class MyStruct(Dstruct, HashaDictMixin):
            pass

        d = MyStruct(a=2, b=3)
        e = {d: 'wow why would you want this'}
        print(e)


if __name__ == "__main__":
    unittest.main()
