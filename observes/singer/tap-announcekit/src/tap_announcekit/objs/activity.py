# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from tap_announcekit.objs.id_objs import (
    ActivityId,
    ExtUserId,
    FeedbackId,
    IndexedObj,
    PostId,
)
from typing import (
    Optional,
)


@dataclass(frozen=True)
class Activity:
    type: str
    created_at: datetime
    external_user_id: Optional[ExtUserId]
    post_id: Optional[PostId]
    feedback_id: Optional[FeedbackId]


ActivityObj = IndexedObj[ActivityId, Activity]
