from enum import (
    Enum,
)
from singer_io.singer2.json import (
    JsonObj,
)
from streamer_zoho_crm.api.common import (
    DataPageInfo,
)
from typing import (
    List,
    NamedTuple,
)


class UserType(Enum):
    ANY = "AllUsers"


class UsersDataPage(NamedTuple):
    data: List[JsonObj]
    info: DataPageInfo
