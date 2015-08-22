import unittest

from common.utils import to_str


class UtilsTestCase(unittest.TestCase):

    def test_to_str(self):
        b = bytes([1, 2, 3])
        s = to_str(b)
        self.assertIsInstance(s, str)

        some_str = 'hellp'
        s = to_str(some_str)
        self.assertIsInstance(s, str)
