# Project 01 — NVIDIA (NVDA) Equity Research & Three-Statement DCF

## Analytical question
How does NVIDIA's implied equity value change under explicitly stated cash-flow growth, discount-rate and terminal-growth assumptions?

## Reporting anchor
NVIDIA FY2026 GAAP revenue was **$215,938 million**, net income **$120,067 million**; FY2025 GAAP revenue **$130,497 million**. See [NVIDIA FY2026 investor release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) and [Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm). The forecast starts after NVIDIA FY2026. This is not a current-quarter 2026/27 update.

## Modelling pipeline
1. `model.py`: linked FY2027–FY2029 illustrative income statement, balance sheet and cash-flow forecast from assumptions.
2. `valuation_case.py`: enterprise discounted cash flow based on three-year unlevered cash-flow **proxy** (operating cash flow minus capex), then net cash bridge to equity value.
3. Scenario parameters: bear (12.5% WACC, 2.5% perpetual growth), base (10.5%, 3.5%) and bull (9.0%, 4.0%). Further cash-flow scaling differs by scenario.
4. 5 × 5 WACC/terminal growth sensitivity matrix.
5. A **24,500 million share count is illustrative, not verified for the valuation date**. Verify share count and stock-based compensation treatment before citing any per-share valuation.

## Valuation caveats
Operating cash flow less capex is **levered company FCF**, not technically unlevered FCFF. Accordingly this first-stage DCF uses an approximate enterprise-value bridge and **must not be described as a fully calibrated institutional FCFF DCF or live price target**. The three-year explicit projection also concentrates value in the terminal assumption. Future version should calculate EBIT(1-tax) + D&A - capex - ΔNWC and reconcile share counts/market cap to the same as-of date.

**Do not label scenario outputs BUY / SELL, calculate upside to an unverified current share price, or advertise these as NVIDIA management guidance.**

Reproduce from repository root: `python -m case_studies.nvidia_three_statement.valuation_case`.
