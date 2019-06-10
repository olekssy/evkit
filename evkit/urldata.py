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

import requests
from bs4 import BeautifulSoup


def get_html(ticker, url_symbol, YahooFinance=True, verbose=False):
    if YahooFinance:
        url = ticker.join(['https://finance.yahoo.com/quote/', url_symbol, ''])
    else:
        url = url_symbol
    source = requests.get(url).text
    html_page = BeautifulSoup(source, 'html5lib')
    data = html_page.findAll('td')

    if verbose:
        title = html_page.title.text
        print(f'\n==Raw data of {title}==')
        for num, line in enumerate(data):
            print(num, line.text)
    return data


def get_value(data, value_index, verbose=False):
    value_text = data[value_index].text
    value_str = value_text.replace(',', '')
    value_float = float(value_str)

    if verbose:
        print('\n==Verbose mode of data.get_value==')
        print(f'value_text = {value_text} {type(value_text)}\n'
              f'value_str = {value_str} {type(value_str)}\n'
              f'value_float = {value_float} {type(value_float)}\n')
    return value_float


def main():
    stock = 'GOOG'
    verbose = True

    # unique ID of YahooFinance urlcurrent_assets_id
    summary_url_id = '?p='
    income_statement_url_id = '/financials?p='
    balance_sheet_url_id = '/balance-sheet?p='
    cf_statement_url_id = '/cash-flow?p='

    # other sources
    index_return_url = 'http://news.morningstar.com/index/indexReturn.html'

    # test html getter
    summary_html = get_html(stock, summary_url_id, verbose=verbose)
    income_statement_html = get_html(stock, income_statement_url_id, verbose=verbose)
    balance_sheet_html = get_html(stock, balance_sheet_url_id, verbose=verbose)
    cf_statement_html = get_html(stock, cf_statement_url_id, verbose=verbose)

    # test value getter


if __name__ == '__main__':
    main()
