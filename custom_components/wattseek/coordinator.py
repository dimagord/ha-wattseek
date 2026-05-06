"""DataUpdateCoordinator for Wattseek Solar."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import WattseekApi, WattseekApiError, WattseekAuthError
from .const import DOMAIN, SCAN_INTERVAL_SECONDS, ATTR_NAME_MAP

_LOGGER = logging.getLogger(__name__)


class WattseekCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to fetch data from Wattseek API."""

    def __init__(self, hass: HomeAssistant, api: WattseekApi) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self.api = api
        self.plants: list[dict[str, Any]] = []
        self.devices: list[dict[str, Any]] = []

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the API."""
        try:
            # Get plants
            self.plants = await self.api.get_plants()
            if not self.plants:
                return {}

            result: dict[str, Any] = {"plants": {}, "devices": {}}

            for plant in self.plants:
                plant_id = plant["plantId"]

                # Fetch all plant-level data in parallel-ish fashion
                flow = await self.api.get_plant_flow(plant_id)
                generation = await self.api.get_plant_generation(plant_id)
                consumption = await self.api.get_plant_consumption(plant_id)
                battery = await self.api.get_plant_battery(plant_id)
                grid = await self.api.get_plant_grid(plant_id)

                result["plants"][plant_id] = {
                    "info": plant,
                    "flow": flow,
                    "generation": generation,
                    "consumption": consumption,
                    "battery": battery,
                    "grid": grid,
                }

                # Get devices for this plant
                devices = await self.api.get_devices(plant_id)
                self.devices = devices

                for device in devices:
                    device_id = device["deviceId"]
                    device_type = device.get("deviceType", "")

                    if device_type == "INVERTER":
                        detail = await self.api.get_device_detail(device_id)
                        _LOGGER.debug(
                            "Device %s detail response keys: %s",
                            device_id,
                            list(detail.keys()) if isinstance(detail, dict) else type(detail),
                        )
                        attrs = self._parse_device_attrs(detail)
                        _LOGGER.debug(
                            "Device %s parsed attrs: %s",
                            device_id,
                            list(attrs.keys()) if attrs else "EMPTY",
                        )
                        if not attrs and isinstance(detail, dict):
                            # Log raw structure to help debug
                            for k, v in detail.items():
                                if isinstance(v, list) and v:
                                    _LOGGER.debug(
                                        "Device detail key '%s': list of %d items, first item keys: %s",
                                        k, len(v),
                                        list(v[0].keys()) if isinstance(v[0], dict) else type(v[0]),
                                    )
                                elif isinstance(v, dict):
                                    _LOGGER.debug(
                                        "Device detail key '%s': dict with keys: %s",
                                        k, list(v.keys()),
                                    )
                                else:
                                    _LOGGER.debug("Device detail key '%s': %s", k, repr(v)[:200])
                        result["devices"][device_id] = {
                            "info": device,
                            "attrs": attrs,
                            "detail_raw": detail,
                        }
                    else:
                        result["devices"][device_id] = {
                            "info": device,
                            "attrs": {},
                            "detail_raw": {},
                        }

            return result

        except WattseekAuthError as err:
            raise UpdateFailed(f"Authentication failed: {err}") from err
        except WattseekApiError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

    @staticmethod
    def _parse_device_attrs(detail: dict[str, Any]) -> dict[str, Any]:
        """Parse device detail attributes into a flat dict with English keys."""
        attrs: dict[str, Any] = {}
        for module in detail.get("attrModuleList", []):
            for attr in module.get("attrList", []):
                cn_name = attr.get("attrName", "")
                en_key = ATTR_NAME_MAP.get(cn_name)
                if en_key:
                    value = attr.get("attrValue")
                    unit = attr.get("attrUnit")
                    try:
                        value = float(value)
                    except (TypeError, ValueError):
                        pass
                    attrs[en_key] = {"value": value, "unit": unit}
        return attrs
