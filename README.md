# Equity valuation kit

[![GitHub version](https://badge.fury.io/gh/lialkaas%2Fevkit.svg)](https://badge.fury.io/hooks/github/lialkaas/evkit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

[v0.7.0](CHANGELOG.md)

## Description
Application performs equity valuation of NYSE-listed companies by extracting and analyzing data from public sources. DCF-WACC approach is the core of the valuation algorithm, which is based on pro-forma financial statement projections and the cost of capital analysis.

## Features
- coherent DCF-WACC equity valuation approach
- automated web data extraction from YahooFinance and other public sources
- cost of capital valuation: betas, required rate of return, WACC
- structuring and writing valuation results into csv report

Unsupervised execution of the valuation algorithm is primary objective of the program. Information is automatically extracted, processed and stored for further analysis.


## Algorithm
- extract web data: financial reports, risk-free rate, equity beta
- estimate cost of capital parameters: betas, cost of debt, equity, WACC
- get discount factors from WACC
- make CF projections in pro-forma financial statement
- calculate FCF, Terminal value
- compute Enterprise value, Equity value
- estimate implied stock price from Equity value/shares outstanding
- save valuation results to csv

## License and Copyright
Copyright (c) 2019 Oleksii Lialka

Licensed under the [MIT License](LICENSE.md).
