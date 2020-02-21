import os
import sys
import unittest
from pstruct import Pstruct
import pstruct.types
import pstruct.exceptions
import uuid
import tempfile

TEST_DIR = tempfile.mkdtemp("pstruct_tests")

# todo: i'm sure unittest has actual error handling
class TestPaths(unittest.TestCase):
    def test_path_dont_care(self):
        x = pstruct.types.Path()
        this_should_not_exist = os.path.join(TEST_DIR, str(uuid.uuid4()))
        x.convert(this_should_not_exist, "this_should_not_exist")

    def test_path_missing(self):
        x = pstruct.types.Path(True)
        this_should_not_exist = os.path.join(TEST_DIR, str(uuid.uuid4()))
        try:
            x.convert(this_should_not_exist, "this_should_not_exist")
        except pstruct.exceptions.BadFilePath:
            # except RuntimeError:

            exc_type, value, traceback = sys.exc_info()
            print("Caught {}: {}".format(exc_type.__name__, value))


if __name__ == "__main__":
    unittest.main()
