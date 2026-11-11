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

st.set_page_config(page_title='Finance Research Lab',layout='wide',page_icon='📈')
st.title('Finance Research Lab')
st.caption('Five reproducible analytical prototypes | DEMONSTRATION DATA — not investment advice or live market data')
page=st.sidebar.radio('Project', ['01 · Equity valuation','02 · Portfolio analytics','03 · KYC risk triage','04 · Fixed income','05 · M&A modelling','06 · Applied case studies'])

if page.startswith('01'):
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
