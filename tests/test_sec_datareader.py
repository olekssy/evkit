import unittest

import pandas as pd

from evkit import sec_datareader


class TestFinancialDataSEC(unittest.TestCase):
    """
    Tests for SEC Financial Statement Data Sets downloader.
    """
    def setUp(self):
        self.findata = sec_datareader.FinancialDataSEC()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_download(self):
        self.assertIsNone(self.findata.download())

    def test_extract(self):
        self.assertIsNone(self.findata.extract())

    def test_parse_index(self):
        self.assertIsInstance(self.findata.parse_index(), (pd.DataFrame, ))

    def test_parse_findata(self):
        self.assertIsInstance(self.findata.parse_findata(), (pd.DataFrame, ))

    def test_cleanup(self):
        self.assertIsNone(self.findata.cleanup())


if __name__ == '__main__':
    unittest.main()
