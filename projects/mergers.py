"""Simplified EPS accretion/dilution model. Illustrative only."""
import pandas as pd

def deal_model(acquirer_net_income=600,acquirer_shares=200,acquirer_share_price=45,
               target_net_income=110,target_equity_purchase_price=1500,
               stock_pct=.4,borrow_rate=.065,tax_rate=.25,pretax_synergies=30):
    if acquirer_shares<=0 or acquirer_share_price<=0 or not 0<=stock_pct<=1:raise ValueError('Invalid deal assumptions')
    new_shares=target_equity_purchase_price*stock_pct/acquirer_share_price
    debt=target_equity_purchase_price*(1-stock_pct)
    after_tax_interest=debt*borrow_rate*(1-tax_rate)
    after_tax_synergies=pretax_synergies*(1-tax_rate)
    proforma_income=acquirer_net_income+target_net_income+after_tax_synergies-after_tax_interest
    old_eps=acquirer_net_income/acquirer_shares
    new_eps=proforma_income/(acquirer_shares+new_shares)
    return {'standalone_eps':old_eps,'proforma_eps':new_eps,'accretion_pct':new_eps/old_eps-1,
            'new_shares':new_shares,'new_debt':debt,'after_tax_synergies':after_tax_synergies,'after_tax_interest':after_tax_interest}

def scenarios():
    return pd.DataFrame([{'stock_pct':x,'pretax_synergies':s,**deal_model(stock_pct=x,pretax_synergies=s)} for x in [0,.25,.5,.75,1] for s in [0,20,40,60]])
