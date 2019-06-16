# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [0.7.0] - 2019-06-16
### Added
- automated ticker list extraction with html page offset
- missing data exceptions handling
- writer of valuation results to csv report
- collection IDs of sector/industry securities
- mkt share price getter
- basic interface for selecting stocks pool
- performance and stability improvements
- package files: setup.py, environment.yaml
- Semantic Versioning structure to CHANGELOG.md
- license and build badges to README.md
- sample reports from test-runs

### Changed
- LT growth rate estimate as fraction of WACC
- rd estimate as interest/total debt
- EQ as EV + cash - total debt
- GitHub repo name to https://github.com/lialkaas/evkit
- moved capital, financials, utils into modules dir
- renamed launcher into evkit.py


## [0.6.0] - 2019-06-10
### Added
- complete rebase of the project
- Web data extraction: financial statements, rf, market return, stock stats and summary
- Financials: pro-forma Income statement, Balance Sheet, CF Statement
- Cost of Capital: re, rd, betas, wacc
- appropriate CHANGELOG.md
- MIT license to modules

### Changed
- name of the project to Equity valuation kit

### Removed
- sensitivity reports
- outdated tutorials (all of them)
- irrelevant utils
- all functionality, except bare minimum for DCF-WACC valuation

## [0.5.0] - 2018-11-19
### Added
- modular design of the program
- source of cost of capital assumptions from YahooFinance
- source of financials for DCF from YahooFinance
- no-API design

### Changed
- reduced number of user assumptions to ticker
- optimization tweaks

## [0.4.0] - 2018-09-24
### Added
- Multiples module
- basic public comparables ratios: EPS, P/E, EV/EBITDA, Debt/EBITDA

### Changed
- optimized accuracy and precision of capital structure sensitivity analysis report
- deploying reports into "reports" directory with a company name
- compressed unnecessary functions into nested functions

## [0.3.0] - 2018-09-23
### Added
- sensitivity analysis of share price to LT growth rate
- detailed capital structure report, incl. credit metrics
- detailed report of optimal capital structure
- EXACT method for estimating rd and credit rating from interest coverage ratio
- source of credit ratings from Prof. Damodaran database (NYU Stern)

### Changed
- reduced number of key assumptions
- optimized betas' unlevering/relevering algorithm

## [0.2.0] - 2018-09-21
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

## [0.1.0] - 2018-09-19
### Added
- Initial commit
- cost of capital: re, rd, WACC
- basic DCF-WACC valuation
