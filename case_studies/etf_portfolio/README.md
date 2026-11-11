# Project 02 — Global ETF Portfolio Construction & Risk Stress Test

**Investment mandate:** design a diversified, long-only portfolio allocating 45% VOO (US large cap), 35% VXUS (non-US equities) and 20% QQQ (Nasdaq-100 exposure). This is a *hypothetical portfolio*, not a recommendation or a record of trades.

## Investment question
Does an allocation that includes concentrated US growth exposure justify the additional risk relative to a broader US/non-US allocation?

## Method and outputs
- `study.py` generates 120 monthly *synthetic* multivariate return observations with a reproducible seed.
- Estimates annualised volatility, CAGR, Sharpe ratio, maximum drawdown and beta against the synthetic VOO proxy.
- Computes a nonnegative minimum-variance allocation using the model covariance matrix.
- Applies a discrete hypothetical stress: VOO -30%, VXUS -25%, QQQ -40%; compares with initial portfolio weights.
- Includes correlation assumptions to illustrate overlap, rather than claiming actual holdings-level overlap.

## Initial weight choices
| ETF | Allocation | Role | Key risk |
|---|---:|---|---|
| VOO | 45% | US core | US large-cap concentration |
| VXUS | 35% | International diversification | FX and foreign equity risks |
| QQQ | 20% | US growth tilt | Overlap with VOO and sector concentration |

**Inputs:** illustrative annual returns of 7.5%, 6.5%, 8.5% and volatilities of 18%, 20%, 25%, respectively. These are assumptions, not quoted fund returns or expected performance.

## Reproduce
From repository root: `python -m case_studies.etf_portfolio.study`

## Decision memo
The allocation deliberately balances geographic breadth against a US technology/growth tilt. Overlap between VOO and QQQ weakens the diversification benefit. The risk report is useful for scenario planning but not sufficient to recommend an allocation: next step is to replace synthetic returns with licensed, adjusted, point-in-time histories, document fees, FX, rebalancing, and run rolling out-of-sample tests.

**Sources for fund classification:** [Vanguard VOO](https://investor.vanguard.com/investment-products/etfs/profile/voo), [Vanguard VXUS](https://investor.vanguard.com/investment-products/etfs/profile/vxus), [Invesco QQQ](https://www.invesco.com/qqq-etf/en/home.html). Fund descriptors are references; none of their return histories are embedded here.
