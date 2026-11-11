"""Yahoo Finance-backed NVIDIA analysis. No fabricated historical financials.

Usage from repository root:
    python -m case_studies.nvidia_three_statement.yahoo_research

The yfinance library retrieves Yahoo Finance's normalized annual financial statements
and historical share prices. Data is third-party and may be delayed, incomplete
or unavailable; always cross-check material figures with NVIDIA's 10-K/10-Q.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
import math
import pandas as pd
import numpy as np

SYMBOL="NVDA"
YAHOO_URL="https://finance.yahoo.com/quote/NVDA/"
YAHOO_STATEMENTS={
    "income":"https://finance.yahoo.com/quote/NVDA/financials/",
    "balance":"https://finance.yahoo.com/quote/NVDA/balance-sheet/",
    "cashflow":"https://finance.yahoo.com/quote/NVDA/cash-flow/",
    "price":"https://finance.yahoo.com/quote/NVDA/history/",
}
# Different Yahoo Finance versions can change index terminology.
FIELDS={
    "revenue":("Total Revenue","Operating Revenue"),
    "ebit":("Operating Income",),
    "net_income":("Net Income","Net Income Common Stockholders"),
    "tax":("Tax Provision",),
    "pretax":("Pretax Income",),
    "cash":("Cash And Cash Equivalents","Cash Cash Equivalents And Short Term Investments"),
    "investments":("Other Short Term Investments","Short Term Investments"),
    "debt":("Total Debt",),
    "assets":("Total Assets",),
    "liabilities":("Total Liabilities Net Minority Interest","Total Liabilities"),
    "equity":("Stockholders Equity","Total Equity Gross Minority Interest"),
    "cfo":("Operating Cash Flow","Cash Flow From Continuing Operating Activities"),
    "capex":("Capital Expenditure",),
    "da":("Depreciation And Amortization","Depreciation Amortization Depletion"),
    "shares":("Diluted Average Shares",),
}
class YahooDataError(RuntimeError):
    pass

def _lookup(table:pd.DataFrame,names,period):
    if table.empty or period not in table.columns:
        return None
    for name in names:
        if name in table.index:
            val=table.loc[name,period]
            if isinstance(val,pd.Series):
                val=val.iloc[0]
            if pd.notna(val):
                return float(val)
    return None

def normalise_statements(income,balance,cashflow):
    """Annual data in US$ millions; diluted shares in millions. No gap filling."""
    if income.empty:
        raise YahooDataError("Yahoo Finance returned no annual income statement.")
    periods=sorted(income.columns,reverse=True)[:4]
    result=[]
    for period in periods:
        row={"fiscal_year_end":str(pd.Timestamp(period).date())}
        for field,names in FIELDS.items():
            table=income if field in ("revenue","ebit","net_income","tax","pretax","shares") else (balance if field in ("cash","investments","debt","assets","liabilities","equity") else cashflow)
            value=_lookup(table,names,period)
            row[field]=(value/1e6) if value is not None else np.nan
        if pd.notna(row["capex"]): row["capex"]=abs(row["capex"])
        if pd.notna(row["cfo"]) and pd.notna(row["capex"]):
            row["fcf_reported_proxy"]=row["cfo"]-row["capex"]
        else:
            row["fcf_reported_proxy"]=np.nan
        row["bs_difference"]=(row["assets"]-row["liabilities"]-row["equity"]
              if all(pd.notna(row[x]) for x in ("assets","liabilities","equity")) else np.nan)
        result.append(row)
    return pd.DataFrame(result).sort_values("fiscal_year_end").reset_index(drop=True)

def load_yahoo(symbol=SYMBOL):
    try:
        import yfinance as yf
        ticker=yf.Ticker(symbol)
        income=ticker.income_stmt
        balance=ticker.balance_sheet
        cash=ticker.cash_flow
        prices=ticker.history(period="1y",auto_adjust=False)
    except Exception as exc:
        raise YahooDataError(f"Unable to retrieve Yahoo Finance data: {exc}") from exc
    annual=normalise_statements(income,balance,cash)
    if prices.empty or "Close" not in prices.columns:
        raise YahooDataError("Yahoo Finance historical share prices were unavailable.")
    series=prices[["Close"]].dropna().copy()
    series.index=pd.to_datetime(series.index).tz_localize(None) if getattr(series.index,"tz",None) is not None else series.index
    series=series.sort_index()
    close=float(series["Close"].iloc[-1])
    as_of=str(series.index[-1].date())
    return {"annual":annual,"prices":series,"price":close,"price_date":as_of,
            "retrieved_utc":pd.Timestamp.now(tz="UTC").isoformat(),"symbol":symbol}

@dataclass(frozen=True)
class ForecastDrivers:
    revenue_growth:tuple=(.35,.25,.20,.15,.12)
    operating_margin:tuple=(.57,.55,.53,.51,.50)
    tax_rate:float=.17
    da_ratio:float=.015
    capex_ratio:float=.035
    net_working_capital_ratio:float=.08
    wacc:float=.105
    terminal_growth:float=.035

def project_fcff(latest_revenue_m,drivers=ForecastDrivers()):
    """FCFF from EBIT(1-t)+D&A-capex-incremental operating NWC.

    The NWC ratio is illustrative, NOT directly sourced from Yahoo; scenario
    operating margins and all drivers are analyst assumptions.
    """
    if latest_revenue_m<=0 or not 0<=drivers.terminal_growth<drivers.wacc:
        raise ValueError("Revenue must be positive and WACC > terminal growth.")
    if any(len(seq)!=5 for seq in (drivers.revenue_growth,drivers.operating_margin)):
        raise ValueError("Five revenue growth and five operating margin inputs required.")
    result=[]
    prev=float(latest_revenue_m)
    for i,(growth,margin) in enumerate(zip(drivers.revenue_growth,drivers.operating_margin),1):
        revenue=prev*(1+growth)
        ebit=revenue*margin
        da=revenue*drivers.da_ratio
        capex=revenue*drivers.capex_ratio
        change_nwc=(revenue-prev)*drivers.net_working_capital_ratio
        fcff=ebit*(1-drivers.tax_rate)+da-capex-change_nwc
        result.append(dict(year=i,revenue=revenue,ebit=ebit,da=da,capex=capex,
                           change_nwc=change_nwc,fcff=fcff))
        prev=revenue
    return pd.DataFrame(result)

def dcf_from_yahoo(snapshot,drivers=ForecastDrivers(),shares_m=None):
    annual=snapshot["annual"].dropna(subset=["revenue"]).sort_values("fiscal_year_end")
    if annual.empty:
        raise YahooDataError("Yahoo Finance did not provide annual revenue.")
    latest=annual.iloc[-1]
    if shares_m is None:
        shares_m=latest.get("shares",np.nan)
    if not pd.notna(shares_m) or float(shares_m)<=0:
        raise YahooDataError("Yahoo Finance did not provide diluted average shares: enter a verified share count.")
    years=project_fcff(float(latest["revenue"]),drivers)
    pv=sum(float(r.fcff)/(1+drivers.wacc)**int(r.year) for r in years.itertuples())
    tv=float(years.iloc[-1].fcff)*(1+drivers.terminal_growth)/(drivers.wacc-drivers.terminal_growth)
    pv_terminal=tv/(1+drivers.wacc)**len(years)
    ev=pv+pv_terminal
    if pd.isna(latest.get("cash",np.nan)) or pd.isna(latest.get("debt",np.nan)):
        raise YahooDataError("Cash or debt missing. Cannot calculate equity valuation reliably.")
    investments=latest.get("investments",np.nan)
    if pd.isna(investments):
        investments=0.0
        investments_note="Short-term investments missing from Yahoo; treated as zero and potentially understates equity value."
    else:
        investments_note=""
    net_cash=float(latest["cash"])+float(investments)-float(latest["debt"])
    equity=ev+net_cash
    price=equity/float(shares_m)
    return {"forecast":years,"enterprise_value_m":ev,"net_cash_m":net_cash,
            "equity_value_m":equity,"value_per_share":price,
            "reference_close":snapshot["price"],"reference_date":snapshot["price_date"],
            "implied_upside_pct":(price/snapshot["price"]-1)*100,
            "terminal_pv_pct":pv_terminal/ev*100,
            "shares_m":float(shares_m),"investments_note":investments_note}

def scenario_table(snapshot,shares_m=None):
    base=ForecastDrivers()
    inputs={
        "Bear":ForecastDrivers(revenue_growth=(.22,.16,.12,.10,.08),
           operating_margin=(.51,.49,.48,.47,.46),wacc=.125,terminal_growth=.025),
        "Base":base,
        "Bull":ForecastDrivers(revenue_growth=(.43,.32,.25,.18,.14),
           operating_margin=(.60,.59,.57,.55,.53),wacc=.09,terminal_growth=.04)
    }
    result=[]
    for name,drivers in inputs.items():
        row=dcf_from_yahoo(snapshot,drivers,shares_m)
        result.append({"scenario":name,"wacc":drivers.wacc,
          "terminal_growth":drivers.terminal_growth,
          "value_per_share_usd":row["value_per_share"],
          "upside_to_yahoo_close_pct":row["implied_upside_pct"],
          "terminal_value_pct":row["terminal_pv_pct"]})
    return pd.DataFrame(result)

def sensitivity_table(snapshot,shares_m=None):
    rows=[]
    for wacc in (.09,.10,.105,.11,.12,.13):
        for growth in (.02,.025,.03,.035,.04):
            drivers=ForecastDrivers(wacc=wacc,terminal_growth=growth)
            r=dcf_from_yahoo(snapshot,drivers,shares_m)
            rows.append({"wacc":wacc,"terminal_growth":growth,"value_per_share_usd":r["value_per_share"]})
    return pd.DataFrame(rows).pivot(index="wacc",columns="terminal_growth",values="value_per_share_usd")

if __name__=="__main__":
    snapshot=load_yahoo()
    print(snapshot["annual"].to_string(index=False))
    print("Yahoo closing price:",snapshot["price"],"as of",snapshot["price_date"])
    print(scenario_table(snapshot).to_string(index=False))
