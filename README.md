# Finance Research Lab — Five Applied Finance Projects

[![Python model tests](https://github.com/mdfinancials/Finance-Research-Lab/actions/workflows/python-tests.yml/badge.svg)](https://github.com/mdfinancials/Finance-Research-Lab/actions/workflows/python-tests.yml)

Five educational financial analytics prototypes, five applied case studies, and two research extensions (a sourced NVIDIA PDF and a historical ETF backtesting/optimisation dashboard) that demonstrate core analyst skills: **equity valuation, portfolio construction, financial-crime risk triage, interest-rate risk, and M&A deal analysis**.

> **Transparency:** The synthetic demonstration pages use *fictional return paths and assumptions*. Separate NVIDIA and historical ETF research pages retrieve **dated third-party Yahoo Finance observations**, which may be delayed or unavailable. No real customer records are included. It makes no claim of realised portfolio returns or verified client outcomes. Models are simplified educational tools, not financial advice, KYC compliance determinations, or investment recommendations.


## About the analyst

**MD Mahdi Mahbub Rauf** — Sydney, Australia

Bachelor of Commerce (Finance), **Macquarie University**. Banking experience as a **Personal Banking Consultant at HSBC Australia**, including customer-facing banking operations and fraud/scam awareness. Career interests include investment research, portfolio management, financial modelling, and analytical roles in financial services.

**Tools demonstrated in this repository:** Python, pandas, NumPy, SciPy, Streamlit and Excel. Methods include three-statement forecasting, discounted cash flow (DCF), portfolio risk analysis, fixed-income duration/convexity, synthetic KYC review prioritisation and M&A EPS accretion/dilution.

**Confidentiality:** These are independent educational studies; no bank customer records, confidential employer documents, or proprietary models are included.

## Interactive portfolio website

**[Open the interactive Finance Research Lab →](https://md-finance-research-lab.streamlit.app/)** — Streamlit website deployed from this repository. Explore five model categories, five applied case studies, a downloadable initiation-style NVIDIA research PDF, and a Yahoo-based VOO/VXUS/QQQ historical ETF portfolio dashboard.

Source: [`app.py`](app.py) · [Deployment & troubleshooting](DEPLOY.md).

## NVIDIA equity research using Yahoo Finance

[Open the NVIDIA Yahoo Finance research methodology](case_studies/nvidia_three_statement/YAHOO_FINANCE_RESEARCH.md). The live Streamlit sidebar includes **07 · NVIDIA Yahoo Finance Research**, with a Yahoo Finance annual-statement import, a dated historical share-price chart, five-year FCFF scenarios, and WACC/terminal-growth sensitivity analysis.

**Research report:** [NVIDIA initiation-style PDF methodology](case_studies/nvidia_three_statement/INITIATION_REPORT.md). The Streamlit page generates a professionally formatted PDF from the available Yahoo snapshot, incorporating a dated qualitative thesis, company disclosures from 26 August 2026, illustrative DCF scenarios, catalysts, risk factors and references.

**Historical ETF research:** [VOO/VXUS/QQQ methodology](case_studies/etf_portfolio/HISTORICAL_RESEARCH.md). Sidebar page **08 · Historical ETF Backtest** retrieves adjusted Yahoo price history, computes fixed-weight historical portfolio statistics, plots a long-only efficient frontier, and compares historical *in-sample* minimum-variance and maximum-Sharpe weights. These hindsight-optimised weights are **not** represented as realised trading performance.

**Data quality:** Yahoo Finance data is requested dynamically; availability and reported fields can vary. The project does not claim a verified live price target or publish unvalidated downloaded values.

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

## Research takeaways

| Project | Main learning |
|---|---|
| NVIDIA valuation | Implied DCF values are highly sensitive to WACC, terminal growth and cash-flow assumptions. |
| ETF construction | VOO and QQQ introduce overlapping US large-cap risk. The synthetic risk lab is separate from the real historical backtest; in-sample optimized weights are not out-of-sample investment performance. |
| Synthetic KYC | Reason-coded review queues improve transparency; unvalidated thresholds and small fictional samples cannot support production compliance claims. |
| Bond risk | Fixed-rate bond prices fall as yields rise; convexity improves duration-based approximations for larger yield shocks. |
| Hypothetical M&A | Greater synergies can lift pro-forma EPS, but EPS accretion alone does not establish transaction value creation. |

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
| Portfolio | How do diversification choices affect risk? | The original model is synthetic; the separate adjusted-price backtest is historical but uses simplified costs and in-sample hindsight optimisation |
| KYC | Which *synthetic* cases are flagged for human review? | Thresholds are arbitrary, not validated or regulatory-compliant |
| Bonds | How sensitive is price to parallel rate shifts? | Fixed annual coupons; excludes credit, liquidity, yield-curve shape |
| M&A | Can a simplified deal be EPS-accretive? | Excludes transaction fees, purchase accounting, integration costs |

## Recommended next iterations

1. Replace scenario inputs with properly sourced public-company filings and dated price data; cite every source.
2. Extend the NVIDIA initiation-style research with verified interim 10-Q updates, peer multiples and deeper industry diligence.
3. Extend the current historical ETF sample into a walk-forward out-of-sample optimisation strategy with explicit turnover, fee and tax modelling.
4. Build an anonymised *synthetic* case investigation workflow, with false-positive measurement and governance.
5. Extend the deal model to purchase price allocation, financing schedules, transaction fees and integration scenarios.

## Suggested CV description

**Independent Financial Analytics Portfolio** — Built five Python/Streamlit analytical prototypes covering DCF valuation, portfolio performance measurement, explainable synthetic KYC risk screening, duration/convexity modelling and M&A EPS accretion/dilution. Implemented scenario controls, documented assumptions and automated model tests.

Only use this description once you have personally reviewed and can explain the models. Never present synthetic returns as real investment performance.

## AI-assisted development

This independent educational project was built with the assistance of OpenAI's ChatGPT for programming, workflow design and documentation. AI-assisted outputs remain subject to human review, source verification, and scrutiny of modelling assumptions; AI involvement is not evidence of independently validated institutional-grade research.

## Author and licence

Portfolio project prepared for personal learning and review. Add your name and a repository licence before public release.
