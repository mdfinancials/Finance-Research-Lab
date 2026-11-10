"""No-lookahead demo portfolio attribution. Synthetic scenario data by default."""
import numpy as np
import pandas as pd

def metrics(returns, benchmark=None, annualization=12, risk_free_annual=.03):
    r=pd.Series(returns,dtype=float).dropna()
    if len(r)<2: raise ValueError('Need at least two observations')
    wealth=(1+r).cumprod(); years=len(r)/annualization
    cagr=float(wealth.iloc[-1]**(1/years)-1) if wealth.iloc[-1]>0 else -1.
    vol=float(r.std(ddof=1)*np.sqrt(annualization))
    sharpe=float((r.mean()*annualization-risk_free_annual)/vol) if vol>0 else np.nan
    dd=float((wealth/wealth.cummax()-1).min())
    out={'cagr':cagr,'volatility':vol,'sharpe':sharpe,'max_drawdown':dd,'cumulative_return':float(wealth.iloc[-1]-1)}
    if benchmark is not None:
        aligned=pd.concat([r,pd.Series(benchmark,dtype=float)],axis=1).dropna()
        aligned.columns=['portfolio','benchmark']
        if len(aligned)>1 and aligned.benchmark.var()>0:
            beta=float(aligned.portfolio.cov(aligned.benchmark)/aligned.benchmark.var())
            out['beta']=beta
            out['alpha_annual_approx']=float((aligned.portfolio.mean()-beta*aligned.benchmark.mean())*annualization-(1-beta)*risk_free_annual)
    return out

def min_variance_weights(returns, long_only=True):
    """Constrained minimum variance using scipy; weights sum to 1."""
    from scipy.optimize import minimize
    cov=pd.DataFrame(returns).cov().to_numpy()*12
    n=len(cov)
    if n<2: raise ValueError('Need two assets')
    sol=minimize(lambda w: float(w@cov@w),np.ones(n)/n,
                 bounds=[(0,1) if long_only else (None,None)]*n,
                 constraints=[{'type':'eq','fun':lambda w: w.sum()-1}],method='SLSQP')
    if not sol.success: raise RuntimeError(sol.message)
    return sol.x

def rebalance_returns(asset_returns,weights):
    """Constant mix assumes rebalancing at every return observation; excludes costs."""
    a=pd.DataFrame(asset_returns)
    w=np.asarray(weights,dtype=float)
    if len(w)!=a.shape[1] or not np.isclose(w.sum(),1): raise ValueError('Weights must match assets and sum to one')
    return a@w
