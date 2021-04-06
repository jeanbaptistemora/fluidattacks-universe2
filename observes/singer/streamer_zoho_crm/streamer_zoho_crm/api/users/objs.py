# Standard libraries
from enum import Enum
from typing import (
    List,
    NamedTuple,
)
from streamer_zoho_crm.api.common import (
    DataPageInfo,
    JSON,
)
# Third party libraries
# Local libraries


class UserType(Enum):
    ANY = 'AllUsers'


class UsersDataPage(NamedTuple):
    data: List[JSON]
    info: DataPageInfo
