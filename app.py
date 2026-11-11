"""Interactive finance portfolio. Run: streamlit run app.py"""
import numpy as np
import pandas as pd
import streamlit as st
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

st.set_page_config(page_title='Finance Research Lab',layout='wide',page_icon='📈')
st.markdown("""
<style>
.block-container {max-width: 1120px; padding-top: 2.0rem; padding-bottom: 4rem;}
[data-testid="stSidebar"] {background: #111b2b;}
[data-testid="stSidebar"] * {color: #e4edf8;}
.hero {padding: 2.15rem 2rem; border-radius: 18px; background: linear-gradient(115deg,#132b48,#17253e 60%,#245a69); color: white;}
.hero .eyebrow {font-size: .78rem; letter-spacing: .15em; color: #a6ebd6; text-transform: uppercase; font-weight: 700;}
.hero h1 {font-size: clamp(2rem, 4vw, 3.4rem); line-height: 1.14; color:white; margin: .55rem 0;}
.hero p {color:#d2e0ed; max-width: 680px; font-size:1.07rem;}
.eyebrow-label {letter-spacing:.1em; text-transform:uppercase; font-size:.77rem; font-weight:700; color:#2c8590;}
</style>
""",unsafe_allow_html=True)
page=st.sidebar.radio('Navigate', ['Home · Portfolio', '01 · Equity valuation','02 · Portfolio analytics','03 · KYC risk triage','04 · Fixed income','05 · M&A modelling','06 · Applied case studies','07 · NVIDIA Yahoo Finance Research'])
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
    st.title("NVIDIA · Yahoo Finance Research")
    st.caption("Annual financials and adjusted/closing price history retrieved from Yahoo Finance via yfinance. Analyst forecasts are hypothetical.")
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
        st.metric("Most recent Yahoo Finance closing price (USD)",f"${snapshot['price']:,.2f}")
        st.subheader("Historical annual statements (USD millions)")
        annual_display=snapshot["annual"].copy()
        annual_display["fiscal_year"]="FY"+annual_display["fiscal_year_end"].str.slice(0,4)
        annual_display=annual_display.rename(columns={"fiscal_year_end":"Yahoo period-end label"})
        st.caption("Yahoo often labels annual periods January 31. NVIDIA's actual fiscal year-end date may differ; refer to SEC filings. FY designation is based on the year of Yahoo's period label.")
        st.dataframe(annual_display,use_container_width=True)
        st.line_chart(snapshot["prices"]["Close"])
        st.subheader("Illustrative five-year discounted cash-flow scenarios")
        st.write("The share-count input starts with Yahoo Finance's latest annual diluted weighted-average shares, not a verified current outstanding share count.")
        latest_annual=snapshot["annual"].sort_values("fiscal_year_end").iloc[-1]
        yahoo_shares=latest_annual.get("shares",float("nan"))
        if pd.isna(yahoo_shares) or float(yahoo_shares)<=0:
            st.warning("Yahoo did not provide diluted weighted-average shares. Enter a share count verified from NVIDIA filings before calculating valuation.")
            shares=st.number_input("Verified diluted shares (millions)",min_value=1.0,max_value=100000.0,value=1.0,step=1.0)
            st.stop()
        shares=st.number_input("Diluted shares (millions; verify against filings)",min_value=1.0,max_value=100000.0,value=float(yahoo_shares),step=10.0)
        st.caption(f"Yahoo Finance annual diluted average shares: {float(yahoo_shares):,.0f} million. Forecast price/share is sensitive to this input.")
        scenarios_df=scenario_table(snapshot,shares_m=shares)
        scenario_display=scenarios_df.copy()
        for col in ("wacc","terminal_growth"):
            scenario_display[col]=scenario_display[col].map(lambda x:f"{x:.1%}")
        scenario_display=scenario_display.rename(columns={"scenario":"Scenario","wacc":"WACC","terminal_growth":"Terminal growth","value_per_share_usd":"Value/share (USD)","upside_to_yahoo_close_pct":"Upside vs dated close (%)","terminal_value_pct":"Terminal value share (%)"})
        st.dataframe(scenario_display.round(2),hide_index=True,use_container_width=True)
        st.subheader("Base-case WACC × terminal growth sensitivity")
        st.dataframe(sensitivity_table(snapshot,shares_m=shares).round(2),use_container_width=True)
        st.warning("Scenarios are analyst assumptions, not current price targets or recommendations. Yahoo's filing periods, missing investment lines, dilution and accounting classifications require validation.")
    except (YahooDataError,ValueError,KeyError,TypeError,IndexError) as exc:
        st.error("Yahoo Finance data cannot be used to calculate the report right now.")
        st.code(str(exc))
        st.write("Use the static NVIDIA case study while Yahoo Finance is unavailable. No replacement financial numbers have been invented.")

