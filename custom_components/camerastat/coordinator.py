"""Support for Neato botvac connected vacuum cleaners."""
from datetime import timedelta
from io import BytesIO, StringIO
import logging
from .const import BANDS, DOMAIN

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import CONF_ENTITY_ID, CONF_SCAN_INTERVAL
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.components.camera import Image
from PIL import ImageStat, Image as PImage

_LOGGER = logging.getLogger(__name__)


class CameraStatCoordinator(DataUpdateCoordinator):
    """Coordinator class."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=config_entry.data[CONF_SCAN_INTERVAL]),
        )        

        self._camera_entity_id = config_entry.data[CONF_ENTITY_ID]
        self.device_id = config_entry.entry_id

        assert self.device_id is not None
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name=config_entry.title
        )
   
    async def _async_update_data(self) -> dict:
        """Fetch the data from the device."""
        data = dict()

        _LOGGER.debug("_async_update_data")
        camera = self.hass.components.camera

        try:
            image: Image = await camera.async_get_image(
                self._camera_entity_id, timeout=30
            )

            img = BytesIO(image.content)
        
            im = PImage.open( img,"r")
            
            stat = ImageStat.Stat(im)
            for bi in range(len(BANDS)):
                data[BANDS[bi] + "_STDDEV"] = stat.stddev[bi]
                data[BANDS[bi] + "_MEAN"] = stat.mean[bi]
                data[BANDS[bi] + "_MEDIAN"] = stat.median[bi]
                data[BANDS[bi] + "_RMS"] = stat.rms[bi]
                data[BANDS[bi] + "_VAR"] = stat.var[bi]
                data[BANDS[bi] + "_SUM"] = stat.sum[bi]

            img.close()
            im.close()
            return data

        except HomeAssistantError as err:
            _LOGGER.error("Error on receive image from entity: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}")


        
