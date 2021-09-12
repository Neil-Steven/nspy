import unittest

from ns_datetime import *


class NsDatetimeTestCase(unittest.TestCase):
    date = "2021-07-20 11:54:33.450000"
    timestamp = 1626753273450

    def test_date_to_timestamp(self):
        self.assertEqual(date_to_timestamp(self.date, "%Y-%m-%d %H:%M:%S.%f"), self.timestamp)

    def test_timestamp_to_date(self):
        self.assertEqual(timestamp_to_date(self.timestamp, "%Y-%m-%d %H:%M:%S.%f"), self.date)

    def test_get_current_time(self):
        # Trust
        pass

    def test_get_current_timestamp(self):
        # Trust
        pass
