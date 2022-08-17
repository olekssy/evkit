"""
Module for downloading company filings from
SEC Financial Statement Data Sets.
"""

import os
import shutil
import zipfile

import pandas as pd
import requests


# -------------------- Helper Functions --------------------
def sec_url(period):
    """ Create url link to SEC Financial Statement Data Set """
    url = "".join([
        "https://www.sec.gov/files/dera/data/financial-statement-data-sets/",
        period, ".zip"
    ])

    # handle weird path exception of SEC
    if period == "2020q1":
        url = "".join([
            "https://www.sec.gov/files/node/add/data_distribution/", period,
            ".zip"
        ])
    return url


# -------------------- Global Variables --------------------
CONFIG = {
    "verbose": True,
    "path": {
        "data": "data/",
        "archives": "data/archives/",
        "temp": "data/temp/",
        "index": "data/sec_index.csv",
        "finData": "data/sec_findata.csv",
    },
    "dataSource": {
        # sec_url("2020q2"),
        # sec_url("2020q1"),
        sec_url("2019q4"),
        sec_url("2019q3"),
        sec_url("2019q2"),
        sec_url("2019q1"),
    },
    "convention": {
        "separator": "\t",
        "indexColumn": "adsh",
        "fileIndex": "/sub.txt",
        "fileData": "/num.txt"
    }
}


# -------------------- Downloader Settings --------------------
class FinancialDataSEC:
    """
    Class for collecting Financial Statement Data Sets from SEC.
    """

    def __init__(self):
        self.verbose = CONFIG["verbose"]
        self.source = CONFIG["dataSource"]
        self.data = CONFIG["path"]["data"]
        self.archives = CONFIG["path"]["archives"]
        self.temp = CONFIG["path"]["temp"]

        self.indexFile = CONFIG["path"]["index"]
        self.finDataFile = CONFIG["path"]["finData"]

        self.index = None
        self.finData = None

        # mkdir data/ if not exists
        if not os.path.exists(self.data):
            os.mkdir(self.data)

    def download(self):
        """
        Download Financial Statement Data Sets archives from SEC.
        """
        if self.verbose:
            print("Start downloading from SEC.")

        for url in self.source:
            # mkdir archives/ if not exists
            if not os.path.exists(self.archives):
                os.mkdir(self.archives)

            # download file from SEC database
            fileName = url.split("/")[-1]
            filePath = "".join([self.archives, fileName])
            archive = requests.get(url)

            # save file
            open(filePath, 'wb').write(archive.content)

            if self.verbose:
                print(f"Downloaded {filePath}")

        if self.verbose:
            print("Complete all downloads.\n")

    def extract(self):
        """
        Extract data from SEC archives.
        """
        if self.verbose:
            print("Start extracting SEC archives.")

        if not os.path.exists(self.temp):
            os.mkdir(self.temp)

        for fileName in os.listdir(self.archives):
            # create directory for extracted files
            dirName = fileName.split(".")[0]
            dirPath = "".join([self.temp, dirName])
            if not os.path.exists(dirPath):
                os.mkdir(dirPath)

            # extract files from archive
            archPath = "".join([self.archives, fileName])
            with zipfile.ZipFile(archPath, "r") as archive:
                archive.extractall(path=dirPath, members=None)

                if self.verbose:
                    print(f"Extracted {dirName}")

        if self.verbose:
            print("Complete extracting all archives.\n")

    def parse_index(self, to_csv=True):
        """
        Parse company name and report index to csv.
        """
        if self.verbose:
            print("Start parsing SEC index data.")

        for dirName in os.listdir(self.temp):
            # parse company names and report IDs
            filePath = "".join(
                [self.temp, dirName, CONFIG["convention"]["fileIndex"]])
            df = pd.read_csv(filePath,
                             sep=CONFIG["convention"]["separator"],
                             index_col=CONFIG["convention"]["indexColumn"],
                             low_memory=False)
            self.index = pd.concat([self.index, df])

            if self.verbose:
                print(f"Parsed {dirName}")

        # save data to csv
        if to_csv:
            self.index.to_csv(self.indexFile)
            print(f"Parsed index saved to {self.indexFile}")

        if self.verbose:
            print("Complete parsing SEC index data.\n")

        return self.index

    def parse_findata(self, to_csv=True):
        """
        Parse financial data to csv.
        """
        if self.verbose:
            print("Start parsing SEC financial data.")

        for dirName in os.listdir(self.temp):
            # parse financial statements
            filePath = "".join(
                [self.temp, dirName, CONFIG["convention"]["fileData"]])
            df = pd.read_csv(filePath,
                             sep=CONFIG["convention"]["separator"],
                             index_col=CONFIG["convention"]["indexColumn"],
                             low_memory=False)
            self.finData = pd.concat([self.finData, df])

            if self.verbose:
                print(f"Parsed {dirName}")

        # save data to csv
        if to_csv:
            self.finData.to_csv(self.finDataFile)
            print(f"Parsed data saved to {self.finDataFile}")

        if self.verbose:
            print("Complete parsing SEC financial data.\n")

        return self.finData

    def cleanup(self):
        """
        Remove archives and extracted artifacts.
        """
        if self.verbose:
            print("Start cleanup.")

        # remove archives
        if os.path.exists(self.archives):
            shutil.rmtree(self.archives)

        # remove extracted artifacts
        if os.path.exists(self.temp):
            shutil.rmtree(self.temp)

        if self.verbose:
            print(f"Removed {self.archives}")
            print(f"Removed {self.temp}")
            print("Complete cleanup.\n")


def main():
    # initialize DataSEC instance
    findata = FinancialDataSEC()

    # Download and extract data
    findata.download()
    findata.extract()

    # Parse collected data
    findata.parse_index()
    findata.parse_findata()

    # Cleanup redundant files
    findata.cleanup()


if __name__ == "__main__":
    main()
