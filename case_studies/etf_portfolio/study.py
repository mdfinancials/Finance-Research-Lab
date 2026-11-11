"""VOO, VXUS, QQQ asset allocation study. SYNTHETIC returns, not an ETF backtest."""
import numpy as np
from projects.portfolio import metrics, rebalance_returns, min_variance_weights
TICKERS=("VOO","VXUS","QQQ")
ALLOCATION={"VOO":.45,"VXUS":.35,"QQQ":.20}
ANNUAL_RETURN=np.array([.075,.065,.085])  # scenario assumptions, not forecasts
ANNUAL_VOL=np.array([.18,.20,.25])
CORR=np.array([[1.,.72,.88],[.72,1.,.65],[.88,.65,1.]])
def analyse(months=120,seed=42):
    if months<24: raise ValueError("Minimum 24 synthetic observations")
    rng=np.random.default_rng(seed)
    cov=np.outer(ANNUAL_VOL,ANNUAL_VOL)*CORR/12
    synthetic=rng.multivariate_normal(ANNUAL_RETURN/12,cov,size=months)
    weights=np.array(list(ALLOCATION.values()))
    portfolio=rebalance_returns(synthetic,weights)
    return {"summary":metrics(portfolio,benchmark=synthetic[:,0]),
            "min_variance_weights":min_variance_weights(synthetic),
            "stress_loss":float(weights@np.array([-.30,-.25,-.40]))}
if __name__=="__main__":
    print("SIMULATED, NOT HISTORICAL ETF PERFORMANCE",analyse())
