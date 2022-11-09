# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.finding_comments.enums import (
    CommentType,
)
from typing import (
    NamedTuple,
    Optional,
)


class FindingComment(NamedTuple):
    comment_type: CommentType
    content: str
    creation_date: str
    email: str
    finding_id: str
    id: str
    parent_id: str
    full_name: Optional[str] = None


class FindingCommentsRequest(NamedTuple):
    comment_type: CommentType
    finding_id: str
