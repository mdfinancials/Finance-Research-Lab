"""Historical ETF portfolio research using Yahoo Finance adjusted closing prices.

Optimized portfolios are in-sample, hindsight illustrations; never imply they were
investable historical trading strategies. The user-weighted historical backtest
uses fixed, specified weights and monthly rebalancing (before costs).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize

TICKERS=("VOO","VXUS","QQQ")
SOURCE="Yahoo Finance (via yfinance), auto-adjusted closing prices"
class PortfolioDataError(RuntimeError):
    """Market data unavailable, malformed, or too short for honest comparison."""

def normalise_prices(raw, tickers=TICKERS):
    """Accept either ordering of yfinance MultiIndex columns, or flat Close."""
    if raw is None or raw.empty:
        raise PortfolioDataError("Yahoo Finance did not return adjusted ETF prices.")
    if isinstance(raw.columns,pd.MultiIndex):
        if "Close" in raw.columns.get_level_values(0):
            prices=raw["Close"]
        elif "Close" in raw.columns.get_level_values(1):
            prices=raw.xs("Close",axis=1,level=1)
        else:
            raise PortfolioDataError("The download did not contain closing prices.")
    else:
        prices=raw
    if not all(t in prices.columns for t in tickers):
        raise PortfolioDataError("The download omitted one or more ETFs.")
    prices=prices.loc[:,list(tickers)].apply(pd.to_numeric,errors="coerce")
    prices.index=pd.to_datetime(prices.index,utc=True).tz_localize(None)
    prices=prices.sort_index()
    prices=prices[~prices.index.duplicated(keep="last")].dropna(how="any")
    prices=prices.loc[(prices>0).all(axis=1)]
    if len(prices)<510:
        raise PortfolioDataError("At least approximately two years of common trading history are required.")
    return prices

def load_adjusted_prices(period="5y"):
    if period not in {"3y","5y","10y"}:
        raise ValueError("Supported history windows: 3y, 5y, 10y")
    try:
        import yfinance as yf
        raw=yf.download(list(TICKERS),period=period,interval="1d",
                        auto_adjust=True,progress=False,threads=False)
        prices=normalise_prices(raw)
    except PortfolioDataError:
        raise
    except Exception as exc:
        raise PortfolioDataError("Yahoo Finance request failed: "+str(exc)) from exc
    return prices

def monthly_returns(prices):
    """Month-end adjusted close; first month is the first complete transition."""
    p=normalise_prices(prices) if len(prices)>100 else prices.copy()
    month_end=p.resample("ME").last().dropna(how="any")
    # Do not mistake an in-progress calendar month for a completed month.
    current_month=pd.Timestamp.now(tz="UTC").tz_localize(None).to_period("M")
    if not month_end.empty and month_end.index[-1].to_period("M")==current_month:
        month_end=month_end.iloc[:-1]
    if len(month_end)<25:
        raise PortfolioDataError("Insufficient monthly observations for a meaningful backtest.")
    returns=month_end.pct_change(fill_method=None).iloc[1:]
    if returns.isna().any().any() or (returns <= -1).any().any():
        raise PortfolioDataError("Invalid adjusted-return series.")
    return returns

def _weights(values):
    w=np.asarray(values,dtype=float)
    if w.shape!=(len(TICKERS),) or not np.isfinite(w).all() or np.min(w)<-1e-9 or abs(w.sum()-1)>1e-7:
        raise ValueError("Provide three nonnegative weights summing to 100%.")
    return w

def _moments(returns):
    if len(returns)<24 or returns.isna().any().any():
        raise PortfolioDataError("Need 24 or more valid monthly return observations.")
    mu=returns.mean().to_numpy()*12
    cov=returns.cov().to_numpy()*12
    if not np.isfinite(mu).all() or not np.isfinite(cov).all():
        raise PortfolioDataError("Return or covariance estimate is invalid.")
    return mu,cov

def portfolio_point(w,mu,cov,risk_free=.035):
    ret=float(w@mu)
    vol=float(np.sqrt(max(w@cov@w,0)))
    return {"annual_return":ret,"annual_volatility":vol,
            "sharpe":(ret-risk_free)/vol if vol>0 else np.nan}

def minimum_variance(returns):
    mu,cov=_moments(returns)
    n=len(mu)
    sol=minimize(lambda w: float(w@cov@w),np.ones(n)/n,
                 bounds=[(0.,1.)]*n,
                 constraints=[{"type":"eq","fun":lambda w:float(w.sum()-1)}],
                 method="SLSQP",options={"maxiter":1500,"ftol":1e-11})
    if not sol.success:
        raise PortfolioDataError("Minimum-variance optimiser failed: "+sol.message)
    w=np.clip(sol.x,0,1);return w/w.sum()

def maximum_sharpe(returns,risk_free=.035):
    mu,cov=_moments(returns)
    starts=[np.ones(len(mu))/len(mu)]+[np.eye(len(mu))[i] for i in range(len(mu))]
    solutions=[]
    for guess in starts:
        sol=minimize(lambda w: -portfolio_point(w,mu,cov,risk_free)["sharpe"],
                     guess,bounds=[(0.,1.)]*len(mu),
                     constraints=[{"type":"eq","fun":lambda w:float(w.sum()-1)}],
                     method="SLSQP",options={"maxiter":1500,"ftol":1e-11})
        if sol.success and np.isfinite(sol.fun):
            w=np.clip(sol.x,0,1);w=w/w.sum()
            solutions.append((float(-sol.fun),w))
    if not solutions:
        raise PortfolioDataError("Maximum-Sharpe optimiser did not converge.")
    return max(solutions,key=lambda r:r[0])[1]

def efficient_frontier(returns,risk_free=.035,points=31):
    mu,cov=_moments(returns)
    lo=int(np.argmin(mu));hi=int(np.argmax(mu))
    targets=np.linspace(float(mu[lo]),float(mu[hi]),points)
    frontier=[]
    for target in targets:
        weight_hi=(target-mu[lo])/(mu[hi]-mu[lo]) if mu[hi]>mu[lo] else 0
        seed=np.zeros(len(mu));seed[lo]=1-weight_hi;seed[hi]+=weight_hi
        cons=[{"type":"eq","fun":lambda w:float(w.sum()-1)},
              {"type":"eq","fun":lambda w,m=target:float(w@mu-m)}]
        sol=minimize(lambda w:float(w@cov@w),seed,
                     bounds=[(0.,1.)]*len(mu),constraints=cons,
                     method="SLSQP",options={"maxiter":1200,"ftol":1e-10})
        if sol.success:
            w=np.clip(sol.x,0,1)
            w=w/w.sum()
            point=portfolio_point(w,mu,cov,risk_free)
            frontier.append({"risk_pct":100*point["annual_volatility"],
                             "return_pct":100*point["annual_return"],
                             **{t:float(w[i]) for i,t in enumerate(TICKERS)}})
    if len(frontier)<max(5,points//3):
        raise PortfolioDataError("Efficient-frontier optimisation produced too few valid solutions.")
    return pd.DataFrame(frontier).sort_values("risk_pct")

def historical_backtest(prices,weights=(.45,.35,.20),risk_free=.035,fee_bps=0.):
    """Historical fixed-weight return series, monthly rebalanced.

    Fee assumption is deducted at each monthly rebalance and is an illustrative
    per-month charge, NOT an exact trade-by-trade expense model.
    Optimized weights use the *entire* observed window and are in-sample only.
    """
    w=_weights(weights)
    if risk_free<0 or risk_free>.20 or fee_bps<0 or fee_bps>100:
        raise ValueError("Check risk-free rate and monthly cost assumptions.")
    returns=monthly_returns(prices)
    monthly_fee=fee_bps/10000
    simulated=(returns@w)-monthly_fee
    benchmark=returns["VOO"]
    wealth=pd.DataFrame({"Selected portfolio":(1+simulated).cumprod(),
                         "VOO benchmark":(1+benchmark).cumprod()})
    wealth.index.name="Date"
    n=len(simulated)
    years=n/12
    terminal=float(wealth["Selected portfolio"].iloc[-1])
    cagr=terminal**(1/years)-1 if terminal>0 else -1.
    vol=float(simulated.std(ddof=1)*np.sqrt(12))
    sharpe=float((simulated.mean()*12-risk_free)/vol) if vol>0 else np.nan
    wealth_for_dd=pd.concat([pd.Series([1.0]),wealth["Selected portfolio"].reset_index(drop=True)],ignore_index=True)
    dd=float((wealth_for_dd/wealth_for_dd.cummax()-1).min())
    mu,cov=_moments(returns)
    min_w=minimum_variance(returns)
    max_w=maximum_sharpe(returns,risk_free)
    frontier=efficient_frontier(returns,risk_free)
    points=[]
    for label,weights_ in [("Selected",w),("Minimum variance",min_w),("Maximum Sharpe",max_w)]:
        stats=portfolio_point(weights_,mu,cov,risk_free)
        points.append({"Portfolio":label,"Risk (%)":100*stats["annual_volatility"],
                       "Return (%)":100*stats["annual_return"],
                       **{t:float(weights_[i]) for i,t in enumerate(TICKERS)}})
    for idx,ticker in enumerate(TICKERS):
        aw=np.eye(len(TICKERS))[idx]
        stats=portfolio_point(aw,mu,cov,risk_free)
        points.append({"Portfolio":ticker,"Risk (%)":100*stats["annual_volatility"],
                       "Return (%)":100*stats["annual_return"],
                       **{t:float(aw[i]) for i,t in enumerate(TICKERS)}})
    return {"prices":prices,"monthly_returns":returns,"wealth":wealth,
            "cagr":cagr,"annual_volatility":vol,"sharpe":sharpe,"max_drawdown":dd,
            "frontier":frontier,"points":pd.DataFrame(points),
            "minimum_variance_weights":min_w,"maximum_sharpe_weights":max_w,
            "selected_weights":w,"benchmark_cagr":float(wealth["VOO benchmark"].iloc[-1]**(1/years)-1),
            "period_start":str(returns.index[0].date()),"period_end":str(returns.index[-1].date()),
            "last_price_date":str(prices.index[-1].date()),"months":n,
            "fee_bps":fee_bps,"risk_free":risk_free}
