""" Script for downloading company filings from the SEC EDGAR database. """

import json
import pandas as pd
import sec_edgar_downloader


# Load configs
with open("equity_ai/config.json", "r") as configFile:
    config = json.load(configFile)


# -------------------- Assumptions --------------------
ticker = "AAPL"
verbose = config["global"]["verbose"]
separatorFS = "	"


# -------------------- Scrapper Settings --------------------
def scrap_sec_fillings(ticker, verbose=verbose):
    """ Retrieve SEC fillings for a ticker """
    if verbose:
        print(f'Started scrapping {config["scrapper"]["formType"]} fillings for {ticker}')
    # initialize scrapper
    scrapper = sec_edgar_downloader.Downloader(
        download_folder=config["path"]["data"]
    )
    # collect fillings
    scrapper.get(
        filing_type=config["scrapper"]["formType"],
        ticker_or_cik=ticker,
        num_filings_to_download=config["scrapper"]["numberDownload"]
    )


def main():
    # scrap_sec_fillings(ticker)
    pathFS = "data/2020q2/num.txt"
    df = pd.read_csv(pathFS, sep=separatorFS)
    print(df.head())


if __name__ == "__main__":
    main()