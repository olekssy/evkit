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

from evkit import capital
from evkit import financials

# Assumptions
ticker = 'AMZN'


def main():
    # create instances of pro-forma financial statements and Cost of Capital
    fin_is = financials.IncomeStatement(ticker)
    fin_bs = financials.BalanceSheet(ticker)
    fin_cf = financials.CashFlowStatement(ticker)
    cap = capital.CostOfCapital(ticker)

    # extract data from html
    fin_is.get_html_data()
    fin_bs.get_html_data()
    fin_cf.get_html_data()
    # extract risk-free rate, market return, market risk premium
    cap.get_rf_mrp()
    # extract beta of equity (levered beta)
    cap.get_equity_beta()

    # populate fin statements with actual data
    fin_is.actual_statement()
    fin_bs.actual_statement()
    fin_cf.actual_statement()
    # get effective tax rate
    tax_rate = fin_is.get_tax_rate()

    # get cost of debt
    cap.get_cost_of_debt(fin_bs.lt_debt, fin_is.interest)
    # get debt beta
    cap.get_debt_beta()
    # get asset beta
    cap.get_asset_beta(debt=fin_bs.lt_debt,
                       equity=fin_bs.equity,
                       tax_rate=tax_rate
                       )
    # get cost of equity
    cap.get_cost_of_equity()
    # get WACC
    cap.get_wacc(debt=fin_bs.lt_debt, assets=fin_bs.total_assets, tax_rate=tax_rate)


if __name__ == '__main__':
    main()
