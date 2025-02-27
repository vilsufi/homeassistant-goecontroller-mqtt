"""MQTT component mixins and helpers."""
from homeassistant import config_entries
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.util import slugify

from .const import (
    CONF_SERIAL_NUMBER,
    CONF_TOPIC_PREFIX,
    DEVICE_INFO_MANUFACTURER,
    DEVICE_INFO_MODEL,
    DOMAIN,
)
from .definitions import GoEControllerEntityDescription


class GoEControllerEntity(Entity):
    """Common go-eController entity."""

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEControllerEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        topic_prefix = config_entry.data[CONF_TOPIC_PREFIX]
        serial_number = config_entry.data[CONF_SERIAL_NUMBER]

        topic = description.topic if description.topic else description.key
        self._topic = f"{topic_prefix}/{serial_number}/{topic}"

        slug = slugify(f"{topic_prefix}_{serial_number}_{description.key}")
        self.entity_id = f"{description.domain}.{slug}"

        parsed_attribute = description.attribute
        if isinstance(description.attribute, tuple):
            parsed_attribute = "-".join(description.attribute)

        self._attr_unique_id = "-".join(
            [serial_number, description.domain, description.key, parsed_attribute]
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial_number)},
            name=config_entry.title,
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
        )
