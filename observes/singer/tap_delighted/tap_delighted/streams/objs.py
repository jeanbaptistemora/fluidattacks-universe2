# Standard libraries
from enum import Enum

# Third party libraries
# Local libraries


class SupportedStreams(Enum):
    BOUNCED = 'BOUNCED'
    METRICS = 'METRICS'
    PEOPLE = 'PEOPLE'
    SURVEY_RESPONSE = 'SURVEY_RESPONSE'
    UNSUBSCRIBED = 'UNSUBSCRIBED'
