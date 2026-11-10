# Finance Research Lab — Five Applied Finance Projects

[![Model tests](https://img.shields.io/badge/models-tested-brightgreen)](#quality-checks)

Five educational financial analytics prototypes that demonstrate core analyst skills: **equity valuation, portfolio construction, financial-crime risk triage, interest-rate risk, and M&A deal analysis**.

> **Transparency:** This repository ships with *synthetic illustrative data and assumptions*, **not live prices or real customer records**. It makes no claim of realised portfolio returns or verified client outcomes. Models are simplified educational tools, not financial advice, KYC compliance determinations, or investment recommendations.


## Featured case study: NVIDIA (NVDA) three-statement model

[Explore the NVIDIA three-statement case study](case_studies/nvidia_three_statement/README.md). This research exercise uses reported FY2025–FY2026 NVIDIA financial statements and transparent, illustrative FY2027–FY2029 assumptions to link income, balance-sheet and cash-flow projections. The case study includes a tested Python forecasting implementation. The downloadable Excel workbook can be added to the folder separately.

## Projects

| # | Project | Skills demonstrated | Module |
|---|---|---|---|
| 01 | Equity Research & DCF | Free cash flow forecasting, WACC, terminal value, sensitivity | `projects/valuation.py` |
| 02 | Portfolio Analytics | Sharpe, beta, drawdown, minimum-variance weights | `projects/portfolio.py` |
| 03 | KYC Review Triage | Explainable risk rules, customer data validation, audit-friendly reason codes | `projects/kyc.py` |
| 04 | Fixed Income Risk | Bond pricing, duration, convexity, yield shock scenarios | `projects/fixed_income.py` |
| 05 | M&A Deal Model | Funding mix, pro forma EPS, accretion/dilution, synergies | `projects/mergers.py` |

## Run locally

Requires Python 3.11+:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`. Select a project using the left sidebar and adjust assumptions interactively.

## Quality checks

```bash
python -m pytest -q
```

Unit tests cover fundamental identities, expected sensitivity direction, financial model sanity checks and rule outputs. GitHub Actions runs these tests on pushes and pull requests.

## Analyst-oriented interpretation and limitations

| Project | Illustrative question | Important limitation |
|---|---|---|
| DCF | How does implied value shift with WACC or growth? | No filing-derived forecast; terminal assumptions drive value |
| Portfolio | How do diversification choices affect risk? | Synthetic monthly returns, no transaction costs or forward performance |
| KYC | Which *synthetic* cases are flagged for human review? | Thresholds are arbitrary, not validated or regulatory-compliant |
| Bonds | How sensitive is price to parallel rate shifts? | Fixed annual coupons; excludes credit, liquidity, yield-curve shape |
| M&A | Can a simplified deal be EPS-accretive? | Excludes transaction fees, purchase accounting, integration costs |

## Recommended next iterations

1. Replace scenario inputs with properly sourced public-company filings and dated price data; cite every source.
2. Add company-specific three-statement models and peer valuation, with clear forecast assumptions.
3. Use point-in-time price histories for out-of-sample portfolio backtests and include fees.
4. Build an anonymised *synthetic* case investigation workflow, with false-positive measurement and governance.
5. Extend the deal model to purchase price allocation, financing schedules, transaction fees and integration scenarios.

## Suggested CV description

**Independent Financial Analytics Portfolio** — Built five Python/Streamlit analytical prototypes covering DCF valuation, portfolio performance measurement, explainable synthetic KYC risk screening, duration/convexity modelling and M&A EPS accretion/dilution. Implemented scenario controls, documented assumptions and automated model tests.

Only use this description once you have personally reviewed and can explain the models. Never present synthetic returns as real investment performance.

## Author and licence

Portfolio project prepared for personal learning and review. Add your name and a repository licence before public release.
