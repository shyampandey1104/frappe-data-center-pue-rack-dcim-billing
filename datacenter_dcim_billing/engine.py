"""Data Center Infrastructure Management (DCIM) PUE & Colocation Billing Engine."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class RackEnclosureTelemetry:
    rack_id: str
    hall_id: str
    tenant_id: str
    allocated_kw: float
    metered_it_kw: float
    total_facility_kw: float  # Cooling + UPS loss + IT
    intake_temp_celsius: float
    power_factor: float = 0.98

class DataCenterDCIMBillingEngine:
    def __init__(self, pue_sla_target: float = 1.35):
        self.pue_sla_target = pue_sla_target
        self.racks: Dict[str, RackEnclosureTelemetry] = {}

    def ingest_rack_telemetry(self, tele: RackEnclosureTelemetry) -> Dict[str, Any]:
        if tele.metered_it_kw <= 0:
            raise ValueError("Metered IT load must be strictly positive.")
        pue = round(tele.total_facility_kw / tele.metered_it_kw, 3)
        self.racks[tele.rack_id] = tele
        
        # ASHRAE thermal envelope check (18C to 27C)
        ashrae_breach = tele.intake_temp_celsius < 18.0 or tele.intake_temp_celsius > 27.0
        return {
            "rack_id": tele.rack_id,
            "calculated_pue": pue,
            "pue_sla_compliant": pue <= self.pue_sla_target,
            "ashrae_thermal_warning": ashrae_breach
        }

    def generate_colocation_monthly_bill(self, rack_id: str, kwh_consumed: float, rate_per_kwh: float, base_rack_rent: float) -> Dict[str, Any]:
        if rack_id not in self.racks:
            raise ValueError(f"Rack {rack_id} not registered.")
        rack = self.racks[rack_id]
        
        power_cost = round(kwh_consumed * rate_per_kwh, 2)
        total_bill = round(base_rack_rent + power_cost, 2)
        return {
            "rack_id": rack_id,
            "tenant_id": rack.tenant_id,
            "base_rack_rent": base_rack_rent,
            "kwh_consumed": kwh_consumed,
            "power_charge": power_cost,
            "total_invoice_inr": total_bill
        }
