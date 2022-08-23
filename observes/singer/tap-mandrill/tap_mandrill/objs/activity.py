from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)


@dataclass(frozen=True)
class Activity:
    date: datetime
    email: str
    sender: str
    subject: str
    status: str
    tags: str
    subaccount: str
    opens: int
    clicks: int
    bounce: str
    detail: str
