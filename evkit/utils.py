#  MIT License
#
#  Copyright (c) 2019 Oleksii Lialka
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def get_html(ticker, url_id, YahooFinance=True, show_page=False):
    if YahooFinance:
        url = ticker.join(['https://finance.yahoo.com/quote/', url_id, ''])
    else:
        # treat url_symbol as url link
        url = url_id
    source = requests.get(url).text
    html_page = BeautifulSoup(source, 'html5lib')
    data = html_page.findAll('td')
    # display structured html page
    if show_page:
        title = html_page.title.text
        print(f'\n==Raw data of {title}==')
        for num, line in enumerate(data):
            print(num, line.text)
    return data


def get_value(html_page, value_index):
    try:
        value_text = html_page[value_index].text
        value_str = value_text.replace(',', '')
        if value_str == 'N/A':
            value_float = None
        elif value_str == '-':
            value_float = 0
        elif not value_str.replace('.', '').replace('-', '').isdigit():
            # some tickers have broken index,
            # long text value passes all checks and blows the float value up
            value_float = None
        else:
            value_float = float(value_str)
    except IndexError:
        value_float = None
    return value_float


def get_tickers_url():
    tickers_dict = {
        'mega_cap': 'fa45388d-9752-4201-974f-93c0fffdaf2e',
        'large_cap': 'fd702086-e634-4b39-81e8-3326f43373f6',
        'basic_materials': 'b7a89332-49c1-4c36-aa21-0e5dea8c0a4e',
        'healthcare': 'b5bd835a-1f78-4dd3-a22d-14a97f62e2c4',
        'utilities': 'cea6e52c-0be5-4600-a302-c737e9b7f274',
        'financial_services': 'f48ad0e4-430a-41b5-b42d-9b84ded67143',
        'consumer_defensive': '27c9d45d-6ae9-4404-9c29-977dc249b8fe',
        'consumer_cyclical': '2e4f67d2-c4f2-4e6e-9a88-99084a489809h',
        'technology': '8f642d7d-11b7-435a-aa30-b1570a7d9d26',
        'energy': '238a84a7-d96d-4b87-a1b9-090191c412e3',
        'real_estate': '33d68532-22eb-4ca5-aaab-a2c4e45e6337',
        'communication_services': '17bcd658-1187-431d-8dbb-38d4967e1981',
        'industrials': '64550c05-f55d-4620-9f5d-95143b31e9ed'
    }
    # display available stock pools
    print(f'ID | Industry')
    for num, key in enumerate(tickers_dict.keys()):
        print(f'{num:>2d} | {key}')
    select = input('Enter Industry ID: ')
    # render selection (int) into dict key
    tickers_key = list(tickers_dict.keys())[int(select)]
    print(f'Selected collection of securities: {tickers_key}')
    # collect urls with page offset
    url_offset = 0
    tickers_urls = []
    tickers_url_id = [
        'https://finance.yahoo.com/screener/unsaved/',
        '?count=250&offset='
    ]
    for i in range(6):
        url = tickers_dict[tickers_key].join(tickers_url_id) + str(url_offset)
        tickers_urls.append(url)
        url_offset += 250
        # print(url)
    return tickers_key, tickers_urls


def get_rf_mrp():
    # vars
    summary_url_id = '?p='
    rf_ticker = '^TNX'  # Treasury Yield 10 Years
    market_url = 'http://news.morningstar.com/index/indexReturn.html'
    rf_id = 1
    market_id = 43  # 1Y US market return value id

    # get risk-free rate
    rf_html = get_html(
        ticker=rf_ticker,
        url_id=summary_url_id,
        YahooFinance=True,
        show_page=False
    )
    rf = get_value(rf_html, rf_id) / 100
    # get market return
    market_html = get_html(
        ticker=None,
        url_id=market_url,
        YahooFinance=False,
        show_page=False
    )
    mkt_return = get_value(market_html, market_id) / 100
    # market risk pemium
    mrp = mkt_return - rf
    return rf, mrp


