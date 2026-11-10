"""Interactive finance portfolio. Run: streamlit run app.py"""
import numpy as np
import pandas as pd
import streamlit as st
from projects.valuation import dcf,sensitivity
from projects.portfolio import metrics,rebalance_returns,min_variance_weights
from projects.kyc import score_customers,sample_customers
from projects.fixed_income import bond_analytics,shock_table
from projects.mergers import deal_model,scenarios

st.set_page_config(page_title='Finance Research Lab',layout='wide',page_icon='📈')
st.title('Finance Research Lab')
st.caption('Five reproducible analytical prototypes | DEMONSTRATION DATA — not investment advice or live market data')
page=st.sidebar.radio('Project', ['01 · Equity valuation','02 · Portfolio analytics','03 · KYC risk triage','04 · Fixed income','05 · M&A modelling'])

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

else:
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
