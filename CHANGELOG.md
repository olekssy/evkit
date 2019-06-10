# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]
## [0.6] - TBD
### Complete rebase of the project
### Added
- Web data extraction: financial statements, rf, market return, stock stats and summary
- Financials: pro-forma Income statement, Balance Sheet, CF Statement
- Cost of Capital: re, rd, betas, wacc
- MIT license to modules
- appropriate CHANGELOG.md
- develop branch

### Changed
- name of the project to Equity valuation kit

### Deleted
- sensitivity reports
- outdated tutorials (all of them)
- irrelevant utils
- deprecated modules

### Deprecated
- all functionality, except bare minimum for DCF-WACC valuation

## [0.5] - 2018-11-19
### Added
- modular design of the program
- source of cost of capital assumptions from YahooFinance
- source of financials for DCF from YahooFinance
- no-API design

### Changed
- reduced number of user assumptions to ticker
- optimization tweaks

## [0.4] - 2018-09-24
### Added
- Multiples module
- basic public comparables ratios: EPS, P/E, EV/EBITDA, Debt/EBITDA

### Changed
- optimized accuracy and precision of capital structure sensitivity analysis report
- deploying reports into "reports" directory with a company name
- compressed unnecessary functions into nested functions

## [0.3] - 2018-09-23
### Added
- sensitivity analysis of share price to LT growth rate
- detailed capital structure report, incl. credit metrics
- detailed report of optimal capital structure
- EXACT method for estimating rd and credit rating from interest coverage ratio
- source of credit ratings from Prof. Damodaran database (NYU Stern)

### Changed
- reduced number of key assumptions
- optimized betas' unlevering/relevering algorithm

## [0.2] - 2018-09-21
### Added
- detailed report of capital budgeting
- pro forma cash-flow statement for a chosen investment horizon
- Revenue to FCFF top-down approach for financial highlights
- robust DCF-WACC: Equity value does not depend on investment horizon
- basic sensitivity analysis of capital structure
- rd, re, WACC for different level of leverage
- optimal capital structure estimate for max Equity value
- write sensitivity analysis report to .csv file

### Changed
- improved delevering/relevering betas

## [0.1] - 2018-09-19
### Initial commit
- cost of capital: re, rd, WACC
- basic DCF-WACC valuation
