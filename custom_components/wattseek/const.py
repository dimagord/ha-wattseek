"""Constants for the Wattseek Solar integration."""

DOMAIN = "wattseek"

CONF_USERNAME = "username"
CONF_PASSWORD = "password"

BASE_URL = "https://solar.wattseek.com"

API_BASE = f"{BASE_URL}/apis"
API_LOGIN = f"{API_BASE}/account/login/by/password"
API_LOGOUT = f"{API_BASE}/account/logout"
API_USER = f"{API_BASE}/account/user"
API_PROXY = f"{API_BASE}/common/proxy/sysApiCommon"

SCAN_INTERVAL_SECONDS = 60

ATTR_NAME_MAP: dict[str, str] = {
    # General
    "Device SN(ASCII)": "device_sn",
    "App version": "app_version",
    "Protocol version": "protocol_version",
    "Running mode": "running_mode",
    # Grid
    "Grid voltage": "grid_voltage",
    "Grid current": "grid_current",
    "Grid frequency": "grid_frequency",
    "Grid power": "grid_power",
    # PV
    "PV1 voltage": "pv1_voltage",
    "PV1 current": "pv1_current",
    "PV1 power": "pv1_power",
    # Battery
    "Battery voltage": "battery_voltage",
    "Battery current": "battery_current",
    "Battery capacity(Percentage)": "battery_soc",
    "BMS-Real time SOC": "bms_soc",
    "BMS-Average SOH": "bms_soh",
    "BMS-Single core maximum temperature": "bms_max_cell_temp",
    "BMS-Maximum charging current": "bms_max_charge_current",
    "BMS-Maximum discharge current": "bms_max_discharge_current",
    "BMS-Communication status": "bms_comm_status",
    "BMS-Networking status": "bms_network_status",
    # Output / Load
    "Output voltage": "output_voltage",
    "Output current": "output_current",
    "Output frequency": "output_frequency",
    "Output active power": "output_active_power",
    "Output apparent power": "output_apparent_power",
    "Output percentage": "output_percentage",
    # Statistics
    "Electricity fed into grid of the day": "grid_export_today",
    "Electricity fed into grid of the month": "grid_export_month",
    "Electricity fed into grid of the year": "grid_export_year",
    "Total electricity fed into grid": "grid_export_total",
    "Electricity purchased of the day": "grid_import_today",
    "Electricity purchased of the month": "grid_import_month",
    "Electricity purchased of the year": "grid_import_year",
    "Total electricity purchased": "grid_import_total",
    "Electricity outputed of the day": "load_energy_today",
    "Electricity outputed of the month": "load_energy_month",
    "Electricity outputed of the year": "load_energy_year",
    "Total electricity outputed": "load_energy_total",
    "PV power generation of the day": "pv_energy_today",
    "PV power generation of the month": "pv_energy_month",
    "PV power generation of the year": "pv_energy_year",
    "Total PV power generation": "pv_energy_total",
}
