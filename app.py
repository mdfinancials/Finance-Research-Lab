"""Interactive finance portfolio. Run: streamlit run app.py"""
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from case_studies.etf_portfolio.historical_backtest import load_adjusted_prices, historical_backtest, PortfolioDataError
from case_studies.nvidia_three_statement.research_report import build_nvidia_research_pdf
from projects.valuation import dcf,sensitivity
from projects.portfolio import metrics,rebalance_returns,min_variance_weights
from projects.kyc import score_customers,sample_customers
from projects.fixed_income import bond_analytics,shock_table
from projects.mergers import deal_model,scenarios
from case_studies.nvidia_three_statement.valuation_case import value_case as nvda_dcf, sensitivity as nvda_grid
from case_studies.etf_portfolio.study import analyse as etf_case
from case_studies.kyc_triage.study import evaluate as kyc_case
from case_studies.treasury_duration.study import analyse as bond_case
from case_studies.ma_acquisition.study import analyse as ma_case, matrix as ma_matrix
from case_studies.nvidia_three_statement.yahoo_research import load_yahoo, scenario_table, sensitivity_table, YahooDataError
from ui_components import apply_style, heading, insight, source_note, footer, downloadable_csv

st.set_page_config(page_title='Finance Research Lab',layout='wide',page_icon='📈')
apply_style()
page=st.sidebar.radio('Navigate', ['Home · Portfolio', '01 · Equity valuation','02 · Portfolio analytics','03 · KYC risk triage','04 · Fixed income','05 · M&A modelling','06 · Applied case studies','07 · NVIDIA Yahoo Finance Research','08 · Historical ETF Backtest'])
st.sidebar.divider()
st.sidebar.caption("Independent finance research • Education and scenario analysis")
st.sidebar.link_button("GitHub source code","https://github.com/mdfinancials/Finance-Research-Lab",use_container_width=True)


