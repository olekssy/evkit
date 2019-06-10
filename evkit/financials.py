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

from evkit import urldata


class IncomeStatement:
    # unique ID of YahooFinance url
    fin_statement_url_id = '/financials?p='  # Income statement
    # positional index of values in html
    revenue_id = 6
    cogs_id = 11
    opex_id = 42
    ebit_id = 47
    interest_id = 63
    tax_id = 73

    def __init__(self, ticker):
        self.ticker = ticker
        self.html = None
        self.revenue = []
        self.cogs = []
        self.opex = []
        self.ebit = []
        self.interest = []
        self.tax = []
        self.tax_rate = None

    @staticmethod
    def write_to_list(html, element_list, element_id):
        """
        Write clean data from html to object attribute
        :param html:
        :param element_list:
        :param element_id:
        :return:
        """
        offset = 4
        for i_ in range(element_id, element_id + offset):
            value = urldata.get_value(html, i_)
            element_list.append(value)
        element_list.reverse()

    @staticmethod
    def st_growth(element_list):
        """
        Calculate short-term growth rate
        :param element_list:
        :return:
        """
        n = len(element_list) - 1
        change_list = [element_list[i + 1] / element_list[i] - 1 for i in range(n)]
        rate = sum(change_list) / n
        return rate

    def get_html_data(self):
        self.html = urldata.get_html(ticker=self.ticker,
                                     url_symbol=self.fin_statement_url_id,
                                     YahooFinance=True,
                                     verbose=False
                                     )

    def revenue_ratio(self):
        pass

    def actual_statement(self):
        """
        Write actual data to pro-forma statement
        :return:
        """
        # revenue
        self.write_to_list(self.html,
                           self.revenue,
                           self.revenue_id
                           )
        # cogs
        self.write_to_list(self.html,
                           self.cogs,
                           self.cogs_id
                           )
        # opex
        self.write_to_list(self.html,
                           self.opex,
                           self.opex_id
                           )
        # EBIT
        self.write_to_list(self.html,
                           self.ebit,
                           self.ebit_id
                           )
        # interest expense
        # NOTE: negative values
        self.write_to_list(self.html,
                           self.interest,
                           self.interest_id
                           )
        # tax
        self.write_to_list(self.html,
                           self.tax,
                           self.tax_id
                           )

    def get_tax_rate(self):
        t_rates = np.array(self.tax) / np.array(self.ebit)
        self.tax_rate = np.mean(t_rates)
        return self.tax_rate

    def forecast_statement(self):
        revenue_growth = self.st_growth(self.revenue)
        t = 3
        for i in range(t):
            revenue_t = self.revenue[-1] * (1 + revenue_growth)
            self.revenue.append(revenue_t)


class BalanceSheet(IncomeStatement):
    # unique ID of YahooFinance url
    fin_statement_url_id = '/balance-sheet?p='
    # positional index of values in html
    cash_id = 7
    current_assets_id = 32
    total_assets_id = 72
    current_liabilities_id = 93
    lt_debt_id = 98
    equity_id = 169

    def __init__(self, ticker):
        super().__init__(ticker)
        self.cash = []
        self.current_assets = []
        self.total_assets = []
        self.current_liabilities = []
        self.lt_debt = []
        self.equity = []

    def actual_statement(self):
        """
        Write actual data to pro-forma statement
        :return:
        """
        # cash and equivalents
        self.write_to_list(self.html,
                           self.cash,
                           self.cash_id
                           )
        # current assets
        self.write_to_list(self.html,
                           self.current_assets,
                           self.current_assets_id
                           )
        # total assets
        self.write_to_list(self.html,
                           self.total_assets,
                           self.total_assets_id
                           )
        # current liabilities
        self.write_to_list(self.html,
                           self.current_liabilities,
                           self.current_liabilities_id
                           )
        # long-term debt
        self.write_to_list(self.html,
                           self.lt_debt,
                           self.lt_debt_id
                           )
        # Total Stockholder Equity
        self.write_to_list(self.html,
                           self.equity,
                           self.equity_id
                           )


class CashFlowStatement(IncomeStatement):
    # unique ID of YahooFinance url
    fin_statement_url_id = '/cash-flow?p='
    # positional index of values in html
    depreciation_id = 12
    capex_id = 48

    def __init__(self, ticker):
        super().__init__(ticker)
        self.depreciation = []
        self.capex = []

    def actual_statement(self):
        """
        Write actual data to pro-forma statement
        :return:
        """
        # depreciation
        self.write_to_list(self.html,
                           self.depreciation,
                           self.depreciation_id
                           )
        # capex
        # NOTE: negative values
        self.write_to_list(self.html,
                           self.capex,
                           self.capex_id
                           )


def main():
    stock = 'GOOG'

    # test instances
    print('\n==IS test==')
    is_test = IncomeStatement(stock)
    is_test.get_html_data()
    is_test.actual_statement()
    is_test.forecast_statement()
    print('Revenue', is_test.revenue)
    print('COGS', is_test.cogs)
    print('OPEX', is_test.opex)
    print('EBIT', is_test.ebit)
    print('Interest', is_test.interest)
    print('Tax', is_test.tax)

    print('\n==BS test==')
    bs_test = BalanceSheet(stock)
    bs_test.get_html_data()
    bs_test.actual_statement()
    print('Cash', bs_test.cash)
    print('Current assets', bs_test.current_assets)
    print('Total Assets', bs_test.total_assets)
    print('Current liabilities', bs_test.current_liabilities)
    print('LT debt', bs_test.lt_debt)
    print('Equity', bs_test.equity)

    print('\n==CFS test==')
    cfs_test = CashFlowStatement(stock)
    cfs_test.get_html_data()
    cfs_test.actual_statement()
    print('Depreciation', cfs_test.depreciation)
    print('CAPEX', cfs_test.capex)


if __name__ == '__main__':
    main()
