# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
    Optional,
)

Item = dict[str, Any]


class HookEvent(str, Enum):
    DELETED_VULNERABILITY = "Vulnerability was deleted"
    EDITED_VULNERABILITY = "Vulnerability was edited"
    REPORTED_VULNERABILITY = "Vulnerability was reported"


class StreamEvent(str, Enum):
    INSERT = "INSERT"
    MODIFY = "MODIFY"
    REMOVE = "REMOVE"


class Record(NamedTuple):
    event_name: StreamEvent
    new_image: Optional[Item]
    old_image: Optional[Item]
    pk: str
    sequence_number: str
    sk: str


class Trigger(NamedTuple):
    records_filter: Callable[[Record], bool]
    records_processor: Callable[[tuple[Record, ...]], None]
