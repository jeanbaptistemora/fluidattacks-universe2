# Standard libraries
from typing import (
    Callable,
    FrozenSet,
    NamedTuple,
)
# Third party libraries
# Local libraries
from streamer_zoho_crm.api import (
    ApiClient,
)
from streamer_zoho_crm.api.bulk import (
    BulkData,
    BulkJob,
    ModuleName,
)
from streamer_zoho_crm.api.common import PageIndex
from streamer_zoho_crm.api.users import (
    UserType,
    UsersDataPage,
)
from streamer_zoho_crm.core import users


class IBulk(NamedTuple):
    create: Callable[[ModuleName, int], None]
    update_all: Callable[[], None]
    get_all: Callable[[], FrozenSet[BulkJob]]
    extract_data: Callable[[FrozenSet[str]], FrozenSet[BulkData]]


class IUsers(NamedTuple):
    get_users: Callable[[UserType, PageIndex], UsersDataPage]


class CoreClient(NamedTuple):
    users: IUsers


def new_client(api_client: ApiClient) -> CoreClient:
    def get_users(user_type: UserType, page: PageIndex) -> UsersDataPage:
        return users.get_users(api_client, user_type, page)

    return CoreClient(
        users=IUsers(
            get_users=get_users
        )
    )
