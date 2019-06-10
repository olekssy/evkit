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

# Algorithm
# 1/ get equity_beta, rf, mrp from sources
# 2/ get empirical rd from mean(interest / LT debt)
# 3/ get debt_beta from the reverse CAPM of rd
# 4/ unlever equity beta as βu = (βL + βd*(1-tax)*D/E) / (1 + (1-tax)*D/E)
# 5/ get re from CAPM und beta of assets
# 6/ calculate WACC

# Note: rf yield curve estimates http://www.basiszinskurve.de/basiszinssatz-gemaess-idw.html

import numpy as np

from evkit import urldata


class CostOfCapital:
    # unique ID of YahooFinance urlcurrent_assets_id
    summary_url_id = '?p='
    rf_ticker = '^TNX'  # Treasury Yield 10 Years
    market_url = 'http://news.morningstar.com/index/indexReturn.html'
    # positional index of values in html
    beta_id = 19
    rf_id = 1
    market_id = 43  # 1Y US market return value id

    def __init__(self, ticker):
        self.ticker = ticker
        self.rf = None
        self.mkt_return = None
        self.mrp = None
        self.equity_beta = None  # levered beta
        self.asset_beta = None  # unlevered beta
        self.debt_beta = None
        self.rd = None
        self.re = None
        self.wacc = None
        self.num_shares = None

    def capm(self, beta, rate=None):
        if rate is None:
            # find required rate of return from beta
            value = self.rf + beta * self.mrp
        else:
            # find beta from return
            value = (rate - self.rf) / self.mrp
        return value

    def get_rf_mrp(self):
        # risk-free rate
        rf_html = urldata.get_html(ticker=self.rf_ticker,
                                   url_symbol=self.summary_url_id,
                                   YahooFinance=True,
                                   verbose=False
                                   )
        self.rf = urldata.get_value(rf_html, self.rf_id) / 100
        # market return
        market_html = urldata.get_html(ticker=None,
                                       url_symbol=self.market_url,
                                       YahooFinance=False,
                                       verbose=False
                                       )
        self.mkt_return = urldata.get_value(market_html, self.market_id) / 100
        # market risk pemium
        self.mrp = self.mkt_return - self.rf
        return self.rf, self.mkt_return, self.mrp

    def get_equity_beta(self):
        beta_html = urldata.get_html(ticker=self.ticker,
                                     url_symbol=self.summary_url_id,
                                     YahooFinance=True,
                                     verbose=False
                                     )
        self.equity_beta = urldata.get_value(beta_html, self.beta_id)
        return self.equity_beta

    def get_cost_of_debt(self, debt, interest):
        # cost of debt
        debt = np.asarray(debt)
        interest = - np.asarray(interest)
        self.rd = np.mean(interest / debt)
        return self.rd

    def get_debt_beta(self):
        self.debt_beta = self.capm(beta=None, rate=self.rd)
        return self.debt_beta

    def get_asset_beta(self, debt, equity, tax_rate):
        # βu = (βL + βd * (1 - tax) * D / E) / (1 + (1 - tax) * D / E)
        debt = debt[-1]
        equity = equity[-1]
        self.asset_beta = (self.equity_beta + self.debt_beta * (1 - tax_rate) * debt / equity) \
                          / (1 + (1 - tax_rate) * debt / equity)

    def get_cost_of_equity(self):
        self.re = self.capm(beta=self.asset_beta, rate=None)

    def get_wacc(self, debt, assets, tax_rate):
        debt = debt[-1]
        assets = assets[-1]
        dv = debt / assets
        self.wacc = self.re * (1 - dv) + (1 - tax_rate) * self.rd * dv
        return self.wacc


def main():
    pass


if __name__ == '__main__':
    main()
