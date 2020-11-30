import os

from __init__ import (
    FI_MIXPANEL_API_TOKEN
)


MIXPANEL_API_TOKEN = FI_MIXPANEL_API_TOKEN

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
NEW_RELIC_CONF_FILE = os.path.join(BASE_DIR, 'newrelic.ini')
