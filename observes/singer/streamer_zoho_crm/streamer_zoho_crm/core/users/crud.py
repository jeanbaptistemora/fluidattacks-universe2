# Standard libraries
# Third party libraries
# Local libraries
from streamer_zoho_crm.api import ApiClient
from streamer_zoho_crm.api.common import PageIndex
from streamer_zoho_crm.api.users import (
    UserType,
    UsersDataPage,
)


def get_users(
    api_client: ApiClient, user_type: UserType, page: PageIndex
) -> UsersDataPage:
    return api_client.users.get_users(user_type, page)
