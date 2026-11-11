"""NVIDIA DCF extension to FY2027–29 linked forecast, USD millions.
Illustrative scenario valuations, NOT a live market price target.
"""
from case_studies.nvidia_three_statement.model import forecast, FY26
SCENARIOS={"bear":(.75,.125,.025),"base":(1.,.105,.035),"bull":(1.2,.09,.04)}
SHARES_M=24500  # illustrative diluted share count; replace with point-in-time filings
def value_case(case="base",wacc=None,terminal_growth=None):
    factor,rate,growth=SCENARIOS[case]
    rate=rate if wacc is None else wacc
    growth=growth if terminal_growth is None else terminal_growth
    if not 0<=growth<rate: raise ValueError("WACC must exceed terminal growth")
    base=forecast()
    fcfs=[(r["operating_cash_flow"]-r["capex"])*(1+(factor-1)*(i+1)/3) for i,r in enumerate(base)]
    pv=sum(v/(1+rate)**(i+1) for i,v in enumerate(fcfs))
    terminal=fcfs[-1]*(1+growth)/(rate-growth)/(1+rate)**len(fcfs)
    ev=pv+terminal
    net_cash=FY26["cash"]+FY26["securities"]-FY26["debt"]
    return {"case":case,"fcf_m":fcfs,"wacc":rate,"terminal_growth":growth,
            "ev_m":ev,"equity_m":ev+net_cash,"value_per_share_usd":(ev+net_cash)/SHARES_M,
            "terminal_pv_share":terminal/ev}
def sensitivity():
    return [(w,g,round(value_case(wacc=w,terminal_growth=g)["value_per_share_usd"],2))
            for w in (.09,.10,.11,.12,.13) for g in (.02,.025,.03,.035,.04)]
if __name__=="__main__":
    for case in SCENARIOS: print(value_case(case))
