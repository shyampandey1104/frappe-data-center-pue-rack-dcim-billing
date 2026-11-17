import unittest
from datacenter_dcim_billing.engine import RackEnclosureTelemetry, DataCenterDCIMBillingEngine

class TestDataCenterDCIMBillingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DataCenterDCIMBillingEngine(pue_sla_target=1.35)

    def test_pue_and_telemetry(self):
        tele = RackEnclosureTelemetry(
            rack_id="RACK-H1-042", hall_id="HALL-01", tenant_id="CLOUD-HOST-CORP",
            allocated_kw=15.0, metered_it_kw=10.0, total_facility_kw=12.5,
            intake_temp_celsius=22.5
        )
        res = self.engine.ingest_rack_telemetry(tele)
        self.assertEqual(res["calculated_pue"], 1.25)
        self.assertTrue(res["pue_sla_compliant"])
        self.assertFalse(res["ashrae_thermal_warning"])

    def test_colocation_billing(self):
        tele = RackEnclosureTelemetry(
            rack_id="RACK-H1-043", hall_id="HALL-01", tenant_id="AI-LABS-INC",
            allocated_kw=20.0, metered_it_kw=18.0, total_facility_kw=23.4,
            intake_temp_celsius=24.0
        )
        self.engine.ingest_rack_telemetry(tele)
        bill = self.engine.generate_colocation_monthly_bill(
            rack_id="RACK-H1-043", kwh_consumed=12960.0, rate_per_kwh=9.50, base_rack_rent=45000.0
        )
        self.assertEqual(bill["power_charge"], 123120.0)
        self.assertEqual(bill["total_invoice_inr"], 168120.0)

if __name__ == "__main__":
    unittest.main()
