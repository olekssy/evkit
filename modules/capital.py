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
1/ get equity_beta, rf, mrp from sources
2/ get empirical rd from mean(interest / total debt)
3/ get debt_beta from the reverse CAPM of rd
4/ unlever equity beta by βu = (βL + βd*(1-tax)*D/E) / (1 + (1-tax)*D/E)
5/ get re from CAPM und beta of assets
6/ calculate WACC
"""

import numpy as np

from modules import utils


class CostOfCapital:
    # unique ID of YahooFinance urlcurrent_assets_id
    summary_url_id = '?p='
    statistics_url_id = '/key-statistics?p='
    # positional index of values in html
    mkt_price_id = 1
    beta_id = 19
    shares_outstanding_id = 81

    def __init__(self, ticker, rf, mrp):
        self.ticker = ticker
        self.rf = rf  # risk-free rate
        self.mrp = mrp  # market risk premium
        self.mkt_price = None  # previous close pps
        self.equity_beta = None  # levered beta
        self.asset_beta = None  # unlevered beta
        self.debt_beta = None
        self.rd = None  # cost of debt
        self.re = None  # cost of equity
        self.wacc = None
        self.num_shares = None  # number of shares outstanding

    def get_shares_outstanding(self):
        statistics_html = utils.get_html(
            ticker=self.ticker,
            url_id=self.statistics_url_id,
            show_page=False
        )
        num_shares = utils.get_shares_num(
            html_page=statistics_html,
            value_index=self.shares_outstanding_id
        )
        return num_shares

    def capm(self, beta, rate=None):
        if rate is None:
            # find required rate of return from beta
            value = self.rf + beta * self.mrp
        else:
            # find beta from return
            value = (rate - self.rf) / self.mrp
        return value

    def get_stock_summary(self):
        # open summary page
        summary_html = utils.get_html(
            ticker=self.ticker,
            url_id=self.summary_url_id,
            YahooFinance=True,
            show_page=False
        )
        # get equity beta
        self.equity_beta = utils.get_value(
            html_page=summary_html,
            value_index=self.beta_id
        )
        # get previous close price
        self.mkt_price = utils.get_value(
            html_page=summary_html,
            value_index=self.mkt_price_id
        )
        return self.equity_beta, self.mkt_price

    def get_cost_of_debt(self, debt, interest):
        # cost of debt
        if 0 in debt:
            self.rd = 0
        else:
            interest = -interest  # adjust negative value
            self.rd = np.mean(interest / debt)
        return self.rd

    def get_debt_beta(self):
        self.debt_beta = self.capm(
            beta=None,
            rate=self.rd
        )
        return self.debt_beta

    def get_asset_beta(self, debt, equity, tax_rate):
        # βu = (βL + βd * (1 - tax) * D / E) / (1 + (1 - tax) * D / E)
        debt = debt[3]
        equity = equity[3]
        de = debt/equity
        nominator = self.equity_beta + self.debt_beta*(1 - tax_rate)*de
        denominator = 1 + (1 - tax_rate) * de
        self.asset_beta = nominator / denominator
        return self.asset_beta

    def get_cost_of_equity(self):
        self.re = self.capm(
            beta=self.asset_beta,
            rate=None
        )
        return self.re

    def get_wacc(self, debt, assets, tax_rate):
        debt = debt[3]
        assets = assets[3]
        dv = debt / assets
        self.wacc = self.re * (1 - dv) + (1 - tax_rate) * self.rd * dv
        return self.wacc


def discount_factors(wacc, periods=3):
    periods += 1  # adjust for terminal value
    dt = [1 / (1 + wacc) ** t for t in range(1, periods + 1)]
    return np.array(dt)


def main():
    pass


if __name__ == '__main__':
    main()
