"""Professional, dated NVIDIA equity-research initiation exercise as a PDF.

All live market/financial figures come from the supplied Yahoo Finance snapshot.
Quarterly NVIDIA facts are fixed to the verified 26 August 2026 release; they
are explicitly dated and may become stale. No BUY/SELL rating is given.
"""
from __future__ import annotations

from io import BytesIO
from datetime import datetime, timezone
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak,
    KeepTogether, HRFlowable,
)
from reportlab.lib.colors import HexColor
from case_studies.nvidia_three_statement.yahoo_research import (
    scenario_table, dcf_from_yahoo, ForecastDrivers, sensitivity_table
)

NAVY=HexColor("#152842")
DEEP=HexColor("#0f2138")
TEAL=HexColor("#087f78")
SLATE=HexColor("#596c7e")
LIGHT=HexColor("#edf4f6")
BORDER=HexColor("#d8e3ec")
PALE=HexColor("#f5f8fb")
WHITE=colors.white

RELEASE_URL="https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/"
FILING_URL="https://investor.nvidia.com/financial-info/financial-reports/"
YAHOO_URL="https://finance.yahoo.com/quote/NVDA/"

def _style_sheet():
    s=getSampleStyleSheet()
    return {
        "title":ParagraphStyle("ResearchTitle",parent=s["Title"],fontName="Helvetica-Bold",
             fontSize=23,leading=27,textColor=DEEP,spaceAfter=9,alignment=TA_LEFT),
        "sub":ParagraphStyle("ReportSubtitle",parent=s["Normal"],fontName="Helvetica",
             fontSize=11,leading=16,textColor=SLATE,spaceAfter=10),
        "h":ParagraphStyle("SectionHeading",parent=s["Heading2"],fontName="Helvetica-Bold",
             fontSize=13.0,leading=17,textColor=NAVY,spaceBefore=15,spaceAfter=9),
        "small_h":ParagraphStyle("Subheading",parent=s["Heading3"],fontName="Helvetica-Bold",
             fontSize=10.5,leading=14,textColor=TEAL,spaceBefore=10,spaceAfter=5),
        "body":ParagraphStyle("BodyTextCustom",parent=s["BodyText"],fontName="Helvetica",
             fontSize=9.2,leading=14.1,textColor=DEEP,spaceAfter=8),
        "bullet":ParagraphStyle("BulletTextCustom",parent=s["BodyText"],fontName="Helvetica",
             fontSize=9.0,leading=13.4,textColor=DEEP,leftIndent=12,firstLineIndent=-9,spaceAfter=6),
        "tablehead":ParagraphStyle("TableHead",parent=s["Normal"],fontName="Helvetica-Bold",
             fontSize=8.0,leading=11,textColor=WHITE),
        "cell":ParagraphStyle("TableCell",parent=s["Normal"],fontName="Helvetica",
             fontSize=8.0,leading=11.1,textColor=DEEP),
        "caption":ParagraphStyle("CaptionCustom",parent=s["Normal"],fontName="Helvetica",
             fontSize=7.6,leading=11.1,textColor=SLATE,spaceAfter=6),
        "tag":ParagraphStyle("TagCustom",parent=s["Normal"],fontName="Helvetica-Bold",
             fontSize=8.1,leading=11,spaceAfter=9,textColor=TEAL),
        "footer":ParagraphStyle("FooterCustom",parent=s["Normal"],fontName="Helvetica",
             fontSize=7.5,leading=10.5,textColor=SLATE,alignment=TA_CENTER),
    }

def _p(text, style):
    return Paragraph(text,style)

def _table(headers, rows, styles, widths=None):
    data=[[_p(str(x),styles["tablehead"]) for x in headers]]
    for row in rows:
        data.append([_p(escape(str(x)),styles["cell"]) for x in row])
    tbl=Table(data,colWidths=widths,repeatRows=1,hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,PALE]),
        ("GRID",(0,0),(-1,-1),.35,BORDER),
        ("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
        ("VALIGN",(0,0),(-1,-1),"TOP")
    ]))
    return tbl

