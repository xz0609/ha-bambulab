"""Image platform."""
from __future__ import annotations

from homeassistant.components.image import ImageEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN, LOGGER
from .coordinator import BambuDataUpdateCoordinator
from .models import BambuLabEntity
from .definitions import CHAMBER_IMAGE_SENSOR, COVER_IMAGE_SENSOR, BambuLabSensorEntityDescription

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Everything but the Kitchen Sink config entry."""

    LOGGER.debug("IMAGE::async_setup_entry")
    coordinator: BambuDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    if CHAMBER_IMAGE_SENSOR.exists_fn(coordinator):
        chamber_image = ChamberImage(hass, coordinator, CHAMBER_IMAGE_SENSOR)
        async_add_entities([chamber_image])
        coordinator.ChamberImage = chamber_image

    if COVER_IMAGE_SENSOR.exists_fn(coordinator):
        cover_image = CoverImage(hass, coordinator, COVER_IMAGE_SENSOR)
        async_add_entities([cover_image])
        #coordinator.CoverImage = cover_image


class ChamberImage(ImageEntity, BambuLabEntity):
    """Representation of an image entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: BambuDataUpdateCoordinator,
        description: BambuLabSensorEntityDescription
    ) -> None:
        """Initialize the image entity."""
        super().__init__(hass=hass)
        super(BambuLabEntity, self).__init__(coordinator=coordinator)
        self._attr_content_type = "image/jpeg"
        self._image_filename = None
        self.entity_description = description
        printer = self.coordinator.get_model().info
        self._attr_unique_id = f"{printer.serial}_{description.key}"

    def image(self) -> bytes | None:
        """Return bytes of image."""

        return self.coordinator.get_model().chamber_image.get_jpeg()

    def image_updated(self):
        self._attr_image_last_updated = dt_util.utcnow()

class CoverImage(ImageEntity, BambuLabEntity):
    """Representation of an image entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: BambuDataUpdateCoordinator,
        description: BambuLabSensorEntityDescription
    ) -> None:
        """Initialize the image entity."""
        super().__init__(hass=hass)
        super(BambuLabEntity, self).__init__(coordinator=coordinator)
        self._attr_content_type = "image/jpeg"
        self._image_filename = None
        self.entity_description = description
        printer = self.coordinator.get_model().info
        self._attr_unique_id = f"{printer.serial}_{description.key}"

    def image(self) -> bytes | None:
        """Return bytes of image."""

        return self.coordinator.get_model().cover_image.get_jpeg()

    def image_updated(self):
        self._attr_image_last_updated = dt_util.utcnow()