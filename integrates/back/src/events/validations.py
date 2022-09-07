# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    InvalidParameter,
)
from db_model.events.enums import (
    EventType,
)


def validate_type(event_type: EventType) -> None:
    if event_type in {
        EventType.CLIENT_CANCELS_PROJECT_MILESTONE,
        EventType.INCORRECT_MISSING_SUPPLIES,
    }:
        raise InvalidParameter("eventType")
