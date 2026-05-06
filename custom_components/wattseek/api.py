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
        self._token: str | None = None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure we have an aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
            self._own_session = True
            self._token = None
        return self._session

    def _headers(self) -> dict[str, str]:
        """Build common request headers."""
        hdrs: dict[str, str] = {
            "x-locale": "en-US",
            "x-org-id": "",
        }
        if self._token:
            hdrs["x-auth-token"] = self._token
        return hdrs

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
            async with session.post(
                API_LOGIN, json=payload, headers=self._headers()
            ) as resp:
                data = await resp.json()

                status = data.get("status")
                if status != 0:
                    msg = data.get("message") or data.get("msg", "Unknown error")
                    _LOGGER.error("Wattseek login failed: %s (status=%s)", msg, status)
                    raise WattseekAuthError(f"Login failed: {msg}")

                result = data.get("data", {})
                self._token = result.get("token")
                if not self._token:
                    raise WattseekAuthError("Login succeeded but no token returned")

                _LOGGER.debug("Wattseek authentication successful")
                return True
        except aiohttp.ClientError as err:
            raise WattseekApiError(f"Connection error: {err}") from err

    @staticmethod
    def _is_success(data: dict[str, Any]) -> bool:
        """Check if API response indicates success.

        Login endpoint returns {status: 0, data: ...}.
        Proxy API returns {code: "000200", data: ...}.
        """
        status = data.get("status")
        if status == 0:
            return True
        code = str(data.get("code", ""))
        if code == "000200":
            return True
        return False

    @staticmethod
    def _is_session_expired(data: dict[str, Any]) -> bool:
        """Check if the response indicates an expired session."""
        if data.get("status") == 401:
            return True
        code = str(data.get("code", ""))
        if code in ("010002", "010003", "401"):
            return True
        return False

    async def _request(
        self, method: str, url: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Make an authenticated API request."""
        session = await self._ensure_session()

        if not self._token:
            await self.authenticate()

        kwargs.setdefault("headers", {})
        kwargs["headers"].update(self._headers())

        try:
            async with session.request(method, url, **kwargs) as resp:
                data = await resp.json()

                # Session expired — re-auth once
                if self._is_session_expired(data):
                    _LOGGER.debug("Session expired, re-authenticating")
                    self._token = None
                    await self.authenticate()
                    kwargs["headers"].update(self._headers())
                    async with session.request(method, url, **kwargs) as resp2:
                        data = await resp2.json()

                if not self._is_success(data):
                    code = data.get("code", "")
                    status = data.get("status")
                    msg = data.get("message") or data.get("msg", "Unknown error")
                    raise WattseekApiError(
                        f"API error (status={status}, code={code}): {msg}"
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

    # ── Realtime plant statistics ──────────────────────────────────────────

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
