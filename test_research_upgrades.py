"""Deterministic, offline regression tests for the two research upgrades."""
import numpy as np
import pandas as pd
from case_studies.etf_portfolio.historical_backtest import (
    monthly_returns, historical_backtest, minimum_variance,
    maximum_sharpe, efficient_frontier, PortfolioDataError,
)
from case_studies.nvidia_three_statement.research_report import build_nvidia_research_pdf
from test_yahoo_research import fixture as nvidia_fixture

def synthetic_daily_prices():
    """Testing-only prices; these are not presented as observed ETF data."""
    rng=np.random.default_rng(2026)
    dates=pd.bdate_range("2021-01-04",periods=1450)
    changes=rng.normal(loc=[.0004,.00025,.0006],scale=[.012,.010,.016],size=(len(dates),3))
    return pd.DataFrame(100*np.exp(np.cumsum(changes,axis=0)),index=dates,
                        columns=["VOO","VXUS","QQQ"])

def test_portfolio_historical_engine():
    prices=synthetic_daily_prices()
    m=monthly_returns(prices)
    assert len(m)>=24
    assert (m.columns==["VOO","VXUS","QQQ"]).all()
    report=historical_backtest(prices,[.45,.35,.20],.035)
    assert len(report["wealth"])==len(m)
    assert report["wealth"].notna().all().all()
    assert np.isclose(report["minimum_variance_weights"].sum(),1,atol=1e-6)
    assert np.isclose(report["maximum_sharpe_weights"].sum(),1,atol=1e-6)
    assert np.all(report["minimum_variance_weights"]>=-1e-8)
    assert np.all(report["maximum_sharpe_weights"]>=-1e-8)
    assert len(report["frontier"])>=10
    assert len(report["points"])==6
    assert -1<=report["max_drawdown"]<=0

def test_user_weights_and_cost_effects():
    prices=synthetic_daily_prices()
    zero=historical_backtest(prices,[1,0,0],fee_bps=0)
    fee=historical_backtest(prices,[1,0,0],fee_bps=10)
    assert np.isclose(zero["cagr"],zero["benchmark_cagr"],atol=1e-8)
    assert fee["cagr"]<zero["cagr"]
    try:
        historical_backtest(prices,[.7,.5,-.2])
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid weights should be rejected")

def test_downloadable_nvidia_pdf():
    pdf=build_nvidia_research_pdf(nvidia_fixture())
    assert pdf.startswith(b"%PDF-")
    assert len(pdf)>9000
