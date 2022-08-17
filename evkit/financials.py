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
4/ forecast CF: revenue, EBIT, debt from constant D/E
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
        self.revenue = np.zeros(4)
        self.ebit = np.zeros(4)
        self.interest = np.zeros(4)
        self.tax = np.zeros(4)

    @staticmethod
    def get_actual(html, element_id):
        """
        Write clean data from html to object attribute
        """
        offset = 4  # nubmer of entries
        element_list = np.zeros(offset)
        for i_ in range(element_id, element_id + offset):
            value = utils.get_value(html, i_)
            # break iteration if None value encountered
            if value is None:
                element_list = np.zeros(4)
                break
            element_list[i_ - element_id] = value
        element_list = np.flip(element_list)
        return element_list

    @staticmethod
    def get_st_growth(element_list):
        """
        Calculate short-term growth rate
        """
        if np.any(element_list):
            n = len(element_list) - 1
            change_list = [
                element_list[i + 1] / element_list[i] - 1 for i in range(n)
            ]
            st_growth = sum(change_list) / n
        else:
            st_growth = 0
        return st_growth

    @staticmethod
    def get_projections(elements_list, periods, growth_rate):
        # get projections
        for t in range(periods):
            last_element = elements_list[-1]
            element_t = last_element * (1 + growth_rate)
            elements_list = np.append(elements_list, element_t)
        return elements_list

    def get_html_data(self):
        self.html = utils.get_html(ticker=self.ticker,
                                   url_id=self.fin_statement_url_id,
                                   YahooFinance=True,
                                   show_page=False)

    def get_tax_rate(self):
        actual_tax = self.tax[:4]
        actual_ebit = self.ebit[:4]
        # check data integrity
        if np.any(actual_tax) and np.any(actual_ebit):
            t_rates = self.tax[:4] / self.ebit[:4]
            tax_rate = np.mean(t_rates)
        else:
            tax_rate = 0.21
        return tax_rate

    def get_revenue_ratio(self, elements_list):
        # element/revenue from actual results
        actual_element = elements_list[:4]
        actual_revenue = self.revenue[:4]
        if np.any(actual_element) and np.any(actual_revenue):
            ratios_np = actual_element / actual_revenue
            ratio = np.mean(ratios_np)
        else:
            ratio = 0
        return ratio

    def actual_statement(self):
        """
        Write actual data to pro-forma statement
        :return:
        """
        # revenue
        self.revenue = self.get_actual(html=self.html,
                                       element_id=self.revenue_id)
        # EBIT
        self.ebit = self.get_actual(html=self.html, element_id=self.ebit_id)
        # interest expense
        # NOTE: negative values
        self.interest = self.get_actual(html=self.html,
                                        element_id=self.interest_id)
        # tax
        self.tax = self.get_actual(html=self.html, element_id=self.tax_id)

    def forecast_statement(self, st_growth, periods=3):
        # forecast elements
        # ebit
        self.ebit = self.get_projections(
            elements_list=self.ebit,
            periods=periods,
            growth_rate=st_growth,
        )


class BalanceSheet(IncomeStatement):
    # unique ID of YahooFinance url
    fin_statement_url_id = '/balance-sheet?p='
    # positional index of values in html
    cash_id = 7
    current_assets_id = 32
    total_assets_id = 72
    current_liabilities_id = 93
    st_debt_id = 83
    lt_debt_id = 98
    equity_id = 169

    def __init__(self, ticker):
        super().__init__(ticker)
        self.cash = np.zeros(4)
        self.current_assets = np.zeros(4)
        self.total_assets = np.zeros(4)
        self.current_liabilities = np.zeros(4)
        self.st_debt = np.zeros(4)
        self.lt_debt = np.zeros(4)
        self.total_debt = np.zeros(4)
        self.equity = np.zeros(4)
        self.nwc = np.zeros(4)

    def actual_statement(self):
        """
        Write actual data to pro-forma statement
        :return:
        """
        # cash and equivalents
        self.cash = self.get_actual(html=self.html, element_id=self.cash_id)
        # current assets
        self.current_assets = self.get_actual(
            html=self.html, element_id=self.current_assets_id)
        # total assets
        self.total_assets = self.get_actual(html=self.html,
                                            element_id=self.total_assets_id)
        # current liabilities
        self.current_liabilities = self.get_actual(
            html=self.html, element_id=self.current_liabilities_id)
        # short-term debt
        self.st_debt = self.get_actual(html=self.html,
                                       element_id=self.st_debt_id)
        # long-term debt
        self.lt_debt = self.get_actual(html=self.html,
                                       element_id=self.lt_debt_id)
        # Total Stockholder Equity
        self.equity = self.get_actual(html=self.html,
                                      element_id=self.equity_id)
        # total debt
        self.total_debt = self.st_debt + self.lt_debt

    def get_nwc(self):
        # net working capital
        wc = self.current_assets - self.current_liabilities
        records = len(wc)
        nwc = [0] + [wc[i + 1] - wc[i] for i in range(records - 1)]
        self.nwc = np.array(nwc)
        return self.nwc

    def forecast_statement(self, st_growth, periods=3):
        # forecast elements
        self.current_assets = self.get_projections(
            elements_list=self.current_assets,
            periods=periods,
            growth_rate=st_growth,
        )
        self.current_liabilities = self.get_projections(
            elements_list=self.current_liabilities,
            periods=periods,
            growth_rate=st_growth,
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
        self.depreciation = np.zeros(4)
        self.capex = np.zeros(4)

    def actual_statement(self):
        """
        Write actual data to pro-forma statement
        :return:
        """
        # depreciation
        self.depreciation = self.get_actual(html=self.html,
                                            element_id=self.depreciation_id)
        # capex
        # NOTE: negative values
        self.capex = self.get_actual(html=self.html, element_id=self.capex_id)

    def forecast_statement(self, st_growth, periods=3):
        # forecast elements
        # dna_growth = self.get_st_growth(self.depreciation)
        self.depreciation = self.get_projections(
            elements_list=self.depreciation,
            periods=periods,
            growth_rate=st_growth,
        )
        # capex_growth = self.get_st_growth(self.capex)
        self.capex = self.get_projections(
            elements_list=self.capex,
            periods=periods,
            growth_rate=st_growth,
        )


def dcf(ebit, dna, nwc, capex, tax_rate, lt_growth, wacc, dt):
    # FCF = EBIT(1 - tax) + DnA - NWC - CAPEX
    capex = -capex  # adjust negative value
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
