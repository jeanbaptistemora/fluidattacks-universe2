from db_model.finding_comments.enums import (
    CommentType,
)
from typing import (
    NamedTuple,
    Optional,
)


class FindingComment(NamedTuple):
    finding_id: str
    id: str
    parent_id: str
    comment_type: CommentType
    creation_date: str
    content: str
    email: str
    full_name: Optional[str] = None
