"""Integration to read data from mySutro."""
from __future__ import annotations
from email import header
from typing import Sequence
from urllib.request import Request

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import DOMAIN

from datetime import timedelta
import logging
import asyncio

from .gateway import *

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up House Audio Amplifier from a config entry."""
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)
    hass.data[DOMAIN] = {}
    api_lock = asyncio.Lock()

    gateway = mySutroGateway(entry.data["token"])

    coordinator = mySutroDataUpdateCoordinator(
        hass,
        config_entry=entry,
        gateway=gateway,
        api_lock=api_lock,
    )

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "listener": entry.add_update_listener(async_update_listener),
    }

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    hass.data[DOMAIN].pop(entry.entry_id)

    return True


class mySutroDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, *, gateway, config_entry, api_lock):
        """Initialize the mySutro Data Update Coordinator."""
        self.config_entry = config_entry
        self.api_lock = api_lock
        self.gateway = gateway

        interval = timedelta(seconds=5)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=interval,
        )

    async def _async_update_data(self):
        """Fetch data from the Screenlogic gateway."""
        # try:
        async with self.api_lock:
            await self.hass.async_add_executor_job(self.gateway.update)
        # except Exception as error:
        #     _LOGGER.warning("mySutroError: %s", error)

        return self.gateway.data


class mySutroEntity(CoordinatorEntity):
    def __init__(self, coordinator, data_key):
        """Initialize of the entity."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._enabled_default = True

    def unload(self):
        return True

    @property
    def entity_registry_enabled_default(self):
        """Entity enabled by default."""
        return self._enabled_default

    @property
    def mac(self):
        """Mac address."""
        return self.coordinator.config_entry.entry_id

    @property
    def unique_id(self):
        """Entity Unique ID."""
        return f"{self.mac}_{self._data_key}"

    @property
    def config_data(self):
        """Shortcut for config data."""
        return self.coordinator.data["config"]

    @property
    def gateway(self) -> mySutroGateway:
        """Return the gateway."""
        return self.coordinator.gateway

    @property
    def gateway_name(self) -> str:
        """Return the configured name of the gateway."""
        return self.gateway.name

    @property
    def device_info(self):
        """Return device information for the controller."""
        return {
            "connections": {(dr.CONNECTION_NETWORK_MAC, self.mac)},
            "name": self.gateway_name,
            "manufacturer": "Sutro",
            "model": "0001",
        }


# curl -H 'Content-Type: application/json' -H 'User-Agent: Sutro/348 CFNetwork/1333.0.4 Darwin/21.5.0' -H --compressed -H 'Authorization: Bearer ***REMOVED***' -X POST https://api.mysutro.com/graphql -d '{"query":"\n      query {\n        me {\n          pool {\n            latestReading {\n              alkalinity\n              bromine\n              chlorine\n              ph\n              minAlkalinity\n              maxAlkalinity\n              readingTime\n              invalidatingTrends\n            }\n}\n        }\n      }\n    "}'


