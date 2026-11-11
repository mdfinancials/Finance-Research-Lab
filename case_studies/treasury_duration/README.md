# Project 04 — Treasury Yield Shock & Duration/Convexity Analysis

**Market observation:** 10-year **US Treasury par yield = 4.98% on 10 November 2026** ([US Treasury daily rates](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202611&type=daily_treasury_yield_curve)).

## Trade / risk question
How does a 10-year fixed-rate bond proxy respond to parallel interest-rate shocks? When does duration/convexity approximation diverge from exact discounted cash-flow repricing?

## Hypothetical instrument
- Face value: USD 1,000
- Annual coupon: 4.50% (assumed)
- Remaining maturity: 10 years (assumed)
- Yield: 4.98% (dated market **par yield input**, not a traded bond's observed YTM)
- Price: discounted annual coupons and principal at the same single yield (flat single-rate simplification)

## Method
`study.py` computes exact price, Macaulay/modified duration, convexity, and scenario P&L for shocks -200, -100, -50, 0, +50, +100, +200 basis points. It compares exact discounted-cash-flow repricing against `-modified_duration * Δy + 0.5 * convexity * Δy²`.

## Conclusion
Bond prices and yields move inversely. A longer-duration bond carries larger mark-to-market sensitivity. Convexity improves approximation for larger shocks. **Not a specific Treasury bond or trade recommendation**: no coupon schedule/accrual, non-par curve bootstrapping, key-rate durations, credit spread or liquidity assumptions.

From root: `python -m case_studies.treasury_duration.study`
