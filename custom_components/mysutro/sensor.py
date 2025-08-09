""" Represents a sensor entity for the Sutro device """


import datetime
import logging
from typing import Any
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

import dateutil.parser
from . import MySutroEntity
from .const import DOMAIN, PROP_MAP

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback) -> None: # pylint: disable=line-too-long
    """Set up entry."""
    entities = []
    coordinator = hass.data.get(DOMAIN, {}).get(entry.entry_id, {}).get("coordinator")
    if not coordinator:
        _LOGGER.error("Coordinator not found for entry %s", entry.entry_id)
        return

    entities.append(MySutroSensor(coordinator, 'ph'))
    entities.append(MySutroSensor(coordinator, 'chlorine'))
    entities.append(MySutroSensor(coordinator, 'alkalinity'))
    entities.append(MySutroSensor(coordinator, 'bromine'))

    entities.append(MySutroTimeStamp(coordinator, 'readingTime'))

    async_add_entities(entities)


class MySutroSensor(MySutroEntity, SensorEntity):
    """ Represents a sutro sensor """
    def __init__(self, coordinator: DataUpdateCoordinator, data_key: str) -> None:
        super().__init__(coordinator, data_key)
        self.native_min_value = PROP_MAP[data_key]['min']
        self.native_max_value = PROP_MAP[data_key]['max']
        self.native_step = PROP_MAP[data_key]['step']
        self._attr_state_class = 'measurement'

    @property
    def name(self) -> str:
        return self._data_key

    @property
    def unique_id(self) -> str:
        return f"{super().unique_id}_{self._data_key}"

    @property
    def value(self) -> float:
        """ Returns the value of the sensor """
        # return self.gateway.data.me.pool.latestReading
        return self.gateway.data[self._data_key]

    @property
    def native_value(self) -> float:
        # return self.gateway.data.me.pool.latestReading
        return self.gateway.data[self._data_key]

    @property
    def data_valid(self) -> bool:
        """ Returns true is data is valid, always true """
        return True


class MySutroTimeStamp(MySutroEntity, SensorEntity):
    """ Represents a timestamp """
    def __init__(self, coordinator: Any, data_key: str) -> None:
        super().__init__(coordinator, data_key)
        # self._attr_state_class = 'measurement'
        self._attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def name(self) -> str:
        return self._data_key

    @property
    def unique_id(self) -> str:
        return f"{super().unique_id}_{self._data_key}"

    @property
    def value(self) -> datetime.datetime:
        """ Returns value as timestamp """
        return dateutil.parser.parse(self.gateway.data[self._data_key])

    @property
    def native_value(self) -> datetime.datetime:
        """ Returns value as timestamp """
        return self.value

    @property
    def data_valid(self) -> bool:
        """ Returns true is data is valid, always true """
        return True
