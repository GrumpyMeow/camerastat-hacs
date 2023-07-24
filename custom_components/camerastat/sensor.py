"""Sensor platform for Camera Statistic integration."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from .coordinator import CameraStatCoordinator

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.components.sensor.const import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITY_ID, PERCENTAGE, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, BANDS
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType
import logging

_LOGGER = logging.getLogger(__name__)

@dataclass
class CameraStatEntityDescriptionMixin:
    """Class for keys required by Camera Stat entity."""

    value: Callable[[dict], float | int | None]


@dataclass
class CameraStatEntityDescription(SensorEntityDescription, CameraStatEntityDescriptionMixin):
    """Describes Camera Stat sensor entity."""


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize Camera Statistic config entry."""

    coordinator : CameraStatCoordinator = hass.data[DOMAIN][config_entry.entry_id]
 
    name = config_entry.title

    SENSOR_TYPES: list[CameraStatEntityDescription] = []
    for band in BANDS:
        SENSOR_TYPES.append(            
                CameraStatEntityDescription(
                    key=f"{band}_MEAN",
                    name=f"{name} {band} mean",
                    state_class=SensorStateClass.MEASUREMENT,
                    value=lambda data,key : data.get(key),
                    suggested_display_precision=0,
                )
        )
        SENSOR_TYPES.append(
                CameraStatEntityDescription(
                    key=f"{band}_STDDEV",
                    name=f"{name} {band} stddev",
                    state_class=SensorStateClass.MEASUREMENT,
                    value=lambda data,key : data.get(key),
                    suggested_display_precision=0,
                )
        )
        SENSOR_TYPES.append(
                CameraStatEntityDescription(
                    key=f"{band}_MEDIAN",
                    name=f"{name} {band} median",
                    state_class=SensorStateClass.MEASUREMENT,
                    value=lambda data,key : data.get(key),
                    suggested_display_precision= 0
                )
        )
        SENSOR_TYPES.append(
                CameraStatEntityDescription(
                    key=f"{band}_RMS",
                    name=f"{name} {band} rms",
                    state_class=SensorStateClass.MEASUREMENT,
                    value=lambda data,key : data.get(key),
                    suggested_display_precision=0,
                )
        )
        SENSOR_TYPES.append(
                CameraStatEntityDescription(
                    key=f"{band}_VAR",
                    name=f"{name} {band} var",
                    state_class=SensorStateClass.MEASUREMENT,
                    value=lambda data,key : data.get(key),
                    suggested_display_precision=0
                )
        )
        SENSOR_TYPES.append(
                CameraStatEntityDescription(
                    key=f"{band}_SUM",
                    name=f"{name} {band} sum",
                    state_class=SensorStateClass.MEASUREMENT,
                    value=lambda data,key : data.get(key),
                    suggested_display_precision=0
                )
        )


    entities: list[CameraStatSensorEntity] = []
    for description in SENSOR_TYPES:           
        entities.append(CameraStatSensorEntity(coordinator, description))

    async_add_entities(entities)

class CameraStatSensorEntity(CoordinatorEntity, SensorEntity):
    """Camera Statistic Sensor."""

    _attr_has_entity_name = True
    entity_description: CameraStatEntityDescription

    def __init__(
            self,
            coordinator,
            description: CameraStatEntityDescription,
        ) -> None:
        """Initialize Camera Statistic Sensor."""
        super().__init__(coordinator=coordinator)
        self.entity_description: CameraStatEntityDescription = description
        self._attr_unique_id = f"{coordinator.device_id}_{description.key}"
        self._attr_device_info = coordinator.device_info
        self._attr_native_value = description.value(coordinator.data, self.entity_description.key)


        
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.entity_description.value(self.coordinator.data, self.entity_description.key)
        self.async_write_ha_state()        
