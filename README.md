# Equity valuation kit

[v0.6](CHANGELOG.md)

## Description
Application performs equity valuation of NYSE-listed companies by extracting and analyzing data from public sources. DCF-WACC approach is the core of the valuation algorithm, which is based on pro-forma financial statement projections and the cost of capital analysis.

## Features
- coherent DCF-WACC equity valuation approach
- automated web data extraction from YahooFinance and other public sources
- cost of capital valuation: betas, required rate of return, WACC

Unsupervised execution of the valuation algorithm is primary objective of the program. Information is automatically extracted, processed and stored for further analysis.


## Algorithm
- extract web data: financial reports, risk-free rate, equity beta
- make CF projections in pro-forma financial statement
- estimate cost of capital parameters: betas, cost of debt, equity, WACC
- get discount factors from WACC
- calculate FCF, Terminal value
- compute Enterprise value, Equity value
- estimate implied stock price from Equity value/shares outstanding
- display valuation results

## License and Copyright
Copyright (c) 2019 Oleksii Lialka

Licensed under the [MIT License](LICENSE.md).
