"""Explainable risk-rule demonstrator on SYNTHETIC, non-personal customer records.
Not a production AML tool, regulated advice, or an allegation of misconduct.
"""
import pandas as pd

def score_customers(customers):
    df=pd.DataFrame(customers).copy()
    required={'customer_id','monthly_transactions','cash_ratio','high_risk_jurisdiction','pep','days_since_kyc'}
    if not required.issubset(df.columns): raise ValueError(f'Missing fields: {required-set(df.columns)}')
    df['high_volume_flag']=(df.monthly_transactions>=100).astype(int)
    df['cash_intensity_flag']=(df.cash_ratio>=.6).astype(int)
    df['jurisdiction_flag']=df.high_risk_jurisdiction.astype(int)
    df['pep_flag']=df.pep.astype(int)
    df['stale_kyc_flag']=(df.days_since_kyc>365).astype(int)
    df['score']=20*df.high_volume_flag+20*df.cash_intensity_flag+25*df.jurisdiction_flag+20*df.pep_flag+15*df.stale_kyc_flag
    df['tier']=pd.cut(df.score,[-1,24,59,100],labels=['Low','Review','Priority'])
    df['reason_codes']=df.apply(lambda row:', '.join([col.replace('_flag','') for col in ['high_volume_flag','cash_intensity_flag','jurisdiction_flag','pep_flag','stale_kyc_flag'] if row[col]]) or 'No flags',axis=1)
    return df.sort_values('score',ascending=False)

def sample_customers():
    return pd.DataFrame([
        ['SYN-001',35,.1,False,False,100],['SYN-002',120,.7,True,False,480],
        ['SYN-003',22,.2,False,True,600],['SYN-004',240,.8,True,True,800],
        ['SYN-005',80,.45,False,False,240],['SYN-006',101,.05,False,False,50]],
        columns=['customer_id','monthly_transactions','cash_ratio','high_risk_jurisdiction','pep','days_since_kyc'])
