# Frappe Data Center DCIM, PUE & Colocation Power Billing Engine

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.x-blue.svg)](https://frappeframework.com/)
[![ASHRAE TC 9.9](https://img.shields.io/badge/ASHRAE-TC%209.9%20Thermal-orange.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Executive Overview & Real-World Client Problem

The exponential surge in AI GPU clusters and cloud infrastructure has transformed data center operations. Modern hyperscale and colocation facilities face critical operational friction:
1. **AI Power Density Spikes:** Server rack densities have jumped from 5kW to 30kW–100kW per enclosure. Unbalanced 3-phase branch circuits trigger upstream PDU breaker trips.
2. **PUE SLA Penalties:** Enterprise tenants enforce strict **Power Usage Effectiveness (PUE = Total Facility Energy / IT Equipment Energy)** contractual ceilings (e.g., target PUE $\le$ 1.35). Inefficiencies in Chiller/CRAH plants directly result in commercial billing SLA penalties.
3. **Complex Sub-Metered Power Billing:** Tenants cannot be billed on flat rates; invoicing requires dynamic metered kWh consumption combined with kVA peak demand and power factor adjustments.

This Frappe application functions as an intelligent DCIM bridge connecting IoT smart PDUs, UPS telemetry, and ERPNext billing.

---

## 🏛️ System Architecture Flow

```mermaid
flowchart TD
    A["Smart Rack PDUs & UPS Telemetry (SNMP / Modbus)"] -->|Real-time kW / kWh Ingestion| B["DCIM Telemetry Gateway"]
    B -->|Calculate PUE (Total Facility / IT Load)| C{"PUE SLA Analysis"}
    C -->|PUE <= Target (e.g. 1.25)| D["Green Status: Energy Efficient"]
    C -->|PUE > Target (e.g. 1.45)| E["PUE Excursion SLA Penalty Trigger"]
    B -->|Intake Temp & Humidity| F{"ASHRAE TC 9.9 Thermal Envelope (18°C-27°C)"}
    F -->|Hotspot Warning| G["CRAH Cooling Fan Speed Adjustment"]
    B -->|Aggregated Monthly kWh & Peak kVA| H["Tenant Colocation Billing Engine"]
    H -->|Base U-Space Rent + Metered kWh| I["ERPNext Automated Monthly Invoice"]
```

---

## 🚀 Key Engineering Capabilities

- **Real-Time PUE Monitoring:** Continuously computes Power Usage Effectiveness across individual data halls and entire campus facilities.
- **ASHRAE TC 9.9 Thermal Guard:** Flags hot-aisle/cold-aisle temperature breaches before server throttling occurs.
- **Multi-Tenant Colocation Invoicing:** Automatically calculates base U-rack space rent, metered kWh consumption charges, and peak demand surcharges.
- **3-Phase Circuit Load Balancing:** Identifies phase imbalances (Phase A vs B vs C) across floor power distribution units (PDUs).

---

## 📂 Frappe DocType Schema & Data Structure

```text
datacenter_dcim_billing/
├── datacenter_dcim_billing_core/
│   ├── doctype/
│   │   ├── dcim_rack_meter/
│   │   │   ├── dcim_rack_meter.json
│   │   │   ├── dcim_rack_meter.py
│   │   │   └── dcim_rack_meter.js
│   │   └── dcim_pue_log/
│   │       └── dcim_pue_log.json
│   └── workspace/
│       └── datacenter_dcim_billing_workspace/
│           └── datacenter_dcim_billing_workspace.json
```

---

## ⚡ Frappe Hooks & Whitelisted APIs

- **REST Endpoint:** `POST /api/method/datacenter_dcim_billing.api.ingest_rack_telemetry`
- **Whitelisted Method:** `@frappe.whitelist() def generate_colocation_monthly_bill(rack_id, kwh_consumed, rate_per_kwh, base_rack_rent)`
- **Hooks Event:** `scheduler_events.hourly` triggers facility-wide PUE metric calculations.

---

## 🛠️ Installation & Bench Setup

```bash
bench get-app https://github.com/shyampandey1104/frappe-data-center-pue-rack-dcim-billing
bench --site erp.yourdomain.com install-app datacenter_dcim_billing
bench --site erp.yourdomain.com migrate
python3 -m unittest discover tests
```

---

## 📄 License
MIT License. Optimized for Colocation Providers, Edge DC Operators, and AI Compute Clusters.
