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
from streamer_zoho_crm.core import users, bulk
from streamer_zoho_crm.db import Client as DbClient


class IBulk(NamedTuple):
    create: Callable[[ModuleName, int], None]
    update_all: Callable[[], None]
    get_all: Callable[[], FrozenSet[BulkJob]]
    extract_data: Callable[[FrozenSet[str]], FrozenSet[BulkData]]


class IUsers(NamedTuple):
    get_users: Callable[[UserType, PageIndex], UsersDataPage]


class CoreClient(NamedTuple):
    users: IUsers
    bulk: IBulk


def new_client(api_client: ApiClient, db_client: DbClient) -> CoreClient:
    def create_bulk(module: ModuleName, page: int) -> None:
        bulk.create_bulk_job(api_client, db_client, module, page)

    def update_bulks() -> None:
        bulk.update_all(api_client, db_client)

    def extract(jobs_id: FrozenSet[str]) -> FrozenSet[BulkData]:
        return bulk.get_bulk_data(api_client, jobs_id)

    def get_users(user_type: UserType, page: PageIndex) -> UsersDataPage:
        return users.get_users(api_client, user_type, page)

    return CoreClient(
        users=IUsers(
            get_users=get_users
        ),
        bulk=IBulk(
            create=create_bulk,
            update_all=update_bulks,
            get_all=db_client.get_bulk_jobs,
            extract_data=extract
        )
    )
