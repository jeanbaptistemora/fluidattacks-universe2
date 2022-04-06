from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.utils import (
    raise_exception,
)
from functools import (
    lru_cache,
)
import json
import logging
from ratelimiter import (  # type: ignore[import]
    RateLimiter,
)
from redshift_client.sql_client.core import (
    SqlClient,
)
from redshift_client.sql_client.query import (
    new_query,
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


def get_commit_first_seen_at(client: SqlClient, fa_hash: str) -> Cmd[datetime]:
    stm = """
        SELECT seen_at FROM code.commits
        WHERE fa_hash = %(fa_hash)s ORDER BY seen_at ASC LIMIT 1
    """
    return client.execute(
        new_query(stm), freeze({"fa_hash": fa_hash})
    ) + client.fetch_one().map(lambda i: i[0] if i else None).map(
        lambda i: datetime.fromisoformat(i)
        if isinstance(i, str)
        else raise_exception(
            Exception(f"Expected a datetime; got {str(i)} of type {type(i)}")
        )
    )
