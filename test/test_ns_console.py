import unittest
from unittest.mock import patch

from ns_console import *


class NsConsoleTestCase(unittest.TestCase):

    @patch("builtins.input")
    def test_call_user_input(self, mock_input):
        # All of the input before the last one are illegal, so the final return value must be the last one
        mock_input.side_effect = ["", "OK"]
        self.assertEqual(call_user_input(), "OK")

        mock_input.side_effect = ["not_number", "22", "OK"]
        self.assertEqual(call_user_input(default_value="9", pattern=r"[A-Z]*"), "OK")

        mock_input.side_effect = [""]
        self.assertEqual(call_user_input(default_value="OK"), "OK")

    @patch("getpass.getpass")
    def test_call_user_input_password(self, mock_input):
        mock_input.side_effect = ["", "OK"]
        self.assertEqual(call_user_input_password(), "OK")

        mock_input.side_effect = [""]
        self.assertEqual(call_user_input_password(allow_empty=True), "")

    @patch("builtins.input")
    def test_call_user_choose_number(self, mock_input):
        mock_input.side_effect = ["", "string", "-1", "100"]
        self.assertEqual(call_user_choose_number(), 100)

        mock_input.side_effect = ["0", "99", "10"]
        self.assertEqual(call_user_choose_number(from_num=1, to_num=10), 10)

        mock_input.side_effect = [""]
        self.assertEqual(call_user_choose_number(default_value=123), 123)

    @patch("builtins.input")
    def test_call_user_choose_from_list(self, mock_input):
        data = ["apple", "boy", "cat", "dog"]

        mock_input.side_effect = ["", "0", "-1", "5", "3"]
        self.assertEqual(call_user_choose_from_list(data), "cat")

        mock_input.side_effect = [""]
        self.assertEqual(call_user_choose_from_list(data, default_value=2), "boy")
