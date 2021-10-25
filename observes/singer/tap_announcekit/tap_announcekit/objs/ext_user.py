from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from typing import (
    Optional,
)

JsonStr = str


@dataclass(frozen=True)
class ExternalUser:
    # pylint: disable=too-many-instance-attributes
    created_at: datetime
    seen_at: datetime
    name: Optional[str]
    email: Optional[str]
    fields: JsonStr
    is_anon: bool
    is_following: bool
    is_email_verified: bool
    avatar: Optional[str]
    is_app: Optional[bool]
