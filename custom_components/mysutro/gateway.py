"""" Defines the gateway class for the sutro device """


from typing import Any
import logging
import requests
from .const import API_ENDPOINT, USER_AGENT, CONTENT_TYPE, INTEGRATION_NAME, API_TIMEOUT


_LOGGER = logging.getLogger(__name__)



class MySutroGateway:
    """Gateway object to communicate with sutro service
    
    Args:
        token (str): the token to authenticate with the server
    """
    def __init__(self, token: str) -> None:
        self.token = token
        self.api_endpoint = API_ENDPOINT
        self.sutro_state = ""
        _LOGGER.debug("Initialized MySutroGateway with token: %s", token[:6] + "..." if token else None)

    def update(self) -> None:
        """Called when an update is requested by HASS
        """
        _LOGGER.debug("Calling update on MySutroGateway")
        result_json = self.api_request()
        _LOGGER.debug("API request result: %s", result_json)
        if result_json != "":
            try:
                self.sutro_state = result_json['data']['me']['pool']['latestReading']
                _LOGGER.debug("Updated sutro_state: %s", self.sutro_state)
            except Exception as e:
                _LOGGER.error("Failed to update sutro_state: %s", e)

    def api_request(self) -> dict[str, Any]:
        """Sends a request to the sutro API.  Currently just loads the status   .

        Returns:
            str: The result from the query as JSON
        """
        args = {}
        req_data = """
        {
            "query": "query { 
                me { 
                    pool { 
                        latestReading { 
                            alkalinity 
                            bromine 
                            chlorine 
                            ph 
                            minAlkalinity 
                            maxAlkalinity 
                            readingTime 
                            invalidatingTrends 
                        } 
                    } 
                } 
            }"
        }
        """.replace("\n", "").replace("  ", "")
        req_headers = {
            "Content-Type": CONTENT_TYPE,
            "User-Agent": USER_AGENT,
            "Authorization": "Bearer " + self.token
        }
        _LOGGER.debug("Sending POST to %s with headers: %s and data: %s",
                        self.api_endpoint,
                        req_headers,
                        req_data)
        try:
            ret = requests.post(
                self.api_endpoint,
                params=args,
                timeout=API_TIMEOUT,
                data=req_data,
                headers=req_headers
            )
            ret.raise_for_status()
            ret_json = ret.json()
            _LOGGER.debug("Received response: %s", ret_json)
            return ret_json
        except Exception as e:
            _LOGGER.error("API request failed: %s", e)
            return {}

    @property
    def data(self) -> str:
        """ Returns the last data retrieved with the update method """
        _LOGGER.debug("Accessing sutro_state: %s", self.sutro_state)
        return self.sutro_state

    @property
    def name(self) -> str:
        """ Returns the name of the integration """
        return INTEGRATION_NAME
