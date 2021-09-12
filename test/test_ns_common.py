import unittest

from ns_common import *


class NsCommonTestCase(unittest.TestCase):

    def test_is_basic_type(self):
        self.assertTrue(is_basic_type(1))
        self.assertTrue(is_basic_type(2.3))
        self.assertTrue(is_basic_type(True))
        self.assertTrue(is_basic_type(12 + 0.2j))
        self.assertFalse(is_basic_type(None))
        self.assertFalse(is_basic_type("Yes"))

    def test_is_empty(self):
        self.assertFalse(is_empty(1))
        self.assertFalse(is_empty(2.3))
        self.assertFalse(is_empty(True))
        self.assertFalse(is_empty(12 + 0.2j))

        self.assertTrue(is_empty(None))
        self.assertFalse(is_empty("Yes"))
        self.assertTrue(is_empty(""))
        self.assertTrue(is_empty("        "))

        self.assertTrue(is_empty([]))
        self.assertTrue(is_empty({}))
        self.assertTrue(is_empty(()))
        self.assertTrue(is_empty(set()))
        self.assertFalse(is_empty([1, 2]))
        self.assertFalse(is_empty({1: 2}))
        self.assertFalse(is_empty((1, 2)))
        self.assertFalse(is_empty({1, 2}))
