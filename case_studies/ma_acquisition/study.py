"""Aster Cloud acquiring Beacon AI: fictional EPS accretion/dilution project."""
from projects.mergers import deal_model
BASE={"acquirer_net_income":600,"acquirer_shares":200,"acquirer_share_price":45,
      "target_net_income":110,"target_equity_purchase_price":1500,
      "stock_pct":.40,"borrow_rate":.065,"tax_rate":.25,"pretax_synergies":30}
def analyse(stock_pct=.4,pretax_synergies=30,borrow_rate=.065):
    p={**BASE,"stock_pct":stock_pct,"pretax_synergies":pretax_synergies,"borrow_rate":borrow_rate}
    r=deal_model(**p)
    shares=p["acquirer_shares"]+r["new_shares"]
    income_before_synergies=p["acquirer_net_income"]+p["target_net_income"]-r["after_tax_interest"]
    required_synergies=(r["standalone_eps"]*shares-income_before_synergies)/(1-p["tax_rate"])
    return {**r,"break_even_synergies_m":required_synergies}
def matrix():
    return [{"stock_fraction":s,"synergies_m":v,"accretion":analyse(s,v)["accretion_pct"]}
            for s in (0,.25,.5,.75,1) for v in (0,20,40,60,80)]
if __name__=="__main__":
    print("FICTIONAL COMPANIES AND DEAL; EDUCATIONAL ONLY",analyse())
