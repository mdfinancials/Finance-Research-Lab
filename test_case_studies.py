"""Regression tests across five applied finance case studies.
Run from repository root: python -m pytest -q
"""
import numpy as np
import pytest
from case_studies.nvidia_three_statement.model import forecast
from case_studies.nvidia_three_statement.valuation_case import value_case,sensitivity
from case_studies.etf_portfolio.study import analyse as etf_analyse
from case_studies.kyc_triage.study import evaluate as kyc_evaluate
from case_studies.treasury_duration.study import analyse as bond_analyse
from case_studies.ma_acquisition.study import analyse as deal_analyse,matrix

def test_nvidia_statements_balance():
    rows=forecast()
    assert len(rows)==3
    assert [r["year"] for r in rows]==[2027,2028,2029]
    for row in rows:
        assert abs(row["bs_check"])<1e-5
        assert abs(row["cashflow_check"])<1e-5

def test_nvidia_dcf_scenarios_and_sensitivity():
    bear=value_case("bear")
    base=value_case("base")
    bull=value_case("bull")
    assert 0<bear["value_per_share_usd"]<base["value_per_share_usd"]<bull["value_per_share_usd"]
    assert base["terminal_pv_share"]>0
    assert len(sensitivity())==25
    assert value_case(wacc=.12)["value_per_share_usd"]<value_case(wacc=.10)["value_per_share_usd"]

def test_etf_risk_and_weights():
    r=etf_analyse()
    assert abs(sum(r["min_variance_weights"])-1)<1e-6
    assert np.all(r["min_variance_weights"]>=-1e-8)
    assert r["stress_loss"]<0
    assert r["summary"]["volatility"]>0

def test_kyc_explainable_review():
    r=kyc_evaluate()
    assert len(r["review_queue"])==6
    assert sum(r["confusion_matrix"].values())==6
    assert 0<=r["precision"]<=1
    assert 0<=r["recall"]<=1

def test_bond_yield_price_inverse():
    low=bond_analyse(.04)
    high=bond_analyse(.06)
    assert low["base_price"]>high["base_price"]
    assert high["duration"]>0
    assert len(high["scenarios"])==7

def test_merger_synergy_accretion():
    low=deal_analyse(pretax_synergies=0)
    high=deal_analyse(pretax_synergies=80)
    assert high["accretion_pct"]>low["accretion_pct"]
    assert len(matrix())==25
