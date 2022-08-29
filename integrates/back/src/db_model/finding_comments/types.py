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
