from functools import (
    lru_cache,
)
import json
import logging
from ratelimiter import (  # type: ignore[import]
    RateLimiter,
)
import requests
from typing import (
    cast,
    Optional,
)

LOG = logging.getLogger(__name__)


@lru_cache(maxsize=None)
@RateLimiter(max_calls=60, period=60)
def _get_group_org(token: str, group: str) -> Optional[str]:
    query = """
        query ObservesGetGroupOrganization($groupName: String!){
            group(groupName: $groupName){
                    organization
            }
        }
    """
    variables = {"groupName": group}
    json_data = {
        "query": query,
        "variables": variables,
    }
    result = requests.post(
        "https://app.fluidattacks.com/api",
        json=json_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = result.json()
    LOG.debug("Group: %s; \nResponse: %s", group, json.dumps(data, indent=4))
    if data["data"]["group"]:
        raw = data["data"]["group"]["organization"]
        return str(raw) if raw is not None else None
    return None


def get_org(token: str, group: str) -> Optional[str]:
    return cast(Optional[str], _get_group_org(token, group))
