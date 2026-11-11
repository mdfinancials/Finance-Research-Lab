"""Dated US Treasury 10-year PAR yield and a hypothetical annual coupon bond."""
from projects.fixed_income import bond_analytics,shock_table
AS_OF="2026-11-10"
SOURCE="https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202611&type=daily_treasury_yield_curve"
TEN_YEAR_PAR_YIELD=.0498  # published 10 November 2026
COUPON=.045  # hypothetical 4.5% annual coupon, NOT a specific Treasury security
def analyse(yield_rate=TEN_YEAR_PAR_YIELD):
    bond=bond_analytics(face=1000,coupon_rate=COUPON,yield_rate=yield_rate,years=10)
    shocks=shock_table(base_yield=yield_rate,face=1000,coupon_rate=COUPON,years=10)
    rows=[]
    for _,r in shocks.iterrows():
        change=r["yield_change_bps"]/10000
        approx=-bond["modified_duration"]*change+.5*bond["convexity"]*change**2
        rows.append({"yield_shock_bps":int(r["yield_change_bps"]),
                     "exact_price_move_pct":r["price_change_pct"]*100,
                     "duration_convexity_move_pct":approx*100})
    return {"base_price":bond["price"],"duration":bond["modified_duration"],
            "convexity":bond["convexity"],"scenarios":rows}
if __name__=="__main__":
    print("HYPOTHETICAL 10Y BOND, NOT ACTUAL TREASURY PRICE",analyse())
