import logging
from ratelimiter import (
    RateLimiter,
)
import requests  # type: ignore
from singer_io.singer2.json import (
    JsonEmitter,
    JsonFactory,
)
from streamer_zoho_crm.api.common import (
    API_URL,
    DataPageInfo,
    PageIndex,
)
from streamer_zoho_crm.api.users.objs import (
    UsersDataPage,
    UserType,
)

API_ENDPOINT = API_URL + "/crm/v2/users"
LOG = logging.getLogger(__name__)
rate_limiter = RateLimiter(max_calls=10, period=60)
json_emitter = JsonEmitter()


def get_users(
    token: str, user_type: UserType, page_i: PageIndex
) -> UsersDataPage:
    LOG.info("API: Get users (%s)", user_type)
    endpoint = API_ENDPOINT
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    params = {
        "type": user_type.value,
        "page": page_i.page,
        "per_page": page_i.per_page,
    }
    response = requests.get(url=endpoint, headers=headers, params=params)
    response_json = JsonFactory.from_dict(response.json())
    users = [item.to_json() for item in response_json["users"].to_list()]
    LOG.debug(
        "response json: %s", json_emitter.to_str(response_json, indent=4)
    )
    response_info = response_json["info"].to_json()
    info = DataPageInfo(
        page=PageIndex(
            page=response_info["page"].to_primitive(int),
            per_page=response_info["per_page"].to_primitive(int),
        ),
        n_items=response_info["count"].to_primitive(int),
        more_records=response_info["more_records"].to_primitive(bool),
    )
    return UsersDataPage(data=users, info=info)
