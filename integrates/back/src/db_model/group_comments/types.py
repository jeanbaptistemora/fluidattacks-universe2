from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class GroupComment(NamedTuple):
    group_name: str
    id: str
    parent_id: str
    creation_date: datetime
    content: str
    email: str
    full_name: str | None = None
