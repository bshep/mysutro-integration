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

from .const import DOMAIN, API_ENDPOINT, USER_AGENT, CONTENT_TYPE, INTEGRATION_TITLE, ERROR_CANNOT_CONNECT, ERROR_INVALID_AUTH, ERROR_UNKNOWN, DEFAULT_UPDATE_INTERVAL, MIN_UPDATE_INTERVAL
class MySutroOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            # Validate credentials and update entry
            try:
                hass = self.hass
                info = await validate_input(hass, user_input)
            except CannotConnect:
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._get_schema(user_input),
                    errors={"base": ERROR_CANNOT_CONNECT},
                )
            except InvalidAuth:
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._get_schema(user_input),
                    errors={"base": ERROR_INVALID_AUTH},
                )
            except Exception:
                _LOGGER.exception("Unexpected exception in options flow")
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._get_schema(user_input),
                    errors={"base": ERROR_UNKNOWN},
                )
            # Save new credentials, token, and update interval
            data = dict(self.config_entry.data)
            data.update({
                "username": user_input["username"],
                "password": user_input["password"],
                "token": info["token"],
            })
            options = dict(self.config_entry.options)
            options["update_interval"] = user_input["update_interval"]
            return self.async_create_entry(title="", data=options)

        # Show form with current values as defaults
        defaults = self.config_entry.data
        options = self.config_entry.options
        schema = self._get_schema({
            "username": defaults.get("username", ""),
            "password": defaults.get("password", ""),
            "update_interval": options.get("update_interval", DEFAULT_UPDATE_INTERVAL),
        })
        return self.async_show_form(step_id="init", data_schema=schema)

    def _get_schema(self, user_input):
        return vol.Schema({
            vol.Required("username", default=user_input.get("username", "")): str,
            vol.Required("password", default=user_input.get("password", "")): str,
            vol.Required("update_interval", default=user_input.get("update_interval", DEFAULT_UPDATE_INTERVAL)): vol.All(int, vol.Range(min=MIN_UPDATE_INTERVAL, max=3600)),
        })

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("username"): str,
        vol.Required("password"): str,
    }
)

def get_token(username: str, password: str) -> str:
    """Perform the login mutation to retrieve a token from the Sutro API."""
    url = API_ENDPOINT
    headers = {
        "Content-Type": CONTENT_TYPE,
        "User-Agent": USER_AGENT,
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

    try:
        _LOGGER.debug("Sending login request to Sutro API")
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        _LOGGER.debug("Login request successful, parsing response")
        data = resp.json()
        token = data.get("data", {}).get("login", {}).get("token")
    except requests.RequestException as ex:
        _LOGGER.error("Failed to connect to Sutro API: %s", ex)
        raise CannotConnect from ex
    except ValueError as ex:
        _LOGGER.error("Failed to parse response from Sutro API: %s", ex)
        raise InvalidAuth("Invalid response from Sutro API") from ex
    except KeyError as ex:
        _LOGGER.error("Unexpected response structure from Sutro API: %s", ex)
        raise InvalidAuth("Unexpected response structure from Sutro API") from ex
    except Exception as ex:
        _LOGGER.exception("Unexpected error while retrieving token: %s", ex)
        raise InvalidAuth("Unexpected error while retrieving token") from ex

    if not token:
        raise InvalidAuth("No token returned from Sutro API")
    return token

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect and retrieve a token."""
    try:
        _LOGGER.debug("Attempting to retrieve token for user: %s", data["username"])
        token = await hass.async_add_executor_job(get_token, data["username"], data["password"])
    except Exception as ex:
        _LOGGER.error("Failed to retrieve token: %s", ex)
        raise CannotConnect from ex
    return {"title": INTEGRATION_TITLE, "token": token}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    @staticmethod
    def async_get_options_flow(config_entry):
        return MySutroOptionsFlowHandler(config_entry)
    """Handle a config flow for MySutro Integration."""

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
            errors["base"] = ERROR_CANNOT_CONNECT
        except InvalidAuth:
            errors["base"] = ERROR_INVALID_AUTH
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = ERROR_UNKNOWN
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
