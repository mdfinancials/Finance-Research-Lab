"""Annual-coupon fixed-rate bond analytics with parallel yield shocks."""
import numpy as np
import pandas as pd

def bond_analytics(face=1000,coupon_rate=.045,yield_rate=.05,years=8):
    if years<1 or int(years)!=years or yield_rate<=-1: raise ValueError('Invalid maturity or yield')
    t=np.arange(1,int(years)+1)
    cf=np.full(len(t),face*coupon_rate,dtype=float);cf[-1]+=face
    pv=cf/(1+yield_rate)**t
    price=pv.sum()
    mac_duration=float(np.sum(t*pv)/price)
    mod_duration=mac_duration/(1+yield_rate)
    convexity=float(np.sum(t*(t+1)*pv)/(price*(1+yield_rate)**2))
    return {'price':float(price),'macaulay_duration':mac_duration,'modified_duration':mod_duration,'convexity':convexity,'cashflows':pd.DataFrame({'year':t,'cash_flow':cf,'present_value':pv})}

def shock_table(base_yield=.05,shocks_bps=(-200,-100,-50,0,50,100,200),**kwargs):
    base=bond_analytics(yield_rate=base_yield,**kwargs)['price']
    rows=[]
    for bps in shocks_bps:
        price=bond_analytics(yield_rate=base_yield+bps/10000,**kwargs)['price']
        rows.append({'yield_change_bps':bps,'bond_price':price,'price_change_pct':price/base-1})
    return pd.DataFrame(rows)
