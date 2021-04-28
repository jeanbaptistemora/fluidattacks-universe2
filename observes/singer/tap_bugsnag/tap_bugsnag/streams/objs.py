# Standard libraries
from enum import Enum


class SupportedStreams(Enum):
    COLLABORATORS = "COLLABORATORS"
    ERRORS = "ERRORS"
    EVENTS = "EVENTS"
    ORGS = "ORGS"
    PIVOTS = "PIVOTS"
    PROJECTS = "PROJECTS"
    RELEASES = "RELEASES"
    RELEASE_GROUPS = "RELEASE_GROUPS"
    STABILITY_TREND = "STABILITY_TREND"
