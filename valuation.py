"""Illustrative DCF and trading multiples. Values are in millions unless stated."""
import numpy as np
import pandas as pd

def dcf(revenue=1000, growth=.07, ebit_margin=.20, tax_rate=.25, da_pct=.04,
        capex_pct=.06, nwc_pct=.02, wacc=.095, terminal_growth=.025,
        net_debt=300, shares=100, years=5):
    if not (0 <= terminal_growth < wacc):
        raise ValueError('Require 0 <= terminal growth < WACC')
    if shares <= 0 or years < 1: raise ValueError('Invalid share count or projection years')
    rows=[]; rev=float(revenue)
    for t in range(1,years+1):
        prev=rev; rev *= (1+growth)
        ebit=rev*ebit_margin
        nopat=ebit*(1-tax_rate)
        da=rev*da_pct; capex=rev*capex_pct
        delta_nwc=(rev-prev)*nwc_pct
        fcf=nopat+da-capex-delta_nwc
        rows.append(dict(year=t,revenue=rev,ebit=ebit,nopat=nopat,da=da,capex=capex,delta_nwc=delta_nwc,fcf=fcf,pv_fcf=fcf/(1+wacc)**t))
    forecast=pd.DataFrame(rows)
    tv=forecast.iloc[-1].fcf*(1+terminal_growth)/(wacc-terminal_growth)
    pv_tv=tv/(1+wacc)**years
    ev=forecast.pv_fcf.sum()+pv_tv
    equity=ev-net_debt
    return {'forecast':forecast,'terminal_value':tv,'enterprise_value':ev,'equity_value':equity,'price_per_share':equity/shares,'terminal_share_of_ev':pv_tv/ev}

def sensitivity(base=None, wacc_values=None, growth_values=None):
    base=base or {}
    wacc_values=wacc_values if wacc_values is not None else [.085,.09,.095,.10,.105]
    growth_values=growth_values if growth_values is not None else [.015,.02,.025,.03,.035]
    return pd.DataFrame([[dcf(**{**base,'wacc':w,'terminal_growth':g})['price_per_share'] if w>g else np.nan for g in growth_values] for w in wacc_values],index=wacc_values,columns=growth_values)

def peer_multiples(peers):
    df=pd.DataFrame(peers).copy()
    df['ev_ebitda']=df['enterprise_value']/df['ebitda']
    df['pe']=df['market_cap']/df['net_income']
    return df
