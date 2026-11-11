# Historical ETF Portfolio | VOO, VXUS and QQQ

**New interactive page:** select **08 | Historical ETF Backtest** inside the [Finance Research Lab](https://md-finance-research-lab.streamlit.app/).

## Objective
Show how *specified*, long-only VOO/VXUS/QQQ allocations performed in a historical USD backtest. Compare risk-return characteristics with a VOO-only benchmark and visualise a **hindsight / in-sample** efficient frontier and theoretical maximum-Sharpe and minimum-variance weights.

## Data
- Yahoo Finance through the `yfinance` package, with **auto-adjusted daily closes** (dividends/splits).
- Samples are the **common** observations for all three ETFs, with daily prices reduced to completed month-ends.
- The current, incomplete calendar month is not included in the monthly backtest.
- The site caches Yahoo downloads for one hour and provides manual refresh.
- Yahoo data is third-party and may be delayed, amended or temporarily unavailable. No synthetic fallback is mislabelled as historical.

## Methods
- User-selected weights sum to 100%, are non-negative and are rebalanced every month.
- Cumulative wealth begins at one dollar; annualised CAGR, volatility, Sharpe and maximum drawdown describe the sampled historical returns.
- Simplified optional monthly transaction-cost deduction is included but does not simulate actual turnover, tax, FX, fees or bid-ask spreads.
- Annual risk-free input affects the Sharpe ratio and optimisation.
- The long-only efficient frontier minimises historical sample variance for a series of target annualised **arithmetic** returns.
- Maximum-Sharpe weights maximise the sampled annualised risk-adjusted **arithmetic** return. All optimised portfolios use the full historical window and must **not** be represented as investable or out-of-sample performance.
- The only displayed historical backtest is for the user's *selected static weights*. We do not backtest maximum-Sharpe weights using returns that the optimiser has already seen.

## Limitations
In-sample optimisation is susceptible to hindsight and estimation error; a professional extension would use walk-forward out-of-sample testing and realistic turnover, cost, tax and market-data validation. VOO and QQQ hold overlapping US mega-cap exposures. The sample does not offer forward expected returns. Currency changes may materially affect Australian investors.

Run `python -m pytest -q` locally for offline deterministic model tests. All numbers on the live page should be independently checked against fund statements before publication as investment research.
