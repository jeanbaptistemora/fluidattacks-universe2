from datetime import (
    datetime,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from typing import (
    NamedTuple,
)


class FindingComment(NamedTuple):
    comment_type: CommentType
    content: str
    creation_date: datetime
    email: str
    finding_id: str
    id: str
    parent_id: str
    full_name: str | None = None


class FindingCommentsRequest(NamedTuple):
    comment_type: CommentType
    finding_id: str
