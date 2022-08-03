from typing import (
    NamedTuple,
    Optional,
)


class EventComment(NamedTuple):
    event_id: str
    id: str
    parent_id: str
    comment_type: str
    creation_date: str
    content: str
    email: str
    full_name: Optional[str] = None
