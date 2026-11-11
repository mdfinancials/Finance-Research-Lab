# Project 05 — Aster Cloud / Beacon AI Hypothetical Acquisition

**Scenario:** Aster Cloud (fictional buyer) considers acquiring Beacon AI (fictional software business). This is **not a real transaction** and all figures are fabricated analytical assumptions.

## Decision question
At what combination of funding mix, debt cost and annual pre-tax synergies would the transaction be EPS accretive? What synergies are required to break even?

## Transaction assumptions (US$ millions unless per share)
| Metric | Assumption |
|---|---:|
| Buyer earnings / diluted shares | $600m / 200m |
| Buyer share price | $45.00 |
| Target earnings / equity purchase price | $110m / $1,500m |
| Stock consideration | 40% |
| Debt consideration | 60% |
| Incremental debt interest | 6.5% |
| Tax rate | 25% |
| Annual pre-tax run-rate synergies | $30m |

## Method
The `study.py` script wraps the portfolio's original M&A EPS engine to compute new shares, new debt, after-tax interest, after-tax synergies, standalone and pro forma EPS, accretion/dilution and **EPS break-even synergies**. The scenario matrix spans stock funding from 0–100% and synergies from $0–80m.

## Investment committee memo
EPS accretion is only one screen, **not** value creation. Required diligence includes purchase accounting, one-off integration fees, amortisation, target debt/cash, cost of capital, deal strategic fit, governance, regulatory scrutiny and downside liquidity. The appropriate next stage is a full merger model with pro-forma three-statement outputs and transaction valuation.

From root: `python -m case_studies.ma_acquisition.study`
