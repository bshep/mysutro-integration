import logging
from xmlrpc.client import Boolean

from homeassistant.components.number import NumberEntity
from homeassistant.helpers import entity_platform, config_validation as cv

from . import mySutroEntity
from .const import DOMAIN, PROP_MAP

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up entry."""
    entities = []
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities.append(mySutroNumber(coordinator, 'ph'))

    async_add_entities(entities)


class mySutroNumber(mySutroEntity, NumberEntity):
    def __init__(self, coordinator, data_key):
        super().__init__(coordinator, data_key)
        self.native_min_value = PROP_MAP[data_key]['min']
        self.native_max_value = PROP_MAP[data_key]['max']
        self.native_step = PROP_MAP[data_key]['step']

    @property
    def name(self) -> str:
        return self.property_name

    @property
    def unique_id(self):
        return f"{super().unique_id}_{self._data_key}"

    @property
    def native_value(self) -> float:
        # return self.gateway.data.me.pool.latestReading
        return self.gateway.data[self._data_key]

    @property
    def data_valid(self):
        return True
