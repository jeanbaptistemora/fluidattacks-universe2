from typing import (
    NamedTuple,
    Optional,
)


class GroupComment(NamedTuple):
    group_name: str
    id: str
    parent_id: str
    creation_date: str
    content: str
    email: str
    full_name: Optional[str] = None
