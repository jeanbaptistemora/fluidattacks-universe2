from tap_zoho_crm.api import (
    ApiClient,
)
from tap_zoho_crm.api.common import (
    PageIndex,
)
from tap_zoho_crm.api.users import (
    UsersDataPage,
    UserType,
)


def get_users(
    api_client: ApiClient, user_type: UserType, page: PageIndex
) -> UsersDataPage:
    return api_client.users.get_users(user_type, page)
