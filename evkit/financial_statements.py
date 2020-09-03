""" Script for downloading company filings from the SEC EDGAR database. """

import json
import pandas as pd


# Load configs
with open("evkit/settings.json", "r") as configFile:
    config = json.load(configFile)


# -------------------- Assumptions --------------------
ticker = "AAPL"
verbose = config["general"]["verbose"]
separator = "	"


# -------------------- Downloader Settings --------------------



def main():
    # scrap_sec_fillings(ticker)
    pathData = config["path"]["data"] + "2020q2/num.txt"
    df = pd.read_csv(pathData, sep=separator)
    print(df.head())


if __name__ == "__main__":
    main()