elif page.startswith('01'):
    st.header('DCF valuation and sensitivity analysis')
    a,b,c=st.columns(3)
    rev=a.number_input('Starting revenue (million)',100.,100000.,1000.)
    growth=b.slider('Revenue growth',-.10,.30,.07,.01)
    wacc=c.slider('WACC',.04,.25,.095,.005)
    margin=a.slider('EBIT margin',.01,.5,.20,.01)
    tg=b.slider('Terminal growth',0.,.05,.025,.005)
    netdebt=c.number_input('Net debt (million)',-10000.,10000.,300.)
    if tg>=wacc: st.error('WACC must exceed terminal growth')
    else:
        params=dict(revenue=rev,growth=growth,wacc=wacc,ebit_margin=margin,terminal_growth=tg,net_debt=netdebt)
        result=dcf(**params)
        col1,col2,col3=st.columns(3)
        col1.metric('Enterprise value (m)',f"{result['enterprise_value']:,.1f}")
        col2.metric('Equity value (m)',f"{result['equity_value']:,.1f}")
        col3.metric('Value per share',f"${result['price_per_share']:,.2f}")
        st.dataframe(result['forecast'].round(2),use_container_width=True)
        st.subheader('Sensitivity: price per share, WACC × terminal growth')
        st.dataframe(sensitivity(params).round(2),use_container_width=True)
        st.caption('Assumptions are synthetic. Terminal value may dominate the result; validate against peers and disclosures.')

elif page.startswith('02'):
    st.header('Portfolio analysis and minimum-variance allocation')
    seed=st.number_input('Synthetic return scenario seed',0,100000,42)
    rng=np.random.default_rng(seed)
    data=pd.DataFrame(rng.multivariate_normal([.008,.006,.004],[[.0025,.0009,.0004],[.0009,.0016,.0002],[.0004,.0002,.0007]],size=120),columns=['Equity A','Equity B','Bonds'])
    w=np.array([.5,.3,.2]); r=rebalance_returns(data,w)
    st.line_chart(pd.DataFrame({'Illustrative portfolio':(1+r).cumprod(),'Equity A':(1+data['Equity A']).cumprod()}))
    m=metrics(r,benchmark=data['Equity A'])
    st.dataframe(pd.DataFrame([m]).T.rename(columns={0:'Value'}))
    optim=min_variance_weights(data)
    st.write('Constrained minimum-variance allocation (historical synthetic covariance)')
    st.dataframe(pd.DataFrame({'asset':data.columns,'current_weight':w,'min_variance_weight':optim}))
    st.caption('Synthetic monthly returns, monthly rebalancing, no trading costs. No historical investment performance is claimed.')

elif page.startswith('03'):
    st.header('Explainable customer risk review triage')
    st.warning('Entirely synthetic records. Scores are illustrative prioritisation rules, NOT validated AML risk ratings or proof of suspicious activity.')
    df=score_customers(sample_customers())
    st.metric('Priority review cases',int((df.tier=='Priority').sum()))
    st.bar_chart(df.set_index('customer_id').score)
    st.dataframe(df,use_container_width=True)
    st.markdown('**Controls:** human approval, access restrictions, false-positive review, documented policy mapping and periodic validation would be required before any real-world use.')

elif page.startswith('04'):
    st.header('Bond duration, convexity and interest-rate shocks')
    a,b,c=st.columns(3)
    coupon=a.slider('Annual coupon',0.,.15,.045,.005)
    yld=b.slider('Yield',0.,.20,.05,.005)
    years=c.slider('Years to maturity',1,30,8)
    x=bond_analytics(coupon_rate=coupon,yield_rate=yld,years=years)
    a,b,c=st.columns(3)
    a.metric('Bond price',f"${x['price']:,.2f}")
    b.metric('Modified duration',f"{x['modified_duration']:.2f}")
    c.metric('Convexity',f"{x['convexity']:.2f}")
    st.dataframe(shock_table(base_yield=yld,coupon_rate=coupon,years=years),use_container_width=True)
    st.caption('Annual-coupon bond, parallel yield shocks, no spread or default modelling.')

