# NVIDIA (NVDA) — Three-Statement Financial Model

**Scope:** Two years of audited annual history (FY2025–FY2026) and three illustrative forecasts (FY2027–FY2029). **Units: US$ millions**, unless otherwise stated.

## Deliverables
- `NVIDIA_NVDA_Three_Statement_Model.xlsx`: Excel workbook with **Overview**, **Assumptions**, **Income Statement**, **Balance Sheet**, **Cash Flow**, and **Sources & Notes**. Upload the Excel workbook into this folder to distribute it with the source code.
- `model.py`: fully linked Python operating forecast that tests balance-sheet and cash-flow identities.
- `test_model.py`: automated reconciliation tests.

### Historical source
[NVIDIA Form 10-K for FY2026, ending 25 January 2026](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), consolidated financial statements (pp. 51, 53, 55).

| Historical reported metric | FY2025 | FY2026 |
| --- | ---: | ---: |
| Revenue | 130,497 | 215,938 |
| Net income | 72,880 | 120,067 |
| Operating cash flow | 64,089 | 102,718 |
| Total assets | 111,601 | 206,803 |
| Total shareholders' equity | 79,327 | 157,293 |

**Forecast assumptions are analyst-created educational scenarios, not NVIDIA guidance, consensus estimates or a price target.** The model holds other non-current assets, non-working-capital liabilities and debt constant, excludes extraordinary acquisitions and equity remeasurements, and uses a cash-to-marketables treasury sweep. Repurchases reduce equity; stock compensation increases it.

### Run the Python model

```sh
cd case_studies/nvidia_three_statement
python model.py
python -m unittest test_model.py
```

The script writes `nvda_forecast.csv` and asserts both accounting identities for each forecast year. The Excel file independently links statement calculations to editable driver assumptions. Neither the script nor workbook predicts NVDA's share price.

### Interpretation
The model is intended for interviews to explain how revenue, profitability, working capital, capital spending, cash, and shareholder distributions interact. Validate all assumptions against more recent quarterly filings before treating any forecast as current.