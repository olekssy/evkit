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
ticker = input('Enter ticker (e.g. "AMZN"): ')
lt_growth = 0.045
forecast_horizon = 3


def main():
    # create instances of pro-forma financial statements and Cost of Capital
    fin_is = financials.IncomeStatement(ticker)
    fin_bs = financials.BalanceSheet(ticker)
    fin_cf = financials.CashFlowStatement(ticker)
    cap = capital.CostOfCapital(ticker)

    # extract risk-free rate, market return, market risk premium
    cap.get_rf_mrp()
    # extract financial reports
    fin_is.get_html_data()
    fin_bs.get_html_data()
    fin_cf.get_html_data()
    # extract beta of equity (levered beta)
    beta_eq = cap.get_equity_beta()
    # extract shares outstanding
    num_shares = cap.get_shares_outstanding()

    # populate fin statements with actual data
    fin_is.actual_statement()
    fin_bs.actual_statement()
    fin_cf.actual_statement()
    # get effective tax rate
    tax_rate = fin_is.get_tax_rate()
    # get ST growth rate from revenue
    st_growth = fin_is.get_st_growth(fin_is.revenue)
    # make financial projections
    fin_is.forecast_statement(st_growth=st_growth, periods=forecast_horizon)
    fin_bs.forecast_statement(st_growth=st_growth, periods=forecast_horizon)
    fin_cf.forecast_statement(st_growth=st_growth, periods=forecast_horizon)
    # get net working capital
    fin_bs.get_nwc()

    # get cost of debt
    rd = cap.get_cost_of_debt(fin_bs.lt_debt, fin_is.interest)
    # get debt beta
    beta_debt = cap.get_debt_beta()
    # get asset beta
    beta_asset = cap.get_asset_beta(debt=fin_bs.lt_debt,
                                    equity=fin_bs.equity,
                                    tax_rate=tax_rate
                                    )
    # get cost of equity
    re = cap.get_cost_of_equity()
    # get WACC
    wacc = cap.get_wacc(debt=fin_bs.lt_debt,
                        assets=fin_bs.total_assets,
                        tax_rate=tax_rate
                        )
    # get discount factors
    dt = capital.discount_factors(wacc, periods=forecast_horizon)

    # DCF
    # Enterprise value
    fcf, ev = financials.dcf(ebit=fin_is.ebit,
                             dna=fin_cf.depreciation,
                             nwc=fin_bs.nwc,
                             capex=fin_cf.capex,
                             tax_rate=tax_rate,
                             lt_growth=lt_growth,
                             wacc=wacc,
                             dt=dt
                             )
    # Equity value
    eq = ev - fin_bs.lt_debt[3] + fin_bs.cash[3]
    # Share price
    stock_price = eq / num_shares

    # Display results
    print(f'==Cost of capital report==\n'
          f'debt beta = {beta_debt:.2f}\n'
          f'equity beta = {beta_eq:.2f}\n'
          f'asset beta = {beta_asset:.2f}\n'
          f'rd = {rd * 100:.2f}%\n'
          f're = {re * 100:.2f}%\n'
          f'WACC = {wacc * 100:4.2f}%\n')
    print(f'==Financial projections==\n'
          f'Revenue {fin_is.revenue}\n'
          f'EBIT {fin_is.ebit}\n'
          f'NWC {fin_bs.nwc}\n'
          f'DnA {fin_cf.depreciation}\n'
          f'CAPEX {fin_cf.capex}\n'
          f'FCF {fcf}\n')
    print(f'==DCF-WACC results==\n'
          f'Enterprise value = {ev / 1_000_000:.2f}B\n'
          f'Equity value = {eq / 1_000_000:.2f}B\n'
          f'Stock price = {stock_price:.2f}')


if __name__ == '__main__':
    main()
