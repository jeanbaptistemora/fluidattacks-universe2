from typing import (
    NamedTuple,
)


class GroupComment(NamedTuple):
    group_name: str
    id: str
    parent_id: str
    creation_date: str
    full_name: str
    content: str
    email: str
