"""Reconciliation tests for NVIDIA illustrative three-statement forecast."""
import unittest
from model import forecast, FY26, ASSUMPTIONS, Drivers
class ModelTests(unittest.TestCase):
    def test_historical_anchor_balances(self):
        assets=sum(FY26[k] for k in ('cash','securities','ar','inventory','prepaid','ppe','other_assets'))
        liabilities=sum(FY26[k] for k in ('ap','accrued','debt','other_liabilities'))
        self.assertEqual(assets,liabilities+FY26['equity'])
    def test_three_fiscal_years(self):
        rows=forecast()
        self.assertEqual([x['year'] for x in rows],[2027,2028,2029])
        for x in rows:
            self.assertAlmostEqual(x['bs_check'],0,places=5)
            self.assertAlmostEqual(x['cashflow_check'],0,places=5)
            self.assertGreater(x['cash'],0)
    def test_sensitivity(self):
        base=forecast()[0]['revenue']
        altered=dict(ASSUMPTIONS)
        d=altered[2027]
        altered[2027]=Drivers(**{**d.__dict__,'growth':d.growth+0.05})
        self.assertGreater(forecast(drivers=altered)[0]['revenue'],base)
if __name__=='__main__': unittest.main()
