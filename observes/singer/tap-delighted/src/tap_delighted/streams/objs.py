from enum import (
    Enum,
)


class SupportedStreams(Enum):
    BOUNCED = "BOUNCED"
    METRICS = "METRICS"
    PEOPLE = "PEOPLE"
    SURVEY_RESPONSE = "SURVEY_RESPONSE"
    UNSUBSCRIBED = "UNSUBSCRIBED"