def get_tickers(url_list):
    collection = {'ticker': [],
                  'name': []
                  }
    # open urls from the offset collection
    for url in url_list:
        html_page = get_html(
            ticker=None,
            url_id=url,
            YahooFinance=False,
            show_page=False
        )
        data_len = len(html_page)
        value_indices = np.arange(
            start=0,
            stop=data_len,
            step=10
        )
        # extract data, write to dictionary collection
        for i in value_indices:
            ticker = html_page[i].text
            company_name = html_page[i + 1].text
            # avoid duplicates
            if company_name in collection['name']:
                continue
            else:
                collection['ticker'].append(ticker)
                collection['name'].append(company_name)
    # render dictionary into DataFrame
    stocks_df = pd.DataFrame(collection)
    return stocks_df


def plot_beta_wacc(beta, wacc):
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 5))
    n = len(wacc)
    plt.scatter(x=beta,
                y=wacc,
                edgecolor='black',
                linewidth=1,
                alpha=0.75
                )
    plt.title('Asset beta - WACC \nN = ' + str(n))
    plt.xlabel('Asset beta')
    plt.ylabel('WACC')
    plt.tight_layout()
    plt.show()


def plot_dcf_mkt_price(dcf_price, mkt_price):
    plt.style.use('seaborn')
    plt.figure(figsize=(10, 5))
    n = len(dcf_price)
    # plt.plot(
    #     dcf_price,
    #     linewidth=1,
    # )
    # plt.plot(
    #     mkt_price,
    #     linewidth=1,
    #     alpha=0.75
    # )
    plt.scatter(
        x=mkt_price,
        y=dcf_price / mkt_price,
        linewidth=1,
        alpha=0.75
    )
    plt.xscale('log')
    # plt.yscale('log')
    plt.title('DCF-WACC stock price to market quote \nN = ' + str(n))
    plt.xlabel('DCF-WACC / Market quote')
    plt.ylabel('Market quote')
    plt.tight_layout()
    plt.show()


def get_shares_num(html_page, value_index):
    try:
        value_text = html_page[value_index].text
        value_str = value_text.replace(',', '')
    except IndexError:
        value_text = 'IndexError'
        value_str = 'N/A'
    if value_str == 'N/A':
        value_float = None
    elif value_str[-1] == 'B':
        value_float = float(value_str[:-1]) * 1_000_000
    elif value_str[-1] == 'M':
        value_float = float(value_str[:-1]) * 1_000
    elif value_str[-1] == 'k':
        value_float = float(value_str[:-1])
    else:
        raise Exception(f'Error: unknown scale of shares outstanding. '
                        f'raw value = {value_text}')
    return value_float


def results_to_csv(data_df, report_id):
    # save results to csv
    path = report_id.join(['./reports/', '.csv'])
    data_df.to_csv(
        path_or_buf=path,
        index=False
    )
    print(f'\n-> Results saved to a file {path}')
    return None


def main():
    ticker = 'AMZN'
    display_results = True

    # unique ID of YahooFinance urlcurrent_assets_id
    summary_url_id = '?p='
    income_statement_url_id = '/financials?p='
    balance_sheet_url_id = '/balance-sheet?p='
    cf_statement_url_id = '/cash-flow?p='
    statistics_url_id = '/key-statistics?p='

    # test html getter
    get_html(
        ticker=ticker,
        url_id=summary_url_id,
        show_page=display_results
    )
    get_html(
        ticker=ticker,
        url_id=income_statement_url_id,
        show_page=display_results
    )
    get_html(
        ticker=ticker,
        url_id=balance_sheet_url_id,
        show_page=display_results
    )
    get_html(
        ticker=ticker,
        url_id=cf_statement_url_id,
        show_page=display_results
    )
    get_html(
        ticker=ticker,
        url_id=statistics_url_id,
        show_page=display_results
    )
    # get_tickers_url()


if __name__ == '__main__':
    main()
