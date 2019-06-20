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

import warnings
from datetime import datetime

import pandas as pd

from evkit import capital
from evkit import financials
from evkit import utils

warnings.filterwarnings('ignore')

# Assumptions
forecast_horizon = 5

# get tickers pool url
tickers_key, tickers_urls = utils.get_tickers_url()
# extract list of stocks, write to file
tickers_df = utils.get_tickers(tickers_urls)
# extract risk-free rate, market return, market risk premium
rf, mrp = utils.get_rf_mrp()
# select data to be written to report
results_dict = {
    'beta_equity': [],
    'beta_asset': [],
    'beta_debt': [],
    're': [],
    'rd': [],
    'wacc': [],
    'enterprise_value, $B': [],
    'equity_value, $B': [],
    'stock_price': [],
    'mkt_stock_price': []
}
# select tickers sample
ticker_collection = tickers_df.ticker[:]
sample_size = len(ticker_collection)
try:
    for num, ticker in enumerate(ticker_collection):
        print(f'\n{num + 1}/{sample_size} Processing {ticker}', end=' ')
        # create instances of pro-forma financial statements and Cost of Capital
        fin_is = financials.IncomeStatement(ticker)
        fin_bs = financials.BalanceSheet(ticker)
        fin_cf = financials.CashFlowStatement(ticker)
        cap = capital.CostOfCapital(
            ticker=ticker,
            rf=rf,
            mrp=mrp
        )
        # Web data extraction
        # extract beta of equity (levered beta)
        beta_eq, mkt_price = cap.get_stock_summary()
        # extract shares outstanding
        num_shares = cap.get_shares_outstanding()
        # extract previous close
        # [TBD]

        # web data integrity check
        collection = [
            beta_eq,
            mkt_price,
            num_shares
        ]
        if None in collection:
            print('-> Missing trading information', end='')
            for key in results_dict.keys():
                results_dict[key].append(None)
            continue
        # extract financial reports
        fin_is.get_html_data()
        fin_bs.get_html_data()
        fin_cf.get_html_data()
        # populate fin statements with actual data
        fin_is.actual_statement()
        fin_bs.actual_statement()
        fin_cf.actual_statement()
        # get effective tax rate
        tax_rate = fin_is.get_tax_rate()

        # Cost of Capital
        # get cost of debt
        rd = cap.get_cost_of_debt(
            debt=fin_bs.total_debt,
            interest=fin_is.interest
        )
        # get debt beta
        beta_debt = cap.get_debt_beta()
        # get asset beta
        beta_asset = cap.get_asset_beta(
            debt=fin_bs.lt_debt,
            equity=fin_bs.equity,
            tax_rate=tax_rate
        )
        # get cost of equity
        re = cap.get_cost_of_equity()
        # get WACC
        wacc = cap.get_wacc(
            debt=fin_bs.lt_debt,
            assets=fin_bs.total_assets,
            tax_rate=tax_rate
        )
        # get discount factors
        dt = capital.discount_factors(
            wacc=wacc,
            periods=forecast_horizon
        )

        # DCF
        # implement industry-specific estimates for LT growth rate
        lt_growth = wacc * 0.5
        # get ST growth rate from revenue
        st_growth = fin_is.get_st_growth(fin_is.revenue)
        # make financial projections
        fin_is.forecast_statement(
            st_growth=st_growth,
            periods=forecast_horizon
        )
        fin_bs.forecast_statement(
            st_growth=st_growth,
            periods=forecast_horizon
        )
        fin_cf.forecast_statement(
            st_growth=st_growth,
            periods=forecast_horizon
        )
        # Enterprise value
        fcf, ev = financials.dcf(
            ebit=fin_is.ebit,
            dna=fin_cf.depreciation,
            nwc=fin_bs.nwc,
            capex=fin_cf.capex,
            tax_rate=tax_rate,
            lt_growth=lt_growth,
            wacc=wacc,
            dt=dt
        )
        # Equity value
        eq = ev - fin_bs.total_debt[3] + fin_bs.cash[3]
        # Share price
        stock_price = max(0, eq / num_shares)

        # store results into dictionary
        results_dict['beta_equity'].append(beta_eq)
        results_dict['beta_asset'].append(beta_asset)
        results_dict['beta_debt'].append(beta_debt)
        results_dict['re'].append(re)
        results_dict['rd'].append(rd)
        results_dict['wacc'].append(wacc)
        results_dict['enterprise_value, $B'].append(ev / 1_000_000)
        results_dict['equity_value, $B'].append(eq / 1_000_000)
        results_dict['stock_price'].append(stock_price)
        results_dict['mkt_stock_price'].append(mkt_price)

except KeyboardInterrupt:
    print('\n-> Program interrupted by user', end='')
    quit()
finally:
    # write results to report
    results_df = pd.DataFrame(results_dict)
    report_df = pd.concat([tickers_df, results_df], axis=1)
    # get date as id for report
    date = datetime.today().strftime('-%Y%m%d')
    report_id = date.join([tickers_key, ''])
    utils.results_to_csv(
        data_df=report_df,
        report_id=report_id
    )
    # plot results
    beta_asset = report_df.beta_asset
    wacc = report_df.wacc
    dcf = report_df.stock_price
    mkt_quote = report_df.mkt_stock_price
    utils.plot_beta_wacc(
        beta=beta_asset,
        wacc=wacc
    )
    utils.plot_dcf_mkt_price(
        dcf_price=dcf,
        mkt_price=mkt_quote
    )
