# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
