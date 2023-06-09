from enum import (
    Enum,
)


class SupportedStreams(Enum):
    COLLABORATORS = "COLLABORATORS"
    ERRORS = "ERRORS"
    EVENTS = "EVENTS"
    EVENT_FIELDS = "EVENT_FIELDS"
    ORGS = "ORGS"
    PIVOTS = "PIVOTS"
    PROJECTS = "PROJECTS"
    RELEASES = "RELEASES"
    STABILITY_TREND = "STABILITY_TREND"
