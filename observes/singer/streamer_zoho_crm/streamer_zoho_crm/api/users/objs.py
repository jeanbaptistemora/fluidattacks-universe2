from enum import (
    Enum,
)
from streamer_zoho_crm.api.common import (
    DataPageInfo,
    JSON,
)
from typing import (
    List,
    NamedTuple,
)


class UserType(Enum):
    ANY = "AllUsers"


class UsersDataPage(NamedTuple):
    data: List[JSON]
    info: DataPageInfo
