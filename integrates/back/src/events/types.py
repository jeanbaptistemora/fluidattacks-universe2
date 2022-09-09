# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.events.enums import (
    EventSolutionReason,
    EventType,
)
from typing import (
    NamedTuple,
    Optional,
)


class EventAttributesToUpdate(NamedTuple):
    event_type: Optional[EventType] = None
    other_solving_reason: Optional[str] = None
    solving_reason: Optional[EventSolutionReason] = None
