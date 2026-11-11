"""Shared visual design system for Finance Research Lab.

No external images, injected JavaScript, or user-derived HTML.
"""
import html
import streamlit as st

GITHUB = "https://github.com/mdfinancials/Finance-Research-Lab"
COLORS = {"ink":"#14233c", "muted":"#60718a", "teal":"#087f78",
          "navy":"#122840", "blue":"#3f6dcb", "border":"#dae4ef"}

CSS = """
<style>
:root { color-scheme: light; }
.block-container { max-width: 1260px; padding-top: 1.5rem; padding-bottom: 5rem; }
[data-testid="stAppViewContainer"] { background: #f8fafc; }
[data-testid="stHeader"] { background: #f8fafc; }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#111f35,#172a43); }
[data-testid="stSidebar"] * { color: #e7eff9 !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {border-radius: 9px; padding: .12rem .25rem;}
h1,h2,h3 {letter-spacing: -.025em; color:#14233c !important; line-height:1.18 !important; overflow-wrap:break-word;}
h1 {font-weight: 760 !important; font-size:clamp(2.15rem,3.1vw,2.9rem) !important;}
h3 {font-weight: 670 !important;}
[data-testid="stMetric"] {
    background:#fff; border:1px solid #dce6f1; border-radius:14px;
    padding: .85rem 1rem; box-shadow:0 6px 22px rgba(26,52,82,.035);
}
[data-testid="stMetricLabel"] {color:#66788e;}
[data-testid="stMetricValue"] {color:#142943; font-weight:700;}
[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-radius: 15px !important;
}
[data-testid="stExpander"] {border-radius:12px !important;}
[data-testid="stDataFrame"] {border: 1px solid #e0e8f1; border-radius:12px; overflow:hidden;}
[data-testid="stButton"] button[kind="primary"] {
    background:#087f78; border:none; border-radius:10px;
}
div[data-testid="stCaptionContainer"], div[data-testid="stCaptionContainer"] * {color:#586d84 !important;}
.hero {
    padding: 2.2rem 2rem; background:linear-gradient(112deg,#132b46,#173d55 68%,#12645e);
    border:1px solid #31536c; border-radius:20px; color:#fff;
    box-shadow:0 14px 35px rgba(19,43,70,.14);
}
.hero h1 {font-size:clamp(2.1rem,4vw,3.25rem) !important;line-height:1.12; color:#fff !important;margin:.65rem 0;}
.hero p {color:#dceaf2;max-width:800px;font-size:1.03rem;line-height:1.65;}
.hero .eyebrow {font-size:.74rem;font-weight:700;letter-spacing:.16em;color:#a4e2d2 !important;}
.eyebrow {font-size:.76rem;font-weight:750;letter-spacing:.14em;color:#087f78 !important;margin-bottom:.2rem;line-height:1.5;}
.page-subtitle {color:#536981;font-size:1.02rem;line-height:1.55;max-width:800px;margin:.3rem 0 .75rem;}
.insight {background:#eef6f6;padding:1rem 1.2rem;border-left:3px solid #087f78;
    border-radius:0 12px 12px 0;color:#25445a;line-height:1.65;margin:.7rem 0 1.15rem;}
.small-tag {display:inline-block;background:#e5f3f1;color:#126d67;border-radius:100px;
    font-weight:700;font-size:.72rem;padding:.26rem .65rem;margin:.2rem .3rem .2rem 0;}
.footer-note {color:#66798b;font-size:.84rem;border-top:1px solid #dce5ef;margin-top:2.5rem;padding-top:1.15rem;}
@media(max-width: 700px) {
 /* Prevent section labels from appearing behind Streamlit's mobile action toolbar. */
 .block-container {padding:2.75rem .85rem 3.5rem !important;}
 .block-container h1 {font-size:2.12rem !important;line-height:1.15 !important;margin:.3rem 0 .55rem !important;}
 .block-container h2 {font-size:1.48rem !important;line-height:1.25 !important;}
 .block-container h3 {font-size:1.32rem !important;line-height:1.28 !important;}
 .eyebrow {font-size:.70rem;letter-spacing:.095em;margin-bottom:.22rem;color:#087f78 !important;}
 .page-subtitle {font-size:.96rem;line-height:1.48;margin:.15rem 0 .65rem;}
 .hero {padding:1.4rem 1.15rem; border-radius:14px;}
 .hero h1 {font-size:2.0rem !important;}
 .hero p {font-size:.94rem;line-height:1.5;}
 [data-testid="stMetric"] {padding:.68rem .85rem;border-radius:12px;}
 [data-testid="stMetricValue"] {font-size:1.18rem !important;}
 [data-testid="stMetricLabel"] {font-size:.83rem;}
 .insight {padding:.8rem 1rem;line-height:1.5;}
 .footer-note {font-size:.78rem;line-height:1.5;}
}
</style>
"""

def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)

def heading(index, title, subtitle, tag="INTERACTIVE RESEARCH"):
    st.markdown('<div class="eyebrow">'+html.escape(tag+" / "+index)+'</div>',unsafe_allow_html=True)
    st.title(title)
    st.markdown('<div class="page-subtitle">'+html.escape(subtitle)+'</div>',unsafe_allow_html=True)

def insight(text):
    st.markdown('<div class="insight">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def source_note(text):
    st.caption("DATA & METHODOLOGY  ·  "+text)

def footer():
    st.markdown(
      '<div class="footer-note">Finance Research Lab · Independent educational analysis. '
      'Illustrative outputs are not financial advice, actual investment performance, '
      'regulatory determinations or verified transaction recommendations.</div>',
      unsafe_allow_html=True)

def downloadable_csv(df, filename, title="Download results (CSV)"):
    st.download_button(title, data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,mime="text/csv",key="dl_"+filename)
