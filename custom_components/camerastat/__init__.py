"""The Camera Statistic integration."""
from __future__ import annotations
from homeassistant.components.camerastat.coordinator import CameraStatCoordinator

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Camera Statistic from a config entry."""

    coordinator = CameraStatCoordinator(hass, config_entry)

    # Query the device for the first time and initialise coordinator.data
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, (Platform.SENSOR,))

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(
        config_entry, (Platform.SENSOR,)
    )
