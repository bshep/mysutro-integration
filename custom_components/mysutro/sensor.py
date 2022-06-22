import logging
from xmlrpc.client import Boolean

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers import entity_platform, config_validation as cv

from . import mySutroEntity
from .const import DOMAIN, PROP_MAP
import dateutil.parser

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up entry."""
    entities = []
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities.append(mySutroSensor(coordinator, 'ph'))
    entities.append(mySutroSensor(coordinator, 'chlorine'))
    entities.append(mySutroSensor(coordinator, 'alkalinity'))
    entities.append(mySutroSensor(coordinator, 'bromine'))

    entities.append(mySutroTimeStamp(coordinator, 'readingTime'))

    async_add_entities(entities)


class mySutroSensor(mySutroEntity, SensorEntity):
    def __init__(self, coordinator, data_key):
        super().__init__(coordinator, data_key)
        self.native_min_value = PROP_MAP[data_key]['min']
        self.native_max_value = PROP_MAP[data_key]['max']
        self.native_step = PROP_MAP[data_key]['step']
        self._attr_state_class = 'measurement'

    @property
    def name(self) -> str:
        return self._data_key

    @property
    def unique_id(self):
        return f"{super().unique_id}_{self._data_key}"

    @property
    def value(self) -> float:
        # return self.gateway.data.me.pool.latestReading
        return self.gateway.data[self._data_key]

    @property
    def native_value(self) -> float:
        # return self.gateway.data.me.pool.latestReading
        return self.gateway.data[self._data_key]

    @property
    def data_valid(self):
        return True


class mySutroTimeStamp(mySutroEntity, SensorEntity):
    def __init__(self, coordinator, data_key):
        super().__init__(coordinator, data_key)
        self._attr_state_class = 'measurement'
        self._attr_device_class = 'timestamp'

    @property
    def name(self) -> str:
        return self._data_key

    @property
    def unique_id(self):
        return f"{super().unique_id}_{self._data_key}"

    @property
    def value(self) -> float:
        # return self.gateway.data.me.pool.latestReading
        # lastReadTime = dateutil.parser.parse(self.gateway.data[self._data_key])
        return dateutil.parser.parse(self.gateway.data[self._data_key])

    @property
    def native_value(self) -> float:
        # return self.gateway.data.me.pool.latestReading
        return dateutil.parser.parse(self.gateway.data[self._data_key])

    @property
    def data_valid(self):
        return True
