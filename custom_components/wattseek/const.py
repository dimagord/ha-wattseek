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
    # General / 通用
    "机器SN码(ASCII)": "device_sn",
    "软件版本号": "app_version",
    "协议版本号": "protocol_version",
    "运行模式": "running_mode",
    # Grid / 电网
    "电网电压": "grid_voltage",
    "电网电流": "grid_current",
    "电网频率": "grid_frequency",
    "电网功率": "grid_power",
    # PV / 光伏
    "PV1电压": "pv1_voltage",
    "PV1电流": "pv1_current",
    "PV1功率": "pv1_power",
    # Battery / 电池
    "电池电压": "battery_voltage",
    "电池电流": "battery_current",
    "电池容量百分比": "battery_soc",
    "BMS-实时SOC": "bms_soc",
    "BMS-平均SOH": "bms_soh",
    "BMS-单芯最高温度": "bms_max_cell_temp",
    "BMS-最大充电电流": "bms_max_charge_current",
    "BMS-最大放电电流": "bms_max_discharge_current",
    "电池功率": "battery_power_detail",
    "电池温度": "battery_temperature",
    # Load / 负载
    "输出电压": "output_voltage",
    "输出电流": "output_current",
    "输出频率": "output_frequency",
    "输出有功功率": "output_active_power",
    "输出视在功率": "output_apparent_power",
    "输出百分比": "output_percentage",
    # Statistics / 统计
    "当日市电馈网电量": "grid_export_today",
    "当月市电馈网电量": "grid_export_month",
    "当年市电馈网电量": "grid_export_year",
    "总市电馈网电量": "grid_export_total",
    "当日市电用电量": "grid_import_today",
    "当月市电用电量": "grid_import_month",
    "当年市电用电量": "grid_import_year",
    "总市电用电量": "grid_import_total",
    "当日输出电量": "load_energy_today",
    "当月输出电量": "load_energy_month",
    "当年输出电量": "load_energy_year",
    "总输出电量": "load_energy_total",
    "当日光伏发电量": "pv_energy_today",
    "当月光伏发电量": "pv_energy_month",
    "当年光伏发电量": "pv_energy_year",
    "总光伏发电量": "pv_energy_total",
}
