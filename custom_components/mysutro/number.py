import logging

from homeassistant.components.number import NumberEntity
from homeassistant.helpers import entity_platform, config_validation as cv

from . import mySutroEntity
from .const import DOMAIN, PROP_MAP_INV, PROP_MAX

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up entry."""
    entities = []
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities.append(mySutroNumber(coordinator, 'pH'))

    async_add_entities(entities)


class mySutroNumber(mySutroEntity, NumberEntity):
    def __init__(self, coordinator, data_key):
        super().__init__(coordinator, data_key)
        self._attr_min_value = 0
        self._attr_max_value = 200
        self._attr_step = .1
        self.property_name = data_key

    @property
    def name(self) -> str:
        return self.property_name

    @property
    def unique_id(self):
        return f"{super().unique_id}_{self.property_name}"

    @property
    def value(self) -> float:
        # return self.gateway.data.me.pool.latestReading
        return 6.9

    @property
    def data_valid(self):
        return True
