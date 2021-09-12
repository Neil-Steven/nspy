import unittest

from ns_number import *


class NsNumberTestCase(unittest.TestCase):

    def test_plural(self):
        try:
            # Trust inspect module and don't test it
            import inspect
        except ImportError:
            self.assertEqual(plural(0, "file"), "0 files")
            self.assertEqual(plural(1, "file"), "1 file")
            self.assertEqual(plural(5, "file"), "5 files")

            self.assertEqual(plural(2, "bus"), "2 buses")
            self.assertEqual(plural(5, "box"), "5 boxes")
            self.assertEqual(plural(7, "flash"), "7 flashes")
            self.assertEqual(plural(9, "match"), "9 matches")
            self.assertEqual(plural(0, "man"), "0 men")
