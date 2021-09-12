import unittest

from ns_codec import *


# noinspection SpellCheckingInspection
class NsCodecTestCase(unittest.TestCase):

    def test_base64_encode(self):
        self.assertEqual(base64_encode("ABCDEFG"), "QUJDREVGRw==")

    def test_base64_decode(self):
        self.assertEqual(base64_decode("QUJDREVGRw=="), "ABCDEFG")
