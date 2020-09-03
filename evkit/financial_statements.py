""" Script for downloading company filings from the SEC EDGAR database. """

import pandas as pd
import utils


# Load configs
configs = utils.load_configs()


# -------------------- Assumptions --------------------
ticker = "AAPL"
verbose = configs["general"]["verbose"]
separator = "	"


# -------------------- Downloader Settings --------------------



def main():
    # scrap_sec_fillings(ticker)
    pathData = configs["pathInternal"]["data"] + "2020q2/num.txt"
    df = pd.read_csv(pathData, sep=separator, low_memory=False)
    print(df)


if __name__ == "__main__":
    main()
