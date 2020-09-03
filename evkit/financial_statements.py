""" Script for downloading company filings from the SEC database. """


import pandas as pd
import requests
import utils
from tqdm import tqdm
import zipfile
import os


# -------------------- Global Variables --------------------
config = utils.load_config()
verbose = config["general"]["verbose"]


# -------------------- Downloader Settings --------------------
class Data:
    """
    Class for collecting Financial Statement Data Sets from SEC.
    """
    def __init__(self):
        self.SEC = config["dataSource"]["SEC"]
        self.pathData = config["localPath"]["data"]
        self.pathArchives = {}
    
    def download(self, verbose=False):
        """
        Download FSD archives from SEC.
        """
        if verbose:
            print("Start downloading FSD archives.")

        for year in self.SEC.keys():
            # create dir for archives
            dirPath = config["localPath"]["archives"]
            if not os.path.exists(dirPath):
                os.mkdir(dirPath)
            for quarter in self.SEC[year].keys():
                fileName = "".join([year, quarter])
                filePath = "".join([dirPath, fileName, ".zip"])
                # download file from SEC database
                archive = requests.get(self.SEC[year][quarter])
                # save file
                open(filePath, 'wb').write(archive.content)
                # write path to file
                self.pathArchives[fileName] = filePath

                if verbose:
                    print(f"Downloaded {filePath}")
        
        if verbose:
            print("Complete all downloads.\n")
    
    def extract(self, verbose=False):
        """
        Extract FSD from archives.
        """
        if verbose:
            print("Start extracting FSD archives.")

        for fileName, filePath in self.pathArchives.items():
            # create directory for extracted files
            dirPath = "".join([config["localPath"]["data"], fileName])
            if not os.path.exists(dirPath):
                os.mkdir(dirPath)
            # extract files from archive
            with zipfile.ZipFile(filePath, "r") as zipObj:
                zipObj.extractall(
                    path=dirPath,
                    members=None
                )

                if verbose:
                    print(f"Extracted {fileName}")
        
        if verbose:
            print(f"Complete extracting all archives.\n")

    def cleanup(self, verbose=False):
        """
        Remove all archives.
        """
        if verbose:
            print(f"Start cleanup.")

        for file in self.pathArchives.values():
            os.remove(file)
            if verbose:
                print(f"Removed {file}")
        
        if verbose:
            print(f"Complete cleanup.\n")

        



def main():
    # scrap_sec_fillings(ticker)
    # pathData = configs["pathInternal"]["data"] + "2020q2/num.txt"
    # df = pd.read_csv(pathData, sep=separator, low_memory=False)
    # print(df)
    findata = Data()
    findata.download(verbose=verbose)
    findata.extract(verbose=verbose)
    findata.cleanup(verbose=verbose)

    pass

if __name__ == "__main__":
    main()
