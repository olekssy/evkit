

import sys
import unittest

sys.path.append('./')

from evkit import utils

class TestConfigs(unittest.TestCase):
    """
    Configuration file tests
    """
    def setUp(self):
        self.configs = utils.load_configs()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
    
    def test_general(self):
        self.assertIsInstance(self.configs["general"]["verbose"], bool)
    
    def test_repo(self):
        self.assertEqual(
            first=self.configs["pathInternal"]["data"],
            second="data/"
        )
        self.assertEqual(
            first=self.configs["pathInternal"]["docs"],
            second="docs/"
        )
        self.assertEqual(
            first=self.configs["pathInternal"]["media"],
            second="media/"
        )
        self.assertEqual(
            first=self.configs["pathInternal"]["models"],
            second="models/"
        )
        self.assertEqual(
            first=self.configs["pathInternal"]["notebooks"],
            second="notebooks/"
        )
        self.assertEqual(
            first=self.configs["pathInternal"]["reports"],
            second="reports/"
        )
        self.assertEqual(
            first=self.configs["pathInternal"]["tests"],
            second="tests/"
        )

    def test_SEC(self):
        for year in self.configs["pathExternal"]["SEC"].keys():
            self.assertIn(
                member=year,
                container={
                    "FY2020",
                    "FY2019",
                    "FY2018",
                    "FY2017",
                    "FY2016",
                    "FY2015",
                    "FY2014",
                    "FY2013",
                    "FY2012",
                    "FY2011",
                    "FY2010",
                    "FY2009"
                }
            )
            self.assertIsInstance(year, str)
            for quarter in self.configs["pathExternal"]["SEC"][year]:
                self.assertIn(
                    member=quarter,
                    container={
                        "Q1",
                        "Q2",
                        "Q3",
                        "Q4"
                    }
                )
                self.assertIsInstance(quarter, str)



if __name__ == '__main__':
    unittest.main()