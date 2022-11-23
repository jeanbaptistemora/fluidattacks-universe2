from tap_zoho_crm import (
    auth,
)
from tap_zoho_crm.api import (
    bulk,
    users,
)
from tap_zoho_crm.api.bulk import (
    BulkData,
    BulkJob,
    ModuleName,
)
from tap_zoho_crm.api.common import (
    PageIndex,
)
from tap_zoho_crm.api.users import (
    UsersDataPage,
    UserType,
)
from tap_zoho_crm.auth import (
    Credentials,
)
from typing import (
    Callable,
    NamedTuple,
)


class BulkApi(NamedTuple):
    create_bulk_read_job: Callable[[ModuleName, int], BulkJob]
    get_bulk_job: Callable[[str], BulkJob]
    download_result: Callable[[str], BulkData]


class UsersApi(NamedTuple):
    get_users: Callable[[UserType, PageIndex], UsersDataPage]


class ApiClient(NamedTuple):
    bulk: BulkApi
    users: UsersApi


def new_client(credentials: Credentials) -> ApiClient:
    result = auth.generate_token(credentials)
    token = result["access_token"]

    def create_job(module: ModuleName, page: int) -> BulkJob:
        return bulk.create_bulk_read_job(token, module, page)

    def get_job(job_id: str) -> BulkJob:
        return bulk.get_bulk_job(token, job_id)

    def download_job(job_id: str) -> BulkData:
        return bulk.download_result(token, job_id)

    def get_users(u_type: UserType, page_i: PageIndex) -> UsersDataPage:
        return users.get_users(token, u_type, page_i)

    return ApiClient(
        bulk=BulkApi(
            create_bulk_read_job=create_job,
            get_bulk_job=get_job,
            download_result=download_job,
        ),
        users=UsersApi(get_users=get_users),
    )
