import os

from backend_new import settings

from __init__ import (
    FI_MIXPANEL_API_TOKEN
)


MIXPANEL_API_TOKEN = FI_MIXPANEL_API_TOKEN

NEW_RELIC_CONF_FILE = os.path.join(settings.BASE_DIR, 'newrelic.ini')
