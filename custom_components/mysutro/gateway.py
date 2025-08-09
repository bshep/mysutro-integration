"""" Defines the gateway class for the sutro device """

from typing import Any
import logging
import requests


_LOGGER = logging.getLogger(__name__)



class MySutroGateway:
    """Gateway object to communicate with sutro service
    
    Args:
        token (str): the token to authenticate with the server
    """
    def __init__(self, token: str) -> None:
        self.token = token
        self.api_endpoint = "https://api.mysutro.com/graphql"
        self.sutro_state = ""

    def update(self) -> None:
        """Called when an update is requested by HASS
        """
        result_json = self.api_request()

        if result_json != "":
            self.sutro_state = result_json['data']['me']['pool']['latestReading']

    def api_request(self) -> dict[str, Any]:
        """Sends a request to the sutro API.  Currently just loads the status   .

        Returns:
            str: The result from the query as JSON
        """
        args = {}

        ret = None

        req_data = """{
            \"query\":\"query { 
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
                } 
            \"}"""

        req_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Sutro/348 CFNetwork/1333.0.4 Darwin/21.5.0",
            "Authorization": "Bearer " + self.token
        }

        ret = requests.post(
            self.api_endpoint, params=args, timeout=1, data=req_data, headers=req_headers
        )
        ret = ret.json()

        return ret

    @property
    def data(self) -> str:
        """ Returns the last data retrieved with the update method """
        return self.sutro_state

    @property
    def name(self) -> str:
        """ Returns the name of the integration """
        return "mySutro Gateway"
