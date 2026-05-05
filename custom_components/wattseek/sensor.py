"""Sensor platform for Wattseek Solar."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WattseekCoordinator


@dataclass(frozen=True, kw_only=True)
class WattseekSensorDescription(SensorEntityDescription):
    """Describe a Wattseek sensor."""

    value_path: str  # dot-separated path into coordinator data
    category: str = "plant"  # "plant" or "device"


# -- Plant-level flow sensors --

PLANT_FLOW_SENSORS: tuple[WattseekSensorDescription, ...] = (
    WattseekSensorDescription(
        key="pv_power",
        translation_key="pv_power",
        name="PV Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="flow.pvPower",
    ),
    WattseekSensorDescription(
        key="grid_power",
        translation_key="grid_power",
        name="Grid Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="flow.gridPower",
    ),
    WattseekSensorDescription(
        key="load_power",
        translation_key="load_power",
        name="Load Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="flow.loadPower",
    ),
    WattseekSensorDescription(
        key="battery_power",
        translation_key="battery_power",
        name="Battery Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="flow.batteryPower",
    ),
    WattseekSensorDescription(
        key="battery_soc",
        translation_key="battery_soc",
        name="Battery SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="flow.realTimeSOC",
    ),
)

# -- Plant generation stats --

PLANT_GENERATION_SENSORS: tuple[WattseekSensorDescription, ...] = (
    WattseekSensorDescription(
        key="generation_power",
        name="Generation Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="generation.generationPower",
    ),
    WattseekSensorDescription(
        key="generation_today",
        name="Generation Today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_path="generation.generationDay",
    ),
    WattseekSensorDescription(
        key="generation_month",
        name="Generation This Month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="generation.generationMonth",
    ),
    WattseekSensorDescription(
        key="generation_year",
        name="Generation This Year",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="generation.generationYear",
    ),
    WattseekSensorDescription(
        key="generation_total",
        name="Generation Total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="generation.generationTotal",
    ),
)

# -- Plant consumption stats --

PLANT_CONSUMPTION_SENSORS: tuple[WattseekSensorDescription, ...] = (
    WattseekSensorDescription(
        key="consumption_power",
        name="Consumption Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="consumption.usePower",
    ),
    WattseekSensorDescription(
        key="consumption_today",
        name="Consumption Today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_path="consumption.useDay",
    ),
    WattseekSensorDescription(
        key="consumption_month",
        name="Consumption This Month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="consumption.useMonth",
    ),
    WattseekSensorDescription(
        key="consumption_year",
        name="Consumption This Year",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="consumption.useYear",
    ),
    WattseekSensorDescription(
        key="consumption_total",
        name="Consumption Total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="consumption.useTotal",
    ),
)

# -- Plant grid stats --

PLANT_GRID_SENSORS: tuple[WattseekSensorDescription, ...] = (
    WattseekSensorDescription(
        key="grid_import_today",
        name="Grid Import Today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_path="grid.buyDay",
    ),
    WattseekSensorDescription(
        key="grid_import_month",
        name="Grid Import This Month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="grid.buyMonth",
    ),
    WattseekSensorDescription(
        key="grid_import_year",
        name="Grid Import This Year",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="grid.buyYear",
    ),
    WattseekSensorDescription(
        key="grid_import_total",
        name="Grid Import Total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="grid.buyTotal",
    ),
    WattseekSensorDescription(
        key="grid_export_today",
        name="Grid Export Today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_path="grid.sellDay",
    ),
    WattseekSensorDescription(
        key="grid_export_month",
        name="Grid Export This Month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="grid.sellMonth",
    ),
    WattseekSensorDescription(
        key="grid_export_total",
        name="Grid Export Total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="grid.sellTotal",
    ),
)

# -- Plant battery stats --

PLANT_BATTERY_SENSORS: tuple[WattseekSensorDescription, ...] = (
    WattseekSensorDescription(
        key="battery_charge_today",
        name="Battery Charge Today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_path="battery.chargeDay",
    ),
    WattseekSensorDescription(
        key="battery_charge_total",
        name="Battery Charge Total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="battery.chargeTotal",
    ),
    WattseekSensorDescription(
        key="battery_discharge_today",
        name="Battery Discharge Today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_path="battery.dischargeDay",
    ),
    WattseekSensorDescription(
        key="battery_discharge_total",
        name="Battery Discharge Total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_path="battery.dischargeTotal",
    ),
)

# -- Device (inverter) sensors --

DEVICE_SENSORS: tuple[WattseekSensorDescription, ...] = (
    WattseekSensorDescription(
        key="inv_grid_voltage",
        name="Grid Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.grid_voltage.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_grid_current",
        name="Grid Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.grid_current.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_grid_frequency",
        name="Grid Frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.grid_frequency.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_grid_power",
        name="Inverter Grid Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.grid_power.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_pv1_voltage",
        name="PV1 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.pv1_voltage.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_pv1_current",
        name="PV1 Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.pv1_current.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_pv1_power",
        name="PV1 Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.pv1_power.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_battery_voltage",
        name="Battery Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.battery_voltage.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_battery_current",
        name="Battery Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.battery_current.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_battery_soc",
        name="Battery SOC (Inverter)",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.battery_soc.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_bms_max_cell_temp",
        name="BMS Max Cell Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.bms_max_cell_temp.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_output_voltage",
        name="Output Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.output_voltage.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_output_current",
        name="Output Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.output_current.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_output_frequency",
        name="Output Frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.output_frequency.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_output_active_power",
        name="Output Active Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.output_active_power.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_output_apparent_power",
        name="Output Apparent Power",
        native_unit_of_measurement="VA",
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.output_apparent_power.value",
        category="device",
    ),
    WattseekSensorDescription(
        key="inv_output_percentage",
        name="Output Load Percentage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_path="attrs.output_percentage.value",
        category="device",
    ),
)


def _resolve_path(data: dict[str, Any], path: str) -> Any:
    """Resolve a dot-separated path in a nested dict."""
    current = data
    for key in path.split("."):
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wattseek sensors from a config entry."""
    coordinator: WattseekCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = []

    data = coordinator.data or {}

    # Plant sensors
    for plant_id, plant_data in data.get("plants", {}).items():
        plant_info = plant_data["info"]
        plant_name = plant_info.get("plantName", "Wattseek Plant")

        all_plant_sensors = (
            PLANT_FLOW_SENSORS
            + PLANT_GENERATION_SENSORS
            + PLANT_CONSUMPTION_SENSORS
            + PLANT_GRID_SENSORS
            + PLANT_BATTERY_SENSORS
        )

        for desc in all_plant_sensors:
            entities.append(
                WattseekPlantSensor(
                    coordinator=coordinator,
                    description=desc,
                    plant_id=plant_id,
                    plant_name=plant_name,
                )
            )

    # Device sensors
    for device_id, device_data in data.get("devices", {}).items():
        device_info = device_data["info"]
        if device_info.get("deviceType") != "INVERTER":
            continue

        device_sn = device_info.get("deviceSn", device_id)
        device_model = device_info.get("deviceModel", "Unknown")

        for desc in DEVICE_SENSORS:
            entities.append(
                WattseekDeviceSensor(
                    coordinator=coordinator,
                    description=desc,
                    device_id=device_id,
                    device_sn=device_sn,
                    device_model=device_model,
                )
            )

    async_add_entities(entities)


