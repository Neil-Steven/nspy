import unittest

from ns_regex import *


class NsRegexTestCase(unittest.TestCase):

    def test_is_match(self):
        self.assertTrue(is_match(r"\.tar\.gz", ".tar.gz"))
        self.assertTrue(is_match(r"he\S*o", "hello world"))
        self.assertFalse(is_match(r"wo\S*d", "hello world"))
        self.assertFalse(is_match(r"hello", "hello world", full_match=True))
        self.assertTrue(is_match(r"H[a-z]LLo", "hello world", ignore_case=True))

    def test_match(self):
        self.assertEqual(match(r"H[a-z]*", "hello world", ignore_case=True), "hello")

    def test_contains(self):
        self.assertTrue(contains(r"\.tar\.gz", ".tar.gz"))
        self.assertTrue(is_match(r"he\S*o", "hello world"))
        self.assertTrue(contains(r"wo\S*d", "hello world"))
        self.assertTrue(contains(r"W[a-z]rLD", "hello world", ignore_case=True))

    def test_search(self):
        self.assertEqual(search(r"G[a-z]*", "I am a good man", ignore_case=True), "good")
