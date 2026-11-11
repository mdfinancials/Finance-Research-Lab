# NVIDIA (NVDA) — Yahoo Finance-based Equity Research

**Publication framework:** 12 November 2026, Sydney time. **Primary third-party data provider:** Yahoo Finance (`NVDA`), retrieved by the `yfinance` Python library. **Units:** USD millions unless stated otherwise.

## Investment research question

What equity-value range follows from plausible NVIDIA revenue growth, operating margins and discount rates, given the latest annual data available through Yahoo Finance? Which assumptions dominate the estimated value?

## Data pipeline and traceability

- [Yahoo Finance income statement](https://finance.yahoo.com/quote/NVDA/financials/) — annual revenue, operating income, tax and diluted weighted-average share count.
- [Yahoo Finance balance sheet](https://finance.yahoo.com/quote/NVDA/balance-sheet/) — cash, short-term investments, debt and accounting reconciliation (where available).
- [Yahoo Finance cash-flow statement](https://finance.yahoo.com/quote/NVDA/cash-flow/) — operating cash flow and capital spending.
- [Yahoo Finance historical prices](https://finance.yahoo.com/quote/NVDA/history/) — latest available closing quote and one-year daily price series.
- [NVIDIA annual and interim filing source](https://investor.nvidia.com/financial-info/sec-filings/default.aspx) — primary-source cross-check recommended before citing Yahoo's normalized values externally.

**Important:** The script retrieves Yahoo statements *on execution*, so the returned data depends on retrieval date, availability and revisions. Yahoo Finance has rate limits and may omit or relabel fields. The app reports errors rather than inventing missing financial results. No downloaded Yahoo data snapshot is presently committed.

## Modelling steps

1. Import Yahoo annual income, balance-sheet and cash-flow statements, and one-year closing prices using `yfinance`.
2. Normalize monetary amounts to USD millions and capture fiscal-year-end dates.
3. Estimate **five years of free cash flow to the firm (FCFF)** using:
   `EBIT × (1 − tax rate) + depreciation & amortization − capital spending − change in operating working capital`.
4. Discount FCFF at a scenario WACC; calculate terminal value using the Gordon-growth formula.
5. Bridge enterprise value to equity using Yahoo-reported cash, short-term investments and debt.
6. Divide by an explicitly disclosed diluted share count, compare with the dated Yahoo closing price, and show bear/base/bull plus WACC/terminal-growth sensitivity.

## Key assumptions (analyst-created)

| Driver | Bear | Base | Bull |
|---|---|---|---|
| Five annual revenue growth rates | 22%, 16%, 12%, 10%, 8% | 35%, 25%, 20%, 15%, 12% | 43%, 32%, 25%, 18%, 14% |
| First-year operating margin | 51% | 57% | 60% |
| Final-year operating margin | 46% | 50% | 53% |
| WACC | 12.5% | 10.5% | 9.0% |
| Perpetual FCFF growth | 2.5% | 3.5% | 4.0% |

Other assumptions held constant across scenarios: 17% effective tax rate, depreciation and amortization at 1.5% of revenue, capex at 3.5% of revenue, and incremental net operating working capital at 8% of incremental revenue. These are modelling choices, not company management guidance or consensus analyst estimates.

**Share-count caution:** Yahoo's diluted average shares represent a historical weighted average rather than the latest actual outstanding shares. The app allows manual entry and flags the limitation. **Net-cash caution:** if Yahoo lacks a separately identifiable investments value, the model reports that investments were omitted; the resulting equity valuation may be understated.

## Research thesis and risks

NVIDIA's earnings power depends materially on AI data-centre capital spending, product execution and gross margin durability. The largest uncertainties for this specific model are: (a) sustainability of revenue growth, (b) competitive intensity and pricing, (c) export controls and concentration of demand, (d) spending on semiconductor supply and packaging, and (e) terminal-value sensitivity.

**Interpretation:** The valuation is a *conditional scenario exercise*, not a verified institutional price target. A higher WACC reduces present value while stronger sustained FCFF and higher terminal growth increase it. An observed gap between estimated value and market price cannot alone justify a Buy/Sell recommendation.

## Reproduction

From repository root:

```sh
pip install -r requirements.txt
python -m case_studies.nvidia_three_statement.yahoo_research
python -m pytest -q test_yahoo_research.py
streamlit run app.py
```

In the website sidebar, open **07 · NVIDIA Yahoo Finance Research**. Refresh the data to retry Yahoo access. The app caches fetched data for an hour.

## Remaining diligence before publishing an investment rating

- Cross-check Yahoo line items with NVIDIA's latest filed 10-K and 10-Q, including FY2027 interim results.
- Verify diluted shares, net cash including investments, lease obligations and share-based compensation dilution at a consistent valuation date.
- Update the first forecast year from available interim actuals; compare analyst drivers with management guidance and consensus.
- Validate the discount rate from a documented cost-of-equity and capital-structure analysis.
- Include a peer-multiple valuation, reconcile scenario probabilities and publish a dated research report with numerical outputs **only after live Yahoo data has been captured and checked**.

_This case study is educational research and does not constitute investment advice._
