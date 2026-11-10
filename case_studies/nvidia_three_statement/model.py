"""NVIDIA FY2027–FY2029 linked three-statement forecast, USD millions.
Source: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
Illustrative educational assumptions; not consensus investment research.
"""
from dataclasses import dataclass
FY26=dict(revenue=215938,cash=10605,securities=51951,ar=38466,inventory=21403,prepaid=3180,ppe=10383,other_assets=70815,ap=9812,accrued=21352,debt=8468,other_liabilities=9878,equity=157293)
@dataclass(frozen=True)
class Drivers:
    growth:float; gross_margin:float; rd:float; sga:float; tax:float
    other_income:float; sbc:float; da:float; capex:float; ar:float
    inventory:float; prepaid:float; ap:float; accrued:float
    dividends:float; repurchases:float; securities_sweep:float=.85
    minimum_cash:float=10605
ASSUMPTIONS={
    2027:Drivers(.38,.70,.09,.022,.16,.01,.03,.016,.035,.17,.34,.015,.15,.09,.005,.10),
    2028:Drivers(.25,.69,.095,.023,.17,.01,.03,.017,.04,.17,.33,.015,.15,.09,.005,.10),
    2029:Drivers(.18,.68,.10,.024,.18,.01,.03,.018,.045,.16,.32,.015,.15,.09,.005,.10),
}
def forecast(base=None,drivers=None):
    prev=(FY26 if base is None else base).copy()
    result=[]
    for year,p in (ASSUMPTIONS if drivers is None else drivers).items():
        rev=prev['revenue']*(1+p.growth); cost=rev*(1-p.gross_margin)
        op=rev-cost-rev*p.rd-rev*p.sga
        net=(op+rev*p.other_income)*(1-p.tax)
        ar=rev*p.ar; inv=cost*p.inventory; prepaid=rev*p.prepaid
        ap=cost*p.ap; accrued=rev*p.accrued
        sbc=rev*p.sbc; da=rev*p.da; capex=rev*p.capex
        delta_wc=-(ar-prev['ar'])-(inv-prev['inventory'])-(prepaid-prev['prepaid'])+(ap-prev['ap'])+(accrued-prev['accrued'])
        cfo=net+sbc+da+delta_wc
        dividend=rev*p.dividends; buyback=rev*p.repurchases
        cash_before_sweep=prev['cash']+cfo-capex-dividend-buyback
        investment=max(0,cash_before_sweep-p.minimum_cash)*p.securities_sweep
        cash=cash_before_sweep-investment
        sec=prev['securities']+investment
        ppe=prev['ppe']+capex-da
        equity=prev['equity']+net+sbc-dividend-buyback
        assets=cash+sec+ar+inv+prepaid+ppe+prev['other_assets']
        liabilities=ap+accrued+prev['debt']+prev['other_liabilities']
        bs_check=assets-liabilities-equity
        cf_check=cash-prev['cash']-(cfo-capex-investment-dividend-buyback)
        row=dict(year=year,revenue=rev,cost=cost,operating_income=op,net_income=net,
            cash=cash,securities=sec,ar=ar,inventory=inv,prepaid=prepaid,ppe=ppe,
            other_assets=prev['other_assets'],ap=ap,accrued=accrued,debt=prev['debt'],
            other_liabilities=prev['other_liabilities'],equity=equity,assets=assets,
            liabilities=liabilities,operating_cash_flow=cfo,capex=capex,dividends=dividend,
            repurchases=buyback,sbc=sbc,securities_purchase=investment,
            bs_check=bs_check,cashflow_check=cf_check)
        assert abs(bs_check)<1e-6 and abs(cf_check)<1e-6
        result.append(row);prev=row
    return result
if __name__=='__main__':
    import csv
    rows=forecast()
    with open('nvda_forecast.csv','w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    print('Wrote nvda_forecast.csv; balance sheet and cash flow checks passed')
