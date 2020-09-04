""" Script for downloading company filings from the SEC database. """


import os
import zipfile
# import numpy as np
import pandas as pd
import requests

import utils

# -------------------- Global Variables --------------------
config = utils.load_config()


class FinancialDataSEC:
    """
    Class for collecting Financial Statement Data Sets from SEC.
    """
    def __init__(self):
        self.verbose = config["general"]["verbose"]
        self.url = config["dataSource"]["SEC"]
        self.pathData = config["localPath"]["data"]
        self.pathArchives = config["localPath"]["archives"]
        self.pathTemp = config["localPath"]["temp"]

        self.pathIndexSEC = config["localPath"]["SECindex"]
        self.pathFinDataSEC = config["localPath"]["SECdata"]

        self.indexSEC = None
        self.finDataSEC = None

    def download(self):
        """
        Download FSD archives from SEC.
        """
        if self.verbose:
            print("Start downloading FSD archives.")

        for year in self.url.keys():
            # create dir for archives
            if not os.path.exists(self.pathArchives):
                os.mkdir(self.pathArchives)

            for quarter in self.url[year].keys():
                fileName = self.url[year][quarter].split("/")[-1]
                filePath = "".join([self.pathArchives, fileName])
                # download file from SEC database
                archive = requests.get(self.url[year][quarter])
                # save file
                open(filePath, 'wb').write(archive.content)

                if self.verbose:
                    print(f"Downloaded {filePath}")

        if self.verbose:
            print("Complete all downloads.\n")

    def extract(self):
        """
        Extract FSD from archives.
        """
        if self.verbose:
            print("Start extracting FSD archives.")

        if not os.path.exists(self.pathTemp):
            os.mkdir(self.pathTemp)

        for fileName in os.listdir(self.pathArchives):
            # create directory for extracted files
            dirName = fileName.split(".")[0]
            dirPath = "".join([self.pathTemp, dirName])
            if not os.path.exists(dirPath):
                os.mkdir(dirPath)

            archPath = "".join([self.pathArchives, fileName])
            # extract files from archive
            with zipfile.ZipFile(archPath, "r") as zipObj:
                zipObj.extractall(
                    path=dirPath,
                    members=None
                )

                if self.verbose:
                    print(f"Extracted {dirName}")

        if self.verbose:
            print("Complete extracting all archives.\n")

    def parse(self):
        """
        Parse company name and report index to csv.
        """
        if self.verbose:
            print("Start parsing SEC data.")

        for dirName in os.listdir(self.pathTemp):
            # parse company names and report IDs
            filePath = "".join([
                self.pathTemp,
                dirName,
                config["SECconvention"]["nameIndex"]
            ])
            df = pd.read_csv(
                filePath,
                sep=config["SECconvention"]["separator"],
                index_col=config["SECconvention"]["indexColumn"],
                low_memory=False
            )
            self.indexSEC = pd.concat([self.indexSEC, df])

            # parse financial statements
            filePath = "".join([
                self.pathTemp,
                dirName,
                config["SECconvention"]["nameData"]
            ])
            df = pd.read_csv(
                filePath,
                sep=config["SECconvention"]["separator"],
                index_col=config["SECconvention"]["indexColumn"],
                low_memory=False
            )
            self.finDataSEC = pd.concat([self.finDataSEC, df])

            if self.verbose:
                print(f"Parsed {dirName}")

        # save data to csv
        self.indexSEC.to_csv(self.pathIndexSEC)
        self.finDataSEC.to_csv(self.pathFinDataSEC)

        if self.verbose:
            print(f"Parsed index saved to {self.pathIndexSEC}")
            print(f"Parsed data saved to {self.pathFinDataSEC}")
            print("Complete parsing SEC data.")

        return self.indexSEC, self.finDataSEC

    def cleanup(self):
        """
        Remove all archives.
        """
        if self.verbose:
            print("Start cleanup.")

        # remove archives
        if os.path.exists(self.pathArchives):
            for archive in os.listdir(self.pathArchives):
                archivePath = "".join([self.pathArchives, archive])
                os.remove(archivePath)

                if self.verbose:
                    print(f"Removed {archivePath}")

            os.rmdir(self.pathArchives)

        # remove extracted artifacts
        for dir in os.listdir(self.pathData):
            dirPath = "".join([self.pathData, dir])
            for obj in os.listdir(dirPath):
                filePath = "/".join([dirPath, obj])
                os.remove(filePath)

            os.rmdir(dirPath)

            if self.verbose:
                print(f"Removed {dirPath}/")

        if self.verbose:
            print("Complete cleanup.\n")


def main():
    # initialize DataSEC instance
    findata = FinancialDataSEC()

    # Download and extract data
    findata.download()
    findata.extract()

    # Parse collected data
    findata.parse()

    # Cleanup redundant files
    findata.cleanup()
    pass


if __name__ == "__main__":
    main()