elif page.startswith('05'):
    st.header('Acquisition EPS accretion / dilution')
    a,b,c=st.columns(3)
    stock=a.slider('Stock-funded fraction',0.,1.,.4,.05)
    syn=b.number_input('Annual pretax synergies (million)',0.,1000.,30.)
    rate=c.slider('New debt rate',0.,.2,.065,.005)
    x=deal_model(stock_pct=stock,pretax_synergies=syn,borrow_rate=rate)
    a,b,c=st.columns(3)
    a.metric('Standalone EPS',f"${x['standalone_eps']:.2f}")
    b.metric('Pro forma EPS',f"${x['proforma_eps']:.2f}")
    c.metric('Accretion / (dilution)',f"{x['accretion_pct']:+.1%}")
    st.dataframe(scenarios().round(3),use_container_width=True)
    st.caption('Simplified EPS screen only; excludes fees, integration costs, purchase accounting, amortisation and timing.')

else:
    st.header("Applied finance case studies")
    st.caption("Five sourced or synthetic, reproducible analyst cases. These are not live investment recommendations.")
    case=st.selectbox("Select case study",["NVIDIA DCF","ETF Allocation","Synthetic KYC","Treasury Duration","Hypothetical M&A"])
    if case=="NVIDIA DCF":
        st.subheader("NVIDIA | FY2026 filings + FY2027–29 illustrative scenarios")
        st.write("These are analyst scenarios, not a live NVDA price target. Share count and growth assumptions are illustrative.")
        rows=[{"scenario":s,**{k:v for k,v in nvda_dcf(s).items() if k in ("wacc","terminal_growth","value_per_share_usd","terminal_pv_share")}} for s in ("bear","base","bull")]
        st.dataframe(pd.DataFrame(rows),use_container_width=True)
        st.dataframe(pd.DataFrame(nvda_grid(),columns=["WACC","Terminal growth","Illustrative USD/share"]),use_container_width=True)
    elif case=="ETF Allocation":
        st.subheader("VOO / VXUS / QQQ | Synthetic return and stress study")
        r=etf_case()
        st.write("Allocation: 45% VOO / 35% VXUS / 20% QQQ. No historical performance is claimed.")
        st.dataframe(pd.DataFrame([r["summary"]]),use_container_width=True)
        st.metric("Hypothetical stress loss",f'{r["stress_loss"]:.1%}')
        st.dataframe(pd.DataFrame({"ETF":["VOO","VXUS","QQQ"],"minimum_variance_weight":r["min_variance_weights"]}),use_container_width=True)
    elif case=="Synthetic KYC":
        st.subheader("Explainable KYC review queue | Entirely synthetic records")
        r=kyc_case()
        a,b=st.columns(2)
        a.metric("Synthetic precision",f'{r["precision"]:.0%}')
        b.metric("Synthetic recall",f'{r["recall"]:.0%}')
        st.dataframe(r["review_queue"],use_container_width=True)
        st.warning("No actual customers, AML conclusions, or production model validation.")
    elif case=="Treasury Duration":
        st.subheader("10Y Treasury par yield snapshot | 10 Nov 2026")
        r=bond_case()
        st.write("Market par yield input: 4.98% on 10 Nov 2026. 4.5% coupon is hypothetical.")
        st.metric("Model bond price per $1,000 face",f'{r["base_price"]:.2f}')
        st.dataframe(pd.DataFrame(r["scenarios"]),use_container_width=True)
    else:
        st.subheader("Aster Cloud / Beacon AI | Entirely fictional acquisition")
        r=ma_case()
        a,b=st.columns(2)
        a.metric("EPS accretion / dilution",f'{r["accretion_pct"]:+.1%}')
        b.metric("Break-even pretax synergies (USD millions)",f'{r["break_even_synergies_m"]:,.1f}')
        st.dataframe(pd.DataFrame(ma_matrix()),use_container_width=True)
        st.info("Accretion alone does not establish transaction value creation.")
