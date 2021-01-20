# Standard libraries
import json
# Third party libraries
import requests
from ratelimiter import RateLimiter
# Local libraries
from streamer_zoho_crm import utils
from streamer_zoho_crm.api.common import (
    API_URL,
    DataPageInfo,
    PageIndex,
    UnexpectedResponse,
)
from streamer_zoho_crm.api.users._objs import (
    UsersDataPage,
    UserType
)


API_ENDPOINT = API_URL + '/crm/v2/users'
LOG = utils.get_log(__name__)
rate_limiter = RateLimiter(max_calls=10, period=60)


def get_users(
    token: str,
    user_type: UserType,
    page_i: PageIndex
) -> UsersDataPage:
    LOG.info('API: Get users (%s)', user_type)
    endpoint = API_ENDPOINT
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    params = {
        'type': user_type.value,
        'page': page_i.page,
        'per_page': page_i.per_page,
    }
    response = requests.get(url=endpoint, headers=headers, params=params)
    response_json = response.json()
    users = response_json['users']
    LOG.debug('response json: %s', json.dumps(response_json, indent=4))
    if not isinstance(users, list):
        raise UnexpectedResponse()
    info = DataPageInfo(
        page=PageIndex(
            page=response_json['info']['page'],
            per_page=response_json['info']['per_page']
        ),
        n_items=response_json['info']['count'],
        more_records=response_json['info']['more_records'],
    )
    return UsersDataPage(data=users, info=info)
