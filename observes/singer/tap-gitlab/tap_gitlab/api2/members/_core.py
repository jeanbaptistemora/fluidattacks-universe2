from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Maybe,
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
    email: Maybe[str]
    name: str
    state: str
    created_at: datetime


UserObj = Tuple[UserId, User]


@dataclass(frozen=True)
class Member:
    user: UserObj
    membership_state: str