class WattseekPlantSensor(CoordinatorEntity[WattseekCoordinator], SensorEntity):
    """Sensor for plant-level data."""

    entity_description: WattseekSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: WattseekCoordinator,
        description: WattseekSensorDescription,
        plant_id: str,
        plant_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._plant_id = plant_id
        self._attr_unique_id = f"{plant_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, plant_id)},
            name=plant_name,
            manufacturer="Wattseek / JDSolar",
            model="Solar Plant",
            entry_type=None,
        )

    @property
    def native_value(self) -> float | int | str | None:
        """Return the sensor value."""
        plant_data = (self.coordinator.data or {}).get("plants", {}).get(
            self._plant_id
        )
        if plant_data is None:
            return None
        return _resolve_path(plant_data, self.entity_description.value_path)


class WattseekDeviceSensor(CoordinatorEntity[WattseekCoordinator], SensorEntity):
    """Sensor for device-level data (inverter)."""

    entity_description: WattseekSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: WattseekCoordinator,
        description: WattseekSensorDescription,
        device_id: str,
        device_sn: str,
        device_model: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=f"Inverter {device_sn}",
            manufacturer="JDSolar",
            model=device_model,
            serial_number=device_sn,
        )

    @property
    def native_value(self) -> float | int | str | None:
        """Return the sensor value."""
        device_data = (self.coordinator.data or {}).get("devices", {}).get(
            self._device_id
        )
        if device_data is None:
            return None
        return _resolve_path(device_data, self.entity_description.value_path)
