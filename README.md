# Finance Research Lab — Five Applied Finance Projects

[![Python model tests](https://github.com/mdfinancials/Finance-Research-Lab/actions/workflows/python-tests.yml/badge.svg)](https://github.com/mdfinancials/Finance-Research-Lab/actions/workflows/python-tests.yml)

Five educational financial analytics prototypes, plus five applied case studies that demonstrate core analyst skills: **equity valuation, portfolio construction, financial-crime risk triage, interest-rate risk, and M&A deal analysis**.

> **Transparency:** This repository ships with *synthetic illustrative data and assumptions*, **not live prices or real customer records**. It makes no claim of realised portfolio returns or verified client outcomes. Models are simplified educational tools, not financial advice, KYC compliance determinations, or investment recommendations.


## Interactive portfolio website

**[Open the interactive Finance Research Lab →](https://md-finance-research-lab.streamlit.app/)** — Streamlit website deployed from this repository. Explore five model categories and five applied case studies. Screenshots confirm the homepage is loading; individual model interactions and anonymous access should still be checked before putting this link on a CV.

Source: [`app.py`](app.py) · [Deployment & troubleshooting](DEPLOY.md).

## Featured case study: NVIDIA (NVDA) three-statement model

[Explore the NVIDIA three-statement case study](case_studies/nvidia_three_statement/README.md). This research exercise uses reported FY2025–FY2026 NVIDIA financial statements and transparent, illustrative FY2027–FY2029 assumptions to link income, balance-sheet and cash-flow projections. The case study includes a tested Python forecasting implementation. The downloadable Excel workbook can be added to the folder separately.

## Applied finance case studies — five reproducible projects

Each case study has its own analytical question, methods, assumptions, limitations, and runnable Python script.

| Case study | Applied question | Evidence |
|---|---|---|
| [01 NVIDIA three-statement & DCF](case_studies/nvidia_three_statement/VALUATION.md) | What drives implied equity value? | Reported FY2025/26 company data; explicit FY2027–FY2029 scenarios |
| [02 ETF allocation & stress](case_studies/etf_portfolio/README.md) | How do diversification and correlated downside shocks affect risk? | VOO/VXUS/QQQ allocation using clearly *synthetic* return paths |
| [03 Explainable KYC prioritisation](case_studies/kyc_triage/README.md) | Can audit-friendly risk rules help triage reviews? | Synthetic customer data and synthetic review labels |
| [04 Treasury duration & convexity](case_studies/treasury_duration/README.md) | How sensitive is a bond proxy to rate shocks? | Dated US Treasury par yield plus hypothetical coupon bond |
| [05 Hypothetical M&A](case_studies/ma_acquisition/README.md) | What synergies and funding mix lead to EPS accretion? | Fictional acquisition with scenario and break-even analysis |

To reproduce all case studies: install `requirements.txt` then run `python -m pytest -q`. To run individual scripts: `python -m case_studies.etf_portfolio.study` (replace package name).

**Evidence standards:** These are analyst training studies, not validated investment recommendations, real trade returns, regulatory AML systems or actual deal announcements. Inputs, historical reference dates and illustrative scenarios are identified in each project.

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
