"""Constants for the mySutro integration."""

# Domain
DOMAIN = "mysutro"

# Update intervals and timeouts
DEFAULT_UPDATE_INTERVAL = 30  # seconds
MIN_UPDATE_INTERVAL = 5  # seconds
API_TIMEOUT = 5  # seconds

# User-facing strings
INTEGRATION_NAME = "mySutro Gateway"
INTEGRATION_TITLE = "mySutro Service"
ERROR_CANNOT_CONNECT = "Cannot connect to Sutro API. Please check your network and credentials."
ERROR_INVALID_AUTH = "Invalid username or password. Please try again."
ERROR_UNKNOWN = "Unknown error occurred. Please check logs."

# API endpoints
API_ENDPOINT = "https://api.mysutro.com/graphql"

# HTTP headers
USER_AGENT = "Sutro/348 CFNetwork/1333.0.4 Darwin/21.5.0"
CONTENT_TYPE = "application/json"

DOMAIN = "mysutro"

PROP_MAP = {
    'ph': {'min': 6.0, 'max': 8.4, 'step':0.01},
    'chlorine': {'min': 0.0, 'max': 12.0, 'step':0.1},
    'bromine': {'min': 0.0, 'max': 10.0, 'step':0.1},
    'alkalinity': {'min': 0.0, 'max': 300.0, 'step':0.1},
}
