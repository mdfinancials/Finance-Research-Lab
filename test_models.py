import numpy as np
from projects.valuation import dcf,sensitivity
from projects.portfolio import metrics,min_variance_weights
from projects.kyc import score_customers,sample_customers
from projects.fixed_income import bond_analytics,shock_table
from projects.mergers import deal_model

def test_dcf():
    v=dcf();assert v['enterprise_value']>0
    assert np.isclose(v['equity_value'],v['enterprise_value']-300)
    assert dcf(wacc=.08)['price_per_share']>dcf(wacc=.11)['price_per_share']
    assert sensitivity().shape==(5,5)

def test_portfolio():
    r=np.array([.01,.02,-.01,.015]); m=metrics(r)
    assert m['max_drawdown']<0
    rng=np.random.default_rng(1);weights=min_variance_weights(rng.normal(size=(50,3)))
    assert np.isclose(weights.sum(),1) and np.all(weights>=-1e-8)

def test_kyc():
    scored=score_customers(sample_customers())
    assert scored.iloc[0]['customer_id']=='SYN-004'
    assert scored.score.between(0,100).all()

def test_bonds():
    bond=bond_analytics(coupon_rate=.05,yield_rate=.05)
    assert np.isclose(bond['price'],1000)
    shocks=shock_table();assert shocks.iloc[0].bond_price>shocks.iloc[-1].bond_price

def test_deal():
    d=deal_model(); assert np.isclose(d['accretion_pct'],d['proforma_eps']/d['standalone_eps']-1)
    assert deal_model(pretax_synergies=80)['accretion_pct']>d['accretion_pct']
