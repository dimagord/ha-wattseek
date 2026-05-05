"""Wattseek Solar API client."""

from __future__ import annotations

import hashlib
import logging
from typing import Any

import aiohttp

from .const import API_LOGIN, API_LOGOUT, API_PROXY, API_USER

_LOGGER = logging.getLogger(__name__)


class WattseekApiError(Exception):
    """Base exception for Wattseek API errors."""


class WattseekAuthError(WattseekApiError):
    """Authentication error."""


class WattseekApi:
    """API client for Wattseek Solar platform."""

    def __init__(
        self,
        username: str,
        password: str,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initialize the API client."""
        self._username = username
        self._password = password
        self._session = session
        self._own_session = session is None
        self._authenticated = False

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure we have an aiohttp session."""
        if self._session is None or self._session.closed:
            jar = aiohttp.CookieJar()
            self._session = aiohttp.ClientSession(cookie_jar=jar)
            self._own_session = True
            self._authenticated = False
        return self._session

    async def authenticate(self) -> bool:
        """Authenticate with the Wattseek API."""
        session = await self._ensure_session()

        password_md5 = hashlib.md5(
            self._password.encode("utf-8")
        ).hexdigest()

        payload = {
            "username": self._username.strip(),
            "password": password_md5,
        }

        try:
            async with session.post(API_LOGIN, json=payload) as resp:
                data = await resp.json()

                if data.get("code") != "000200":
                    msg = data.get("msg", "Unknown error")
                    _LOGGER.error("Wattseek login failed: %s", msg)
                    raise WattseekAuthError(f"Login failed: {msg}")

                self._authenticated = True
                _LOGGER.debug("Wattseek authentication successful")
                return True
        except aiohttp.ClientError as err:
            raise WattseekApiError(f"Connection error: {err}") from err

    async def _request(
        self, method: str, url: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Make an authenticated API request."""
        session = await self._ensure_session()

        if not self._authenticated:
            await self.authenticate()

        try:
            async with session.request(method, url, **kwargs) as resp:
                data = await resp.json()

                # Session expired — re-auth once
                if data.get("code") in ("000401", "000403"):
                    _LOGGER.debug("Session expired, re-authenticating")
                    self._authenticated = False
                    await self.authenticate()
                    async with session.request(method, url, **kwargs) as resp2:
                        data = await resp2.json()

                if data.get("code") != "000200":
                    raise WattseekApiError(
                        f"API error {data.get('code')}: {data.get('msg')}"
                    )

                return data.get("data", {})
        except aiohttp.ClientError as err:
            raise WattseekApiError(f"Connection error: {err}") from err

    async def _get(self, path: str, **params: Any) -> dict[str, Any]:
        """GET request to the proxy API."""
        url = f"{API_PROXY}/{path}"
        return await self._request("GET", url, params=params or None)

    async def _post(self, path: str, payload: dict | None = None) -> dict[str, Any]:
        """POST request to the proxy API."""
        url = f"{API_PROXY}/{path}"
        return await self._request("POST", url, json=payload)

    # ── Plant endpoints ──────────────────────────────────────────────────────

    async def get_plants(self) -> list[dict[str, Any]]:
        """Get list of plants."""
        data = await self._get("plant/page", current=1, pageSize=99)
        return data.get("data", [])

    async def get_plant(self, plant_id: str) -> dict[str, Any]:
        """Get single plant info."""
        return await self._get(f"plant/{plant_id}")

    # ── Device endpoints ─────────────────────────────────────────────────────

    async def get_devices(self, plant_id: str) -> list[dict[str, Any]]:
        """Get list of devices for a plant."""
        data = await self._get(
            "device/page", current=1, pageSize=99, plantId=plant_id
        )
        return data.get("data", [])

    async def get_device_detail(self, device_id: str) -> dict[str, Any]:
        """Get detailed device info with realtime attributes."""
        return await self._get(
            f"device/{device_id}/detailInfo",
            barType="REALTIME_INFO,BASE_INFO",
        )

    # ── Realtime plant statistics ────────────────────────────────────────────

    async def get_plant_flow(self, plant_id: str) -> dict[str, Any]:
        """Get realtime power flow for a plant."""
        return await self._get(
            f"statistic/realtime/plant/{plant_id}/flow/v2"
        )

    async def get_plant_generation(self, plant_id: str) -> dict[str, Any]:
        """Get PV generation statistics."""
        return await self._get(
            f"statistic/realtime/plant/{plant_id}/generator"
        )

    async def get_plant_consumption(self, plant_id: str) -> dict[str, Any]:
        """Get load consumption statistics."""
        return await self._get(
            f"statistic/realtime/plant/{plant_id}/use"
        )

    async def get_plant_battery(self, plant_id: str) -> dict[str, Any]:
        """Get battery statistics."""
        return await self._get(
            f"statistic/realtime/plant/{plant_id}/battery"
        )

    async def get_plant_grid(self, plant_id: str) -> dict[str, Any]:
        """Get grid statistics."""
        return await self._get(
            f"statistic/realtime/plant/{plant_id}/grid"
        )

    # ── Device realtime flow ─────────────────────────────────────────────────

    async def get_device_flow(self, device_id: str) -> dict[str, Any]:
        """Get realtime power flow for a device."""
        return await self._get(
            f"statistic/realtime/device/{device_id}/flow"
        )

    # ── Cleanup ──────────────────────────────────────────────────────────

    async def close(self) -> None:
        """Close the session."""
        if self._own_session and self._session and not self._session.closed:
            await self._session.close()
