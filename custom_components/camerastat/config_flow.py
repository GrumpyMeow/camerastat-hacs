"""Config flow for Camera Statistic integration."""
from __future__ import annotations

from typing import Any
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

import voluptuous as vol

from homeassistant.components.camera import DOMAIN as CAMERA_DOMAIN
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.const import CONF_ENTITY_ID, CONF_SCAN_INTERVAL
from homeassistant.helpers import entity_registry as er, selector

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): selector.EntitySelector(
            selector.EntitySelectorConfig(domain=CAMERA_DOMAIN)
        ),
        vol.Required(CONF_SCAN_INTERVAL, default=60): vol.All(
            vol.Coerce(int), vol.Range(min=5, max = 86400)
        )
    }
)



class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Camera Statistic."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        # Retrieve camera entity from registry
        registry = er.async_get(self.hass)
        camera_entity_entry = registry.async_get(user_input[CONF_ENTITY_ID])
        _LOGGER.debug(camera_entity_entry)

        return self.async_create_entry(
            title=f"Statistic for {camera_entity_entry.name}",
            data=user_input            
        )
