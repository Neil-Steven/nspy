import unittest

from ns_unit import *


class NsUnitTestCase(unittest.TestCase):

    def test_humanize_file_size(self):
        test_auto = humanize_file_size(32568)
        self.assertEqual(test_auto, "32.568 KB")

        test = humanize_file_size(32568, "KB", digit=2)
        self.assertEqual(test, "32.57 KB")
        test = humanize_file_size(32568, "KiB", digit=4)
        self.assertEqual(test, "31.8047 KiB")
        test = humanize_file_size(32568, "MB", digit=5)
        self.assertEqual(test, "0.03257 MB")
        test = humanize_file_size(32568, "MiB", digit=6)
        self.assertEqual(test, "0.031059 MiB")

        test_add_blank = humanize_file_size(1, digit=None, add_blank=False)
        self.assertEqual(test_add_blank, "1B")

    def test_parse_humanized_file_size(self):
        with self.assertRaises(ValueError):
            parse_humanized_file_size("aaaK")
        with self.assertRaises(ValueError):
            parse_humanized_file_size("123ABC")

        test = parse_humanized_file_size("0 GB")
        self.assertEqual(test, 0)
        test = parse_humanized_file_size("1.23456   TB")
        self.assertEqual(test, 1234560000000)
        test = parse_humanized_file_size("1.23456TiB")
        self.assertEqual(test, 1357413075187)
