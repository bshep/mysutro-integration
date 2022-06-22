"""Constants for the mySutro integration."""

DOMAIN = "mysutro"

PROP_MAP = {
    'ph': {'min': 6.0, 'max': 8.4, 'step':0.01},
    'chlorine': {'min': 0.0, 'max': 12.0, 'step':0.1},
    'bromine': {'min': 0.0, 'max': 10.0, 'step':0.1},
    'alkalinity': {'min': 0.0, 'max': 300.0, 'step':0.1},
}