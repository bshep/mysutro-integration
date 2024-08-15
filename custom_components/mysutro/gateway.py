"""" Defines the gateway class for the sutro device """

import logging
import requests


_LOGGER = logging.getLogger(__name__)


class mySutroGateway:
    """Gateway object to communicate with sutro service
    
    Args:
        token (str): the token to authenticate with the server
    """
    def __init__(self, token) -> None:
        self.token = token
        self.api_endpoint = "https://api.mysutro.com/graphql"
        self.sutroState = ""

    def update(self):
        """Called when an update is requested by HASS
        """
        result_json = self.api_request()

        if result_json != "":
            self.sutroState = result_json['data']['me']['pool']['latestReading']

    def api_request(self) -> str:
        """Sends a request to the sutro API.  Currently just loads the status   .

        Returns:
            str: The result from the query as JSON
        """
        # _LOGGER.warning('mySutroGateway 0')

        args = {}

        ret = None

        # try:
        req_data = """{\"query\":\"query { me { pool { latestReading { alkalinity bromine chlorine ph minAlkalinity maxAlkalinity readingTime invalidatingTrends } } } } \"}"""

        # _LOGGER.warning('mySutroGateway 1')

        req_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Sutro/348 CFNetwork/1333.0.4 Darwin/21.5.0",
            # "Connection": "keep-alive",
            # "Accept": "*/*",
            # "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "Bearer " + self.token
        }

        # _LOGGER.warning('mySutroGateway 2')
        # req = Request('POST', self.api_endpoint, data=req_data, headers=req_headers)

        ret = requests.post(
            self.api_endpoint, params=args, timeout=1, data=req_data, headers=req_headers
        )
        # _LOGGER.warning('mySutroGateway 3  %s ',ret.text)
        ret = ret.json()
        # _LOGGER.warning('mySutroGateway - Data %s', ret)
        # except Exception as ex:
        #     _LOGGER.error("mySutroGateway - api_request: %s", ex)
        #     ret = ""

        return ret

    @property
    def data(self):
        """ Returns the last data retrieved with the update method """
        return self.sutroState

    @property
    def name(self):
        """ Returns the name of the integration """
        return "mySutro Gateway"
