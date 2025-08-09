"""Config flow for mySutro integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
import requests

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("username"): str,
        vol.Required("password"): str,
    }
)

def get_token(username: str, password: str) -> str:
    """Perform the login mutation to retrieve a token from the Sutro API."""
    url = "https://api.mysutro.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Sutro/348 CFNetwork/1333.0.4 Darwin/21.5.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }
    payload = {
        "operationName": None,
        "variables": {
            "email": username,
            "password": password,
            "focusedInput": "",
            "loading": False
        },
        "query": "mutation ($email: String!, $password: String!) { login(email: $email, password: $password) { user { firstName lastName email phone releaseGroup __typename } token __typename } }"
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("data", {}).get("login", {}).get("token")
    if not token:
        raise InvalidAuth("No token returned from Sutro API")
    return token

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect and retrieve a token."""
    try:
        token = await hass.async_add_executor_job(get_token, data["username"], data["password"])
    except Exception as ex:
        _LOGGER.error("Failed to retrieve token: %s", ex)
        raise CannotConnect from ex
    return {"title": "mySutro Service", "token": token}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for House Audio Amplifier."""

    VERSION = 1


    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            # Save the username, password and token in the config entry
            entry_data = {
                "username": user_input["username"],
                "password": user_input["password"],
                "token": info["token"],
            }
            return self.async_create_entry(title=info["title"], data=entry_data)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    def is_matching(self, other_flow: Any) -> bool:
        return False

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