if page.startswith("Home"):
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Independent finance research portfolio</div>
      <h1>Finance Research Lab</h1>
      <p>Five interactive financial analysis tools and five applied case studies covering equity valuation, ETF risk, financial-crime triage, fixed income and M&amp;A.</p>
      <p style="font-size:.86rem;color:#a6ebd6">Python · Financial modelling · Scenario analysis · Research documentation</p>
    </div>
    """,unsafe_allow_html=True)
    st.write("")
    a,b,c1=st.columns(3)
    a.metric("Interactive model categories","5")
    b.metric("Applied case studies","5")
    c1.metric("Reporting standard","Assumptions disclosed")
    st.divider()
    st.subheader("About the analyst")
    st.markdown("**MD Mahdi Mahbub Rauf**  ·  Sydney, Australia")
    st.write("Bachelor of Commerce (Finance), Macquarie University. Banking experience at HSBC Australia, with exposure to customer financial needs, banking operations, and fraud and scam awareness. Interested in investment research, portfolio management, and using financial modelling to make complicated decisions easier to explain.")
    e1,e2=st.columns(2)
    with e1.container(border=True):
        st.markdown("**Education & experience**")
        st.write("B.Com. (Finance) — Macquarie University")
        st.write("Personal Banking Consultant — HSBC Australia")
        st.caption("Independent educational projects; no HSBC customer data or proprietary models are included.")
    with e2.container(border=True):
        st.markdown("**Tools & analytical methods**")
        st.write("Python · pandas · NumPy · SciPy · Streamlit · Excel")
        st.write("Three-statement modelling · DCF · Portfolio risk · Duration & convexity · EPS accretion")
        st.caption("Tools used in the projects; educational model results are not evidence of actual investment performance.")
    st.subheader("Explore the projects")
    catalog=[
      ("01 · Equity research","NVIDIA three-statement model and FCFF valuation scenarios","Reported FY2025–26 financials plus forecast assumptions","https://github.com/mdfinancials/Finance-Research-Lab/tree/main/case_studies/nvidia_three_statement"),
      ("02 · Portfolio construction","VOO / VXUS / QQQ asset allocation, volatility and stress tests","Simulated monthly returns; not investment track record","https://github.com/mdfinancials/Finance-Research-Lab/tree/main/case_studies/etf_portfolio"),
      ("03 · KYC review analytics","Explainable prioritisation with reason codes and synthetic human labels","Fully synthetic; not a regulatory decision engine","https://github.com/mdfinancials/Finance-Research-Lab/tree/main/case_studies/kyc_triage"),
      ("04 · Fixed-income risk","Bond price shocks, modified duration, convexity and curve reference","Dated public Treasury yield; hypothetical coupon bond","https://github.com/mdfinancials/Finance-Research-Lab/tree/main/case_studies/treasury_duration"),
      ("05 · M&A transaction analysis","Pro-forma EPS, funding mix, synergy break-even scenarios","Entirely fictional deal and companies","https://github.com/mdfinancials/Finance-Research-Lab/tree/main/case_studies/ma_acquisition")]
    for i in range(0,len(catalog),2):
        cols=st.columns(2)
        for j,item in enumerate(catalog[i:i+2]):
            title,description,evidence,url=item
            with cols[j].container(border=True):
                st.markdown("**"+title+"**")
                st.write(description)
                st.caption(evidence)
                st.link_button("Read case study",url,use_container_width=True)
    st.divider()
    st.subheader("NVIDIA · Yahoo Finance research")
    st.write("Explore NVIDIA financial statement data retrieved from Yahoo Finance, historical share prices, and interactive five-year DCF scenarios in the sidebar: **07 · NVIDIA Yahoo Finance Research**.")
    st.markdown("[Read the methodology on GitHub](https://github.com/mdfinancials/Finance-Research-Lab/blob/main/case_studies/nvidia_three_statement/YAHOO_FINANCE_RESEARCH.md)")
    st.subheader("Research takeaways")
    st.caption("Interpretations from the exercises; scenario results, not verified trading outcomes.")
    takeaways=[
      ("NVIDIA valuation","The implied value changes materially with WACC and long-run growth. Terminal value dependence means forecast assumptions must be justified against filings."),
      ("ETF portfolio","Adding international equities may diversify geography, but the VOO/QQQ allocation retains overlapping US large-cap exposure. Synthetic stress tests quantify the assumed downside, not real historical losses."),
      ("KYC review analytics","Explicit rule flags and reason codes support explainable triage. Even apparently strong performance on a six-row synthetic dataset cannot establish compliance or production reliability."),
      ("Fixed-income risk","As yields rise, the hypothetical bond price falls. Modified duration gives a first-order estimate; convexity helps explain nonlinear price sensitivity."),
      ("M&A transaction","Higher synergies generally improve pro-forma EPS, but accretion does not prove economic value creation without financing, integration and purchase-accounting analysis.")
    ]
    for heading,insight in takeaways:
        with st.expander(heading):
            st.write(insight)
    st.divider()
    st.subheader("How to use this portfolio")
    st.write("Select a model from the left navigation to adjust financial drivers, examine outputs, and explore the applied case studies. Source code, methodology and assumptions are linked from GitHub.")
    st.info("Educational research: outputs are not live prices, investment recommendations, client records, or validated compliance decisions. All simulations and assumptions are labelled.")

elif page.startswith('07'):
    heading("07","NVIDIA · Yahoo Finance research","Examine annual financial statements, dated historical prices and five-year discounted cash-flow scenarios.",tag="YAHOO FINANCE RESEARCH")
    source_note("Yahoo Finance via yfinance · live retrieval may be delayed or unavailable · analyst assumptions separated from reported financials")
    st.markdown("[Yahoo Finance NVDA](https://finance.yahoo.com/quote/NVDA/) · [Financial statements](https://finance.yahoo.com/quote/NVDA/financials/) · [SEC filings](https://investor.nvidia.com/financial-info/sec-filings/default.aspx)")
    st.info("Yahoo Finance data can be delayed or temporarily inaccessible. Cross-check any figures against company filings before using the model for decisions.")
    @st.cache_data(ttl=3600,show_spinner="Fetching NVIDIA data from Yahoo Finance...")
    def _get_yahoo_nvda():
        return load_yahoo()
    if st.button("Refresh Yahoo Finance data"):
        _get_yahoo_nvda.clear()
    try:
        snapshot=_get_yahoo_nvda()
        st.success(f"Data source: Yahoo Finance | Latest price date: {snapshot['price_date']} | Retrieved UTC: {snapshot['retrieved_utc'][:19]}")
        a,b,d=st.columns(3)
        a.metric("Latest available close",f"US$ {snapshot['price']:,.2f}")
        b.metric("Price date",snapshot["price_date"])
        d.metric("Financial periods",str(len(snapshot["annual"])))
        st.subheader("Historical annual statements (USD millions)")
        annual_display=snapshot["annual"].copy()
        annual_display["fiscal_year"]="FY"+annual_display["fiscal_year_end"].str.slice(0,4)
        annual_display=annual_display.rename(columns={"fiscal_year_end":"Yahoo period-end label"})
        st.caption("Yahoo often labels annual periods January 31. NVIDIA's actual fiscal year-end date may differ; refer to SEC filings. FY designation is based on the year of Yahoo's period label.")
        t1,t2=st.tabs(["Financial statements","One-year price history"])
        with t1:
            st.dataframe(annual_display,hide_index=True,use_container_width=True)
            downloadable_csv(annual_display,"nvidia_yahoo_annual_statements.csv")
        with t2:
            st.line_chart(snapshot["prices"]["Close"],height=345)
            st.caption(f"Close price, USD · latest available trading date {snapshot['price_date']}")
            downloadable_csv(snapshot["prices"].reset_index(),"nvidia_yahoo_price_history.csv")
        st.subheader("Illustrative five-year discounted cash-flow scenarios")
        st.write("The share-count input starts with Yahoo Finance's latest annual diluted weighted-average shares, not a verified current outstanding share count.")
        latest_annual=snapshot["annual"].sort_values("fiscal_year_end").iloc[-1]
        yahoo_shares=latest_annual.get("shares",float("nan"))
        if pd.isna(yahoo_shares) or float(yahoo_shares)<=0:
            st.warning("Yahoo did not provide diluted average shares. Enter a figure verified from NVIDIA filings.")
            shares=st.number_input("Verified diluted shares (millions)",min_value=1.0,max_value=100000.0,value=None,step=1.0)
            if shares is None:
                st.info("Enter a verified share-count input to enable per-share valuation.")
                st.stop()
        else:
            shares=st.number_input("Diluted shares (millions; verify against filings)",min_value=1.0,max_value=100000.0,value=float(yahoo_shares),step=10.0)
            st.caption(f"Yahoo annual diluted weighted-average shares: {float(yahoo_shares):,.0f} million. This differs from current outstanding shares.")
        scenarios_df=scenario_table(snapshot,shares_m=shares)
        scenario_display=scenarios_df.copy()
        for col in ("wacc","terminal_growth"):
            scenario_display[col]=scenario_display[col].map(lambda x:f"{x:.1%}")
        scenario_display=scenario_display.rename(columns={"scenario":"Scenario","wacc":"WACC","terminal_growth":"Terminal growth","value_per_share_usd":"Value/share (USD)","upside_to_yahoo_close_pct":"Upside vs dated close (%)","terminal_value_pct":"Terminal value share (%)"})
        m1,m2,m3=st.columns(3)
        for col,name in zip((m1,m2,m3),("Bear","Base","Bull")):
            value=float(scenarios_df.loc[scenarios_df["scenario"]==name,"value_per_share_usd"].iloc[0])
            col.metric(name+" illustrative value",f"US$ {value:,.2f}")
        insight("These values represent assumed operating performance and discount rates, not established stock-price targets. The comparison with Yahoo's last available close is scenario arithmetic, not an investment recommendation.")
        t3,t4=st.tabs(["Valuation scenarios","Sensitivity heatmap"])
        with t3:
            st.dataframe(scenario_display.round(2),hide_index=True,use_container_width=True)
            downloadable_csv(scenarios_df,"nvidia_dcf_scenarios.csv")
        with t4:
            matrix=sensitivity_table(snapshot,shares_m=shares).round(2)
            matrix.index=[f"{v:.1%}" for v in matrix.index]
            matrix.columns=[f"{v:.1%}" for v in matrix.columns]
            st.dataframe(matrix.style.format("{:,.2f}").background_gradient(cmap="Blues",axis=None),use_container_width=True)
        st.divider()
        st.subheader("NVIDIA equity research initiation report")
        st.markdown("Download an independently prepared PDF containing an investment thesis, business and industry analysis, FY2027 Q2 reported facts, DCF scenarios, catalysts, risks, diligence questions and source references.")
        st.caption("Research facts reviewed 12 November 2026. The 26 August 2026 earnings release is dated and may be superseded. The DCF uses the annual Yahoo observations above.")
        with st.expander("Research thesis and key questions"):
            st.markdown("**Thesis:** AI infrastructure deployment presents a growth opportunity, but valuation depends on capacity, profitability, geopolitics and the discount rate. Not rated; no investment recommendation.")
            st.markdown("**Key risks:** export restrictions, customer capital spending, competing accelerators, supply constraints and terminal-value sensitivity.")
            st.markdown("**Further work:** reconcile to current 10-K/10-Q, incorporate new interim results and evaluate valuation against peers.")
        try:
            pdf_bytes=build_nvidia_research_pdf(snapshot,shares_m=shares)
            st.download_button("Download NVIDIA research report (PDF)",data=pdf_bytes,
                file_name="NVIDIA_Research_Initiation_Finance_Research_Lab.pdf",
                mime="application/pdf",type="primary",use_container_width=True)
            st.caption("Generated from the current Yahoo Finance data snapshot and your selected share count.")
        except Exception as report_error:
            st.warning("PDF export is temporarily unavailable; the financial dashboard remains accessible.")
            st.caption(str(report_error))
        st.warning("Scenarios are analyst assumptions, not current price targets or recommendations. Yahoo's filing periods, missing investment lines, dilution and accounting classifications require validation.")
    except (YahooDataError,ValueError,KeyError,TypeError,IndexError) as exc:
        st.error("Yahoo Finance data cannot be used to calculate the report right now.")
        st.code(str(exc))
        st.write("Use the static NVIDIA case study while Yahoo Finance is unavailable. No replacement financial numbers have been invented.")

elif page.startswith('08'):
    heading("08","Historical ETF portfolio research","Compare historical VOO, VXUS and QQQ allocations using adjusted market prices, efficient-frontier analysis and hindsight-only optimisation.",tag="MARKET RESEARCH")
    source_note("Yahoo Finance adjusted closing prices · monthly rebalancing · USD total-return approximation")
    st.info("Historical backtests are not a record of real trades. Optimised allocations use the full selected sample and are hindsight illustrations, not out-of-sample strategies.")
    with st.container(border=True):
        st.markdown("**Research settings**")
        a,b,d=st.columns(3)
        period=a.selectbox("Historical window",["3y","5y","10y"],index=1)
        risk_free=b.slider("Risk-free assumption (%)",0.0,10.0,3.5,.5)/100
        fees=d.slider("Simplified monthly cost (bps)",0,25,0,1)
        a,b,d=st.columns(3)
        voo=a.slider("VOO allocation (%)",0,100,45)
        vxus=b.slider("VXUS allocation (%)",0,100,35)
        if voo+vxus>100:
            st.error("VOO and VXUS together must be at most 100%.")
            st.stop()
        qqq=100-voo-vxus
        d.metric("QQQ allocation",f"{qqq}%")
    @st.cache_data(ttl=3600,show_spinner="Loading adjusted ETF price history from Yahoo Finance...")
    def _etf_history(window):
        return load_adjusted_prices(window)
    if st.button("Refresh ETF history"):
        _etf_history.clear()
    try:
        prices=_etf_history(period)
        result=historical_backtest(prices,[voo/100,vxus/100,qqq/100],
                                   risk_free=risk_free,fee_bps=fees)
        st.caption(f"Yahoo adjusted closing prices through {result['last_price_date']}. Completed monthly-return sample: {result['period_start']} to {result['period_end']} ({result['months']} months).")
        a,b,d,e=st.columns(4)
        a.metric("Backtest CAGR",f"{result['cagr']:.1%}")
        b.metric("Annualised volatility",f"{result['annual_volatility']:.1%}")
        d.metric("Sharpe ratio",f"{result['sharpe']:.2f}")
        e.metric("Max drawdown",f"{result['max_drawdown']:.1%}")
        insight("The selected weights are backtested as a monthly-rebalanced historical strategy, with a simplified cost allowance. Optimised weights are fitted to the entire dataset and are NOT presented as historically achieved returns.")
        t1,t2,t3,t4=st.tabs(["Historical backtest","Efficient frontier","Allocation analysis","Data & methodology"])
        with t1:
            st.subheader("Growth of US$1 invested")
            st.line_chart(result["wealth"],height=350)
            st.caption(f"VOO-only benchmark CAGR: {result['benchmark_cagr']:.1%}. Figures are USD-based; no foreign exchange or investor tax modelling.")
            downloadable_csv(result["wealth"].reset_index(),"etf_historical_portfolio_growth.csv")
            st.subheader("Adjusted monthly ETF returns (%)")
            monthly=(100*result["monthly_returns"]).round(2)
            st.dataframe(monthly,use_container_width=True)
        with t2:
            frontier=result["frontier"]
            comparison=result["points"]
            line=alt.Chart(frontier).mark_line(color="#087f78",strokeWidth=3).encode(
                x=alt.X("risk_pct:Q",title="Annualised volatility (%)",scale=alt.Scale(zero=False)),
                y=alt.Y("return_pct:Q",title="Historical arithmetic return (% p.a.)",scale=alt.Scale(zero=False)),
                tooltip=[alt.Tooltip("risk_pct:Q",format=".2f"),
                         alt.Tooltip("return_pct:Q",format=".2f")])
            dots=alt.Chart(comparison).mark_circle(size=140,opacity=.95).encode(
                x="Risk (%):Q",y="Return (%):Q",
                color=alt.Color("Portfolio:N",legend=alt.Legend(orient="bottom")),
                tooltip=["Portfolio",alt.Tooltip("Risk (%):Q",format=".2f"),
                         alt.Tooltip("Return (%):Q",format=".2f")])
            st.altair_chart((line+dots).properties(height=385),use_container_width=True)
            st.caption("In-sample sample-moment efficient frontier. The green curve is not a prospective risk-return forecast.")
            st.dataframe(comparison.round(3),hide_index=True,use_container_width=True)
        with t3:
            allocation=pd.DataFrame({
                "ETF":["VOO","VXUS","QQQ"],
                "Selected":result["selected_weights"],
                "Minimum variance (in-sample)":result["minimum_variance_weights"],
                "Maximum Sharpe (in-sample)":result["maximum_sharpe_weights"]})
            st.bar_chart(allocation.set_index("ETF"),height=320)
            shown=allocation.copy()
            for col in shown.columns[1:]:
                shown[col]=100*shown[col]
            st.dataframe(shown.round(1),hide_index=True,use_container_width=True)
            st.caption("All allocations shown in percent. Long-only weights add to 100%. Optimisation is in-sample and subject to estimation error.")
            downloadable_csv(shown,"etf_portfolio_allocations.csv")
        with t4:
            st.markdown("**Yahoo Finance:** [VOO](https://finance.yahoo.com/quote/VOO/) · [VXUS](https://finance.yahoo.com/quote/VXUS/) · [QQQ](https://finance.yahoo.com/quote/QQQ/)")
            st.write("Price history uses auto-adjusted Yahoo Finance closing values for dividends and splits, subject to third-party data quality. Common trading days are used across all ETFs.")
            st.write("Daily series are reduced to completed calendar-month returns. Fixed weights are applied every month. The risk-free assumption is annualised; a fixed illustrative fee is deducted each month.")
            st.write("Max-Sharpe and min-variance use the same historical return sample. As such, these are hindsight comparisons, not walk-forward or live portfolio backtests.")
            st.warning("The selected backtest excludes slippage, tax, foreign-exchange costs and the timing effects of distributions. For an investable optimisation strategy, test rolling out-of-sample signals and realised turnover.")
            st.link_button("Review ETF case study","https://github.com/mdfinancials/Finance-Research-Lab/tree/main/case_studies/etf_portfolio")
    except (PortfolioDataError,ValueError,KeyError,TypeError) as exc:
        st.error("Historical ETF analysis is temporarily unavailable.")
        st.code(str(exc))
        st.write("Use the separate simulated Portfolio Risk Laboratory in sidebar item 02. No historical prices will be invented.")

elif page.startswith('01'):
    heading("01","Equity valuation studio","Explore how discount rates, profitability and long-term growth drive intrinsic equity value.")
    source_note("Illustrative financial assumptions · USD millions · five-year discounted cash flow")
    with st.container(border=True):
        st.markdown("**Set the assumptions**")
        a,b,d=st.columns(3)
        revenue=a.number_input("Annual revenue (USD m)",100.,100000.,1000.,step=100.)
        growth=b.slider("Revenue growth (%)",-10,30,7)/100
        wacc=d.slider("Discount rate / WACC (%)",4.0,25.0,9.5,.5)/100
        margin=a.slider("EBIT margin (%)",1,50,20)/100
        terminal_growth=b.slider("Terminal growth (%)",0.0,5.0,2.5,.5)/100
        debt=d.number_input("Net debt (USD m)",-10000.,10000.,300.,step=50.)
    if terminal_growth>=wacc:
        st.error("WACC must be greater than terminal growth.")
    else:
        assumptions=dict(revenue=revenue,growth=growth,wacc=wacc,ebit_margin=margin,terminal_growth=terminal_growth,net_debt=debt)
        result=dcf(**assumptions)
        a,b,d=st.columns(3)
        a.metric("Enterprise value",f"US$ {result['enterprise_value']:,.1f}m")
        b.metric("Equity value",f"US$ {result['equity_value']:,.1f}m")
        d.metric("Implied value/share",f"US$ {result['price_per_share']:,.2f}")
        insight("DCF value is highly sensitive to WACC, future cash flows and terminal growth. These illustrative results are not a recommendation for any traded security.")
        t1,t2,t3=st.tabs(["Forecast cash flows","Valuation sensitivity","Research notes"])
        with t1:
            frame=result["forecast"].copy()
            st.line_chart(frame.set_index("year")[["revenue","fcf"]],height=320)
            st.dataframe(frame.round(2),hide_index=True,use_container_width=True)
            downloadable_csv(frame,"equity_dcf_forecast.csv")
        with t2:
            table=sensitivity(assumptions)
            table.index=[f"{x:.1%}" for x in table.index]
            table.columns=[f"{x:.1%}" for x in table.columns]
            st.dataframe(table.style.format("{:,.2f}").background_gradient(cmap="Blues",axis=None),use_container_width=True)
            st.metric("PV of terminal value / enterprise value",f"{result['terminal_share_of_ev']:.1%}")
        with t3:
            st.write("FCFF = EBIT(1 − tax) + depreciation − capex − change in operating working capital. Enterprise value is bridged to equity value by subtracting net debt.")
            st.link_button("View source and assumptions","https://github.com/mdfinancials/Finance-Research-Lab/blob/main/projects/valuation.py")
elif page.startswith('02'):
    heading("02","Portfolio risk laboratory","Examine diversification, risk-adjusted returns and minimum-variance allocation using reproducible simulated markets.")
    source_note("Synthetic 120-month return paths · no realised investment performance")
    with st.container(border=True):
        a,b,d=st.columns(3)
        seed=a.number_input("Scenario seed",0,100000,42)
        w1=b.slider("Equity A weight (%)",0,100,50)
        w2=d.slider("Equity B weight (%)",0,100,30)
        if w1+w2>100:
            st.error("Equity A and B weights cannot exceed 100% combined.")
            st.stop()
        weights=np.array([w1,w2,100-w1-w2])/100
        st.caption(f"Remaining bond allocation: {weights[2]:.0%}")
    rng=np.random.default_rng(seed)
    returns=pd.DataFrame(rng.multivariate_normal([.008,.006,.004],[[.0025,.0009,.0004],[.0009,.0016,.0002],[.0004,.0002,.0007]],size=120),columns=["Equity A","Equity B","Bonds"])
    portfolio=rebalance_returns(returns,weights)
    report=metrics(portfolio,benchmark=returns["Equity A"])
    cols=st.columns(4)
    for col,name,value in zip(cols,["Illustrative CAGR","Annualised volatility","Sharpe ratio","Max drawdown"],[f"{report['cagr']:.1%}",f"{report['volatility']:.1%}",f"{report['sharpe']:.2f}",f"{report['max_drawdown']:.1%}"]):
        col.metric(name,value)
    insight("Diversification depends on correlation and asset exposure. Statistics here describe hypothetical simulated returns rather than historical ETF returns.")
    t1,t2,t3=st.tabs(["Portfolio growth","Optimal allocation","Risk diagnostics"])
    with t1:
        wealth=pd.DataFrame({"Simulated portfolio":(1+portfolio).cumprod(),"Simulated equity benchmark":(1+returns["Equity A"]).cumprod()})
        st.line_chart(wealth,height=340)
        downloadable_csv(wealth.reset_index(drop=True),"synthetic_portfolio_growth.csv")
    with t2:
        try:
            optimal=min_variance_weights(returns)
            allocations=pd.DataFrame({"Asset":returns.columns,"Current %":weights*100,"Minimum variance %":optimal*100})
            st.bar_chart(allocations.set_index("Asset"),height=310)
            st.dataframe(allocations.round(2),hide_index=True,use_container_width=True)
        except RuntimeError as exc:
            st.warning(f"Optimization could not converge: {exc}")
    with t3:
        st.dataframe(returns.corr().round(2).style.background_gradient(cmap="Blues",axis=None),use_container_width=True)
        st.write("Estimated beta versus the synthetic equity benchmark:",f"{report.get('beta',float('nan')):.2f}")
        st.caption("Assumes monthly rebalancing and excludes costs, tax, and liquidity constraints.")
elif page.startswith('03'):
    heading("03","Financial crime analytics","An explainable synthetic customer-review queue with score drivers and prioritisation.")
    source_note("All customer records are fictional; no actual AML decisions")
    cases=score_customers(sample_customers())
    with st.container(border=True):
        a,b=st.columns([1,2])
        threshold=a.slider("Minimum risk score",0,100,0,5)
        tiers=b.multiselect("Review tiers",["Low","Review","Priority"],default=["Low","Review","Priority"])
    filtered=cases[(cases["score"]>=threshold)&cases["tier"].astype(str).isin(tiers)].copy()
    a,b,d=st.columns(3)
    a.metric("Cases in queue",len(filtered))
    b.metric("Priority cases",int(filtered["tier"].astype(str).eq("Priority").sum()))
    d.metric("Highest score",f"{int(filtered['score'].max()) if len(filtered) else 0}/100")
    insight("The illustrative risk score supports human prioritisation. It does not indicate wrongdoing or determine regulatory compliance.")
    t1,t2,t3=st.tabs(["Review queue","Score distribution","Controls"])
    with t1:
        st.dataframe(filtered[["customer_id","score","tier","reason_codes","monthly_transactions","cash_ratio","days_since_kyc"]],hide_index=True,use_container_width=True)
        downloadable_csv(filtered,"synthetic_kyc_queue.csv")
    with t2:
        st.bar_chart(filtered.set_index("customer_id")["score"],height=320)
    with t3:
        st.write("A real system would require approved risk-policy mapping, controlled access, data validation, false-positive review, quality assurance, human approval, logging and regular monitoring.")
        st.link_button("Read case study","https://github.com/mdfinancials/Finance-Research-Lab/tree/main/case_studies/kyc_triage")
elif page.startswith('04'):
    heading("04","Fixed-income risk desk","Examine bond valuation, modified duration, convexity and rate-shock scenarios.")
    source_note("Hypothetical annual-coupon fixed-rate bond · USD 1,000 face")
    with st.container(border=True):
        a,b,d=st.columns(3)
        coupon=a.slider("Annual coupon (%)",0.0,15.0,4.5,.5)/100
        yld=b.slider("Yield to maturity (%)",0.0,20.0,5.0,.5)/100
        years=d.slider("Years to maturity",1,30,8)
    bond=bond_analytics(coupon_rate=coupon,yield_rate=yld,years=years)
    a,b,d=st.columns(3)
    a.metric("Bond price",f"US$ {bond['price']:,.2f}")
    b.metric("Modified duration",f"{bond['modified_duration']:.2f} yrs")
    d.metric("Convexity",f"{bond['convexity']:.1f}")
    insight("Bond prices generally fall as yields rise. Duration measures first-order rate exposure; convexity helps explain non-linear price responses.")
    shocks=shock_table(base_yield=yld,coupon_rate=coupon,years=years)
    t1,t2,t3=st.tabs(["Yield shocks","Cash-flow schedule","Methodology"])
    with t1:
        visible=shocks.assign(price_change_percent=shocks["price_change_pct"]*100)
        st.line_chart(visible.set_index("yield_change_bps")["price_change_percent"],height=320)
        st.dataframe(visible.round(2),hide_index=True,use_container_width=True)
        downloadable_csv(visible,"fixed_income_shocks.csv")
    with t2:
        st.bar_chart(bond["cashflows"].set_index("year"),height=310)
        st.dataframe(bond["cashflows"].round(2),hide_index=True,use_container_width=True)
    with t3:
        st.write("Discounted annual coupons plus principal using a single YTM. The exercise excludes accrued interest, key-rate duration, non-par curves, default risk and trading costs.")
        st.link_button("Read Treasury case study","https://github.com/mdfinancials/Finance-Research-Lab/tree/main/case_studies/treasury_duration")
elif page.startswith('05'):
    heading("05","M&A transaction studio","Study acquisition funding structures, synergy scenarios and pro-forma earnings accretion.")
    source_note("Entirely hypothetical acquisition · figures in USD millions")
    with st.container(border=True):
        a,b,d=st.columns(3)
        stock=a.slider("Stock financing (%)",0,100,40,5)/100
        synergy=b.number_input("Annual pre-tax synergies (USD m)",0.,1000.,30.,step=5.)
        rate=d.slider("Debt borrowing rate (%)",0.0,20.0,6.5,.5)/100
    model=deal_model(stock_pct=stock,pretax_synergies=synergy,borrow_rate=rate)
    a,b,d=st.columns(3)
    a.metric("Standalone EPS",f"US$ {model['standalone_eps']:.2f}")
    b.metric("Pro-forma EPS",f"US$ {model['proforma_eps']:.2f}")
    d.metric("EPS accretion / dilution",f"{model['accretion_pct']:+.1%}")
    insight("EPS accretion is not the same as economic value creation. Purchase accounting, transaction fees and integration risks are excluded from this simplified screen.")
    t1,t2,t3=st.tabs(["Deal economics","Scenario grid","Investment committee notes"])
    with t1:
        st.bar_chart(pd.DataFrame({"Earnings per share":[model["standalone_eps"],model["proforma_eps"]]},index=["Standalone","Pro forma"]),height=310)
        st.dataframe(pd.DataFrame([model]).round(3),hide_index=True,use_container_width=True)
    with t2:
        grid=scenarios().copy()
        grid["Stock financed (%)"]=grid["stock_pct"]*100
        grid["EPS accretion (%)"]=grid["accretion_pct"]*100
        st.dataframe(grid[["Stock financed (%)","pretax_synergies","EPS accretion (%)"]].round(2),hide_index=True,use_container_width=True)
        downloadable_csv(grid,"merger_scenarios.csv")
    with t3:
        st.write("Further diligence should address the target's operating profile, financing capacity, goodwill, amortisation, integration costs, debt covenants, tax assumptions and value creation.")
        st.link_button("Read M&A case study","https://github.com/mdfinancials/Finance-Research-Lab/tree/main/case_studies/ma_acquisition")
else:
    heading("06","Applied research library","Explore five reproducible case studies that connect analytical methods with practical financial questions.")
    source_note("Public source data where indicated; all synthetic and hypothetical information identified explicitly")
    case=st.selectbox("Research case study",["NVIDIA DCF","ETF Allocation","Synthetic KYC","Treasury Duration","Hypothetical M&A"])
    if case=="NVIDIA DCF":
        st.subheader("NVIDIA | FY2026 filings + FY2027–29 illustrative scenarios")
        st.write("These are analyst scenarios, not a live NVDA price target. Share count and growth assumptions are illustrative.")
        rows=[{"scenario":s,**{k:v for k,v in nvda_dcf(s).items() if k in ("wacc","terminal_growth","value_per_share_usd","terminal_pv_share")}} for s in ("bear","base","bull")]
        results=pd.DataFrame(rows)
        cols=st.columns(3)
        for col,name in zip(cols,("bear","base","bull")):
            value=float(results.loc[results["scenario"]==name,"value_per_share_usd"].iloc[0])
            col.metric(name.title()+" case",f"US$ {value:,.2f}")
        t1,t2=st.tabs(["Valuation scenarios","WACC sensitivity"])
        with t1:
            st.dataframe(results.round(3),hide_index=True,use_container_width=True)
        with t2:
            st.dataframe(pd.DataFrame(nvda_grid(),columns=["WACC","Terminal growth","Illustrative USD/share"]).round(3),hide_index=True,use_container_width=True)
    elif case=="ETF Allocation":
        st.subheader("VOO / VXUS / QQQ | Synthetic return and stress study")
        r=etf_case()
        st.write("Allocation: 45% VOO / 35% VXUS / 20% QQQ. No historical performance is claimed.")
        st.dataframe(pd.DataFrame([r["summary"]]).round(3),hide_index=True,use_container_width=True)
        st.metric("Hypothetical stress loss",f'{r["stress_loss"]:.1%}')
        allocation=pd.DataFrame({"ETF":["VOO","VXUS","QQQ"],"Minimum variance weight (%)":100*r["min_variance_weights"]})
        st.bar_chart(allocation.set_index("ETF"),height=300)
        st.dataframe(allocation.round(2),hide_index=True,use_container_width=True)
    elif case=="Synthetic KYC":
        st.subheader("Explainable KYC review queue | Entirely synthetic records")
        r=kyc_case()
        a,b=st.columns(2)
        a.metric("Synthetic precision",f'{r["precision"]:.0%}')
        b.metric("Synthetic recall",f'{r["recall"]:.0%}')
        st.dataframe(r["review_queue"],hide_index=True,use_container_width=True)
        st.warning("No actual customers, AML conclusions, or production model validation.")
    elif case=="Treasury Duration":
        st.subheader("10Y Treasury par yield snapshot | 10 Nov 2026")
        r=bond_case()
        st.write("Market par yield input: 4.98% on 10 Nov 2026. 4.5% coupon is hypothetical.")
        st.metric("Model bond price per $1,000 face",f'{r["base_price"]:.2f}')
        frame=pd.DataFrame(r["scenarios"])
        st.line_chart(frame.set_index("yield_shock_bps")[["exact_price_move_pct","duration_convexity_move_pct"]],height=320)
        st.dataframe(frame.round(2),hide_index=True,use_container_width=True)
    else:
        st.subheader("Aster Cloud / Beacon AI | Entirely fictional acquisition")
        r=ma_case()
        a,b=st.columns(2)
        a.metric("EPS accretion / dilution",f'{r["accretion_pct"]:+.1%}')
        b.metric("Break-even pretax synergies (USD millions)",f'{r["break_even_synergies_m"]:,.1f}')
        matrix=pd.DataFrame(ma_matrix())
        st.dataframe(matrix.round(3),hide_index=True,use_container_width=True)
        st.info("Accretion alone does not establish transaction value creation.")

footer()
