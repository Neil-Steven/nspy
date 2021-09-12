import unittest
from pathlib import Path

from ns_path import *


class NsPathTestCase(unittest.TestCase):

    def test_list_dir(self):
        # Equals regardless of the order
        test = list_dir("C:\\Windows\\", "System*")
        self.assertCountEqual(test, ["SystemResources", "SystemApps", "System", "system.ini", "System32"])

        # Equals exactly
        test = list_dir("C:\\Windows\\", "System*", absolute_path=True, sort=True)
        self.assertEqual(test, ["C:\\Windows\\System",
                                "C:\\Windows\\System32",
                                "C:\\Windows\\SystemApps",
                                "C:\\Windows\\SystemResources",
                                "C:\\Windows\\system.ini"])

        not_exist = list_dir("not_exist_path")
        self.assertEqual(not_exist, [])

    def test_get_suffix(self):
        test = get_suffix("C:\\Windows\\explorer.exe")
        self.assertEqual(test, ".exe")
        test = get_suffix("C:\\Windows\\explorer.exe", with_point=False)
        self.assertEqual(test, "exe")

        multi_suffix = get_suffix("test.tar.gz")
        self.assertEqual(multi_suffix, ".tar.gz")
        multi_suffix = get_suffix("test.tar.gz", full=False, with_point=False)
        self.assertEqual(multi_suffix, "gz")

        no_suffix = get_suffix("no_suffix")
        self.assertEqual(no_suffix, "")
        no_suffix = get_suffix("no_suffix", full=False, with_point=False)
        self.assertEqual(no_suffix, "")

    def test_is_file_like(self):
        self.assertFalse(is_file_like("C:\\"))
        self.assertFalse(is_file_like("C:\\not_exit_dir"))
        self.assertFalse(is_file_like("C:\\Program Files"))

        self.assertTrue(is_file_like("C:\\not_exist_file.txt"))
        self.assertTrue(is_file_like("C:\\Windows\\system.ini"))

    def test_is_dir_like(self):
        self.assertTrue(is_dir_like("C:\\"))
        self.assertTrue(is_dir_like("C:\\not_exit_dir"))
        self.assertTrue(is_dir_like("C:\\Program Files"))

        self.assertFalse(is_dir_like("C:\\not_exist_file.txt"))
        self.assertFalse(is_dir_like("C:\\Windows\\system.ini"))

    def test_to_path(self):
        test_str = to_path("C:\\Windows")
        self.assertIsInstance(test_str, Path)

        path = Path("C:\\Windows")
        test_path = to_path(path)
        self.assertEqual(path, test_path)

    def test_to_multi_path(self):
        test = to_multi_path(["C:\\Windows", Path("C:\\Program Files")])
        for t in test:
            self.assertIsInstance(t, Path)
