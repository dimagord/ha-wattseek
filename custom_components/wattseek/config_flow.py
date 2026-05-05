"""Config flow for Wattseek Solar integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import WattseekApi, WattseekApiError, WattseekAuthError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class WattseekConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Wattseek Solar."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            # Check for duplicate entries
            await self.async_set_unique_id(username.lower())
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            api = WattseekApi(username, password, session=session)
            try:
                await api.authenticate()
                plants = await api.get_plants()
            except WattseekAuthError as err:
                _LOGGER.error("Wattseek auth error: %s", err)
                errors["base"] = "invalid_auth"
            except WattseekApiError as err:
                _LOGGER.error("Wattseek API error: %s", err)
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during Wattseek setup")
                errors["base"] = "unknown"
            else:
                plant_name = plants[0]["plantName"] if plants else "Wattseek"
                return self.async_create_entry(
                    title=plant_name,
                    data=user_input,
                )
            finally:
                await api.close()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
