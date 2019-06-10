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

"""
Algorithm
1/ extract web data, clean, write actual financials to object attributes
2/ get ST growth rate, effective tax rate
3/ get revenue ratios for CF elements
->4/ forecast CF: revenue, EBIT, debt from constant D/E
5/ get NWC projections
6/ get terminal value
7/ DCF-WACC
"""

import numpy as np

from evkit import utils


class IncomeStatement:
    # unique ID of YahooFinance url
    fin_statement_url_id = '/financials?p='  # Income statement
    # positional index of values in html
    revenue_id = 6
    ebit_id = 47
    interest_id = 63
    tax_id = 73

    def __init__(self, ticker):
        self.ticker = ticker
        self.html = None
        self.revenue = []
        self.ebit = []
        self.interest = []
        self.tax = []

    @staticmethod
    def write_to_list(html, element_list, element_id):
        """
        Write clean data from html to object attribute
        :param html:
        :param element_list:
        :param element_id:
        :return:implied_rate
        """
        offset = 4
        for i_ in range(element_id, element_id + offset):
            value = utils.get_value(html, i_)
            element_list.append(value)
        element_list.reverse()

    @staticmethod
    def get_st_growth(element_list):
        """
        Calculate short-term growth rate
        :param element_list:
        :return:
        """
        n = len(element_list) - 1
        change_list = [element_list[i + 1] / element_list[i] - 1 for i in range(n)]
        st_growth = sum(change_list) / n
        return st_growth

    def get_html_data(self):
        self.html = utils.get_html(ticker=self.ticker,
                                   url_symbol=self.fin_statement_url_id,
                                   YahooFinance=True,
                                   verbose=False
                                   )

    def get_tax_rate(self):
        t_rates = np.array(self.tax[:4]) / np.array(self.ebit[:4])
        tax_rate = np.mean(t_rates)
        return tax_rate

    def get_revenue_ratio(self, elements_list):
        # element/revenue from actual results
        ratio_list = np.array(elements_list[:4]) / np.array(self.revenue[:4])
        ratio = np.mean(ratio_list)
        return ratio

    def get_projections(self, elements_list, periods, growth_rate=None, ratio=True):
        if ratio:
            # get projections for IS elements
            for revenue_t in self.revenue[4:]:
                ratio = self.get_revenue_ratio(elements_list)
                element_t = revenue_t * ratio
                elements_list.append(element_t)
        else:
            # get projections for revenue, BS, CFS elements
            for t in range(periods):
                last_element = elements_list[-1]
                element_t = last_element * (1 + growth_rate)
                elements_list.append(element_t)
        return elements_list

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

    def forecast_statement(self, st_growth, periods=3):
        # forecast elements
        # revenue
        self.get_projections(elements_list=self.revenue,
                             periods=periods,
                             growth_rate=st_growth,
                             ratio=False
                             )
        # ebit
        self.get_projections(elements_list=self.ebit,
                             periods=periods,
                             )


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
        self.nwc = []

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

    def get_nwc(self):
        # net working capital
        wc = np.array(self.current_assets) - np.array(self.current_liabilities)
        records = len(wc)
        self.nwc = [0] + [wc[i + 1] - wc[i] for i in range(records - 1)]
        return self.nwc

    def forecast_statement(self, st_growth, periods=3):
        # forecast elements
        self.get_projections(elements_list=self.current_assets,
                             periods=periods,
                             growth_rate=st_growth,
                             ratio=False
                             )
        self.get_projections(elements_list=self.current_liabilities,
                             periods=periods,
                             growth_rate=st_growth,
                             ratio=False
                             )
        self.get_nwc()


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

    def forecast_statement(self, st_growth, periods=3):
        # forecast elements
        dna_growth = self.get_st_growth(self.depreciation)
        self.get_projections(elements_list=self.depreciation,
                             periods=periods,
                             growth_rate=dna_growth,
                             ratio=False
                             )
        capex_growth = self.get_st_growth(self.capex)
        self.get_projections(elements_list=self.capex,
                             periods=periods,
                             growth_rate=capex_growth,
                             ratio=False
                             )


def dcf(ebit, dna, nwc, capex, tax_rate, lt_growth, wacc, dt):
    # FCF = EBIT(1 - tax) + DnA - NWC - CAPEX
    ebit = np.array(ebit)
    dna = np.array(dna)
    nwc = np.array(nwc)
    capex = -np.array(capex)  # adjust negative value
    fcf = ebit * (1 - tax_rate) + dna - nwc - capex
    # terminal value
    tv = fcf[-1] * (1 + lt_growth) / (wacc - lt_growth)
    fcf_tv = np.append(fcf, tv)[4:]
    # discount forecasted fcf
    ev = np.dot(fcf_tv, dt)
    return fcf_tv, ev


def main():
    pass


if __name__ == '__main__':
    main()