def _page(canvas,doc):
    canvas.saveState()
    w,h=doc.pagesize
    canvas.setFillColor(NAVY)
    canvas.rect(0,h-8,w,8,stroke=0,fill=1)
    canvas.setFont("Helvetica-Bold",8.2)
    canvas.setFillColor(TEAL)
    canvas.drawString(42,h-31,"FINANCE RESEARCH LAB  /  EQUITY RESEARCH")
    canvas.setStrokeColor(BORDER)
    canvas.line(42,45,w-42,45)
    canvas.setFont("Helvetica",7.2)
    canvas.setFillColor(SLATE)
    canvas.drawString(42,31,"Independent educational research | Not investment advice")
    canvas.drawRightString(w-42,31,"NVIDIA / NVDA   -   Page "+str(doc.page))
    canvas.restoreState()

def _bullet(text,s):
    return _p("&#8226;  "+text,s["bullet"])

def build_nvidia_research_pdf(snapshot,shares_m=None):
    """Return report bytes. Raise on missing Yahoo accounting values."""
    latest=snapshot["annual"].dropna(subset=["revenue"]).sort_values("fiscal_year_end").iloc[-1]
    if shares_m is None:
        shares_m=float(latest["shares"])
    valuation=dcf_from_yahoo(snapshot,ForecastDrivers(),shares_m)
    scenarios=scenario_table(snapshot,shares_m)
    curve=sensitivity_table(snapshot,shares_m)
    now=datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")
    close_date=escape(str(snapshot["price_date"]))
    annual_date=escape(str(latest["fiscal_year_end"]))
    s=_style_sheet()
    buf=BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=(595,842),rightMargin=43,leftMargin=43,
                          topMargin=58,bottomMargin=58,title="NVIDIA | Equity Research Initiation - Finance Research Lab",
                          author="MD Mahdi Mahbub Rauf | Finance Research Lab")
    story=[]
    story += [_p("INDEPENDENT EQUITY RESEARCH  /  NVDA",s["tag"]),
              _p("NVIDIA Corporation",s["title"]),
              _p("Initiation-style research note | AI compute infrastructure, financial drivers and valuation",s["sub"]),
              HRFlowable(width="100%",thickness=1.5,color=TEAL,spaceBefore=3,spaceAfter=13)]
    details=[
        ("Research classification","NOT RATED - educational research"),
        ("Last Yahoo close",f"US$ {snapshot['price']:,.2f} ({close_date})"),
        ("Illustrative base DCF",f"US$ {valuation['value_per_share']:,.2f} / share"),
        ("Model upside/(downside)",f"{valuation['implied_upside_pct']:+,.1f}% vs dated close"),
        ("Research generated",now),
        ("Research facts reviewed","12 Nov 2026; fixed FY2027 Q2 earnings release"),
    ]
    story.append(_table(["Reference item","Observation"],details,s,[170,338]))
    story += [_p("Executive research thesis",s["h"]),
              _p("NVIDIA is a leading supplier of accelerated computing hardware and associated infrastructure for AI workloads. "
                 "Its fiscal 2027 second-quarter disclosure illustrates substantial demand and operating scale, but high market expectations "
                 "make the investment case sensitive to capacity buildout, margin durability, policy constraints and the cost of capital.",s["body"]),
              _bullet("<b>Structural growth:</b> AI infrastructure adoption and data-centre investment can support demand, "
                      "subject to the economics and timing of customer deployments.",s),
              _bullet("<b>Competitive differentiation:</b> integrated hardware, networking and software can support customer adoption, "
                      "but peers and internally developed accelerators may affect pricing and share.",s),
              _bullet("<b>Valuation discipline:</b> intrinsic value varies substantially with growth, discount-rate and terminal assumptions; "
                      "the model does not produce a validated price target.",s),
              _p("Investment view",s["small_h"]),
              _p("<b>Not rated.</b> The research outcome is a range of illustrative values, not a recommendation to buy, sell or hold. "
                 "No independent channel checks, expert interviews or peer-multiple validation were completed.",s["body"]),
              _p("Evidence timeline",s["h"]),
              _p("Company facts below are drawn from NVIDIA's <b>26 August 2026</b> fiscal 2027 second-quarter release. "
                 "They have not been refreshed for results published after the research-review date. "
                 "The market close and annual financial data are retrieved separately from Yahoo Finance when the PDF is generated.",s["body"]),
              _table(["FY2027 Q2 disclosure","Company-reported observation"],[
                  ("Quarterly revenue","US$96.221bn, +106% year over year"),
                  ("Data Centre revenue","US$89.0bn, +117% year over year"),
                  ("GAAP gross margin","75.0%"),
                  ("Q3 revenue outlook at release","US$108.0bn +/- 2% (company guidance, not actual)"),
              ],s,[180,328]),
              PageBreak()]
    story += [_p("Business model and industry context",s["h"]),
              _p("NVIDIA supplies computing platforms spanning GPU accelerators, interconnect and networking, and supporting software. "
                 "Data-centre demand is linked to AI training and inference infrastructure as well as customers' expected economics of deployment. "
                 "The wider value chain includes semiconductor foundries, advanced packaging, memory, networking and energy-intensive data centres.",s["body"]),
              _p("What could sustain demand",s["small_h"]),
              _bullet("Training, inference and enterprise AI workloads may require incremental compute, networking and specialised systems.",s),
              _bullet("Software and development ecosystems can increase switching costs, while hardware generation changes create upgrade cycles.",s),
              _bullet("Model and workload efficiency improvements may expand use cases, although they can also reduce compute intensity per task.",s),
              _p("What could constrain demand",s["small_h"]),
              _bullet("Customer capital-spending cycles, financing availability and energy or datacentre capacity constraints.",s),
              _bullet("Export restrictions, trade rules, country concentration and related product-market access.",s),
              _bullet("Alternative accelerators, competitor pricing and large customers' internal semiconductor programmes.",s),
              _p("Financial trajectory: reported vs modelled",s["h"]),
              _p(f"The latest annual revenue observation provided by Yahoo Finance is <b>US$ {float(latest['revenue']):,.0f}m</b> "
                 f"under its annual period label <b>{annual_date}</b>. Period labelling and accounting line definitions require "
                 "cross-checking with SEC filings. No interim figures have been silently substituted into the annual DCF base.",s["body"])]
    years=valuation["forecast"]
    story.append(_table(["Projection","Revenue (US$m)","EBIT (US$m)","FCFF (US$m)"],
          [(f"Year {int(x.year)}",f"{x.revenue:,.0f}",f"{x.ebit:,.0f}",f"{x.fcff:,.0f}") for x in years.itertuples()],
          s,[84,145,139,140]))
    story += [_p("Forecast assumptions",s["small_h"]),
              _p("Five-year base-case revenue growth: 35%, 25%, 20%, 15%, 12%; "
                 "operating margins: 57%, 55%, 53%, 51%, 50%. Further illustrative assumptions: tax 17%, "
                 "D&amp;A 1.5% of sales, capex 3.5% of sales and incremental operating NWC 8% of the revenue change. "
                 "These are scenario drivers chosen for demonstration, <b>not company guidance or independently validated forecasts</b>.",s["body"]),
              PageBreak()]
    story += [_p("Valuation framework",s["h"]),
              _p("Free cash flow to the firm (FCFF) is estimated as EBIT x (1 - tax) + D&amp;A - capital expenditure "
                 "- change in operating working capital. FCFF is discounted at the model WACC. "
                 "Terminal value uses a Gordon-growth perpetuity, then enterprise value is bridged to equity with "
                 "the selected Yahoo balance-sheet fields and divided by diluted annual weighted-average shares.",s["body"]),
              _p("Illustrative scenario valuation",s["small_h"]),
              _table(["Scenario","WACC","Terminal growth","Value / share","vs dated close"],
                     [(r["scenario"],f"{r['wacc']:.1%}",f"{r['terminal_growth']:.1%}",
                       f"US$ {r['value_per_share_usd']:,.2f}",f"{r['upside_to_yahoo_close_pct']:+.1f}%")
                       for _,r in scenarios.iterrows()],s,[100,85,110,110,103]),
              _p("Base-case valuation drivers",s["small_h"]),
              _table(["Measure","Illustrative result"],[
                  ("Enterprise value",f"US$ {valuation['enterprise_value_m']:,.0f}m"),
                  ("Equity value",f"US$ {valuation['equity_value_m']:,.0f}m"),
                  ("Cash + investments - debt",f"US$ {valuation['net_cash_m']:,.0f}m"),
                  ("Diluted weighted average shares",f"{valuation['shares_m']:,.0f}m"),
                  ("Terminal PV / enterprise value",f"{valuation['terminal_pv_pct']:.1f}%"),
              ],s,[244,264]),
              _p("WACC x terminal growth: USD per diluted share",s["small_h"])]
    values=[(f"{idx:.1%}",)+tuple(f"{curve.loc[idx,col]:,.0f}" for col in curve.columns)
            for idx in curve.index]
    story.append(_table(["WACC / g"]+[f"{g:.1%}" for g in curve.columns],values,s,
                        [83]+[85]*len(curve.columns)))
    story += [_p("Interpretation",s["small_h"]),
              _p("The valuation range is dominated by uncertain long-horizon cash flows and terminal assumptions. "
                 "It should not be treated as a market consensus estimate or an actionable price target. "
                 "The Yahoo annual weighted-average share count may differ from current diluted shares outstanding.",s["body"]),
              PageBreak()]
    story += [_p("Catalysts, risks and diligence",s["h"]),
              _p("Potential catalysts (hypotheses, not guarantees)",s["small_h"]),
              _bullet("New product adoption, volume ramp or operating disclosures that support margin durability.",s),
              _bullet("Evidence of AI inference monetisation and sustained customer infrastructure returns.",s),
              _bullet("Improved supply availability and diversification across customers and geographies.",s),
              _p("Material risks and bear-case considerations",s["small_h"]),
              _bullet("<b>Export controls and regulation:</b> changing market access could constrain addressable demand.",s),
              _bullet("<b>Capital spending:</b> slower hyperscaler or enterprise infrastructure rollouts may change the growth trajectory.",s),
              _bullet("<b>Execution and supply chain:</b> advanced manufacturing, packaging, networking and power dependencies may limit shipments.",s),
              _bullet("<b>Competition and pricing:</b> alternative silicon and customer-designed chips may reduce economics.",s),
              _bullet("<b>Model risk:</b> an annual run-rate forecast omits newly released interim information and can exaggerate precision.",s),
              _p("Research questions before issuing a genuine recommendation",s["small_h"]),
              _bullet("Reconcile annual Yahoo line items to audited 10-K and latest 10-Q; separate cash and investment classifications to avoid double counting.",s),
              _bullet("Build an explicit demand-by-platform forecast with orders, capacity, customer concentration and unit economics.",s),
              _bullet("Benchmark operating margin and valuation against a defensible peer set and market-implied assumptions.",s),
              _bullet("Refresh events after 12 November 2026 and document material new quarterly disclosures.",s),
              _p("Sources and disclosures",s["h"]),
              _p(f'<link href="{RELEASE_URL}" color="#087f78">NVIDIA Q2 fiscal 2027 earnings release (26 Aug 2026)</link> '
                 "- source for the reported quarterly metrics and then-current guidance.",s["body"]),
              _p(f'<link href="{FILING_URL}" color="#087f78">NVIDIA investor financial reports and SEC filings</link> '
                 "- primary source to validate reported statements.",s["body"]),
              _p(f'<link href="{YAHOO_URL}" color="#087f78">Yahoo Finance NVDA historical quotes and statements</link> '
                 "- third-party market/annual data retrieved at report generation.",s["body"]),
              _p(f"Yahoo reference price date: {close_date}. PDF generation: {now}. "
                 "Amounts in USD unless stated. Material figures can be delayed, reclassified or missing. "
                 + escape(valuation.get("investments_note","")),s["caption"]),
              _p("Prepared by MD Mahdi Mahbub Rauf | Independent Finance Research Lab. "
                 "Built with AI-assisted software development and researcher-directed financial assumptions. "
                 "This report is an educational research exercise, not regulated investment research, "
                 "personal financial advice or a solicitation to trade.",s["caption"])]
    doc.build(story,onFirstPage=_page,onLaterPages=_page)
    return buf.getvalue()
