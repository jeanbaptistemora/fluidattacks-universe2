from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from tap_gitlab.api2.ids import (
    UserId,
)
from typing import (
    Tuple,
)


@dataclass(frozen=True)
class User:
    username: str
    email: str
    name: str
    state: str
    created_at: datetime
    is_admin: bool


UserObj = Tuple[UserId, User]


@dataclass(frozen=True)
class Member:
    user: UserObj
    membership_state: str
