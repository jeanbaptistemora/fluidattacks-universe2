# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
    Optional,
)


class EventComment(NamedTuple):
    event_id: str
    id: str
    parent_id: str
    creation_date: str
    content: str
    email: str
    full_name: Optional[str] = None
