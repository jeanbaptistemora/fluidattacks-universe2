from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
    Optional,
)


class EventComment(NamedTuple):
    event_id: str
    id: str
    parent_id: str
    creation_date: datetime
    content: str
    email: str
    full_name: Optional[str] = None
