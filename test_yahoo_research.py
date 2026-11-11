"""Offline tests of Yahoo-backed NVIDIA analysis; no network calls in CI."""
import numpy as np
import pandas as pd
import pytest
from case_studies.nvidia_three_statement.yahoo_research import (
    normalise_statements,project_fcff,dcf_from_yahoo,scenario_table,sensitivity_table,
    YahooDataError,ForecastDrivers
)
PERIOD=pd.Timestamp("2026-01-25")
def fixture():
    is_=pd.DataFrame({PERIOD:{"Total Revenue":215938e6,"Operating Income":130387e6,
           "Net Income":120067e6,"Diluted Average Shares":24514e6}})
    bs=pd.DataFrame({PERIOD:{"Cash And Cash Equivalents":10605e6,
           "Other Short Term Investments":51951e6,"Total Debt":8468e6,
           "Total Assets":206803e6,"Total Liabilities Net Minority Interest":49510e6,
           "Stockholders Equity":157293e6}})
    cf=pd.DataFrame({PERIOD:{"Operating Cash Flow":102718e6,
           "Capital Expenditure":-6042e6}})
    annual=normalise_statements(is_,bs,cf)
    return {"annual":annual,"price":175.94,"price_date":"2026-11-11"}
def test_historical_values_preserved():
    row=fixture()["annual"].iloc[0]
    assert row["revenue"]==215938
    assert row["capex"]==6042
    assert row["shares"]==24514
    assert abs(row["bs_difference"])<.01
def test_fcff_and_sensitivity():
    snapshot=fixture()
    report=dcf_from_yahoo(snapshot)
    assert len(report["forecast"])==5
    assert report["value_per_share"]>0
    assert scenario_table(snapshot).shape[0]==3
    assert sensitivity_table(snapshot).shape==(6,5)
    assert dcf_from_yahoo(snapshot,ForecastDrivers(wacc=.12))["value_per_share"]<report["value_per_share"]
def test_missing_history_errors():
    with pytest.raises(YahooDataError):normalise_statements(pd.DataFrame(),pd.DataFrame(),pd.DataFrame())
