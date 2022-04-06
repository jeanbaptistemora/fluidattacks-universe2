from code_etl.compute_bills.contribution import (
    Contribution,
)
from code_etl.objs import (
    CommitDataId,
    CommitId,
    RepoId,
    User,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    Maybe,
    Result,
    Stream,
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
    RowData,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.sql_client.query import (
    new_query,
)
import requests
from typing import (
    cast,
    Dict,
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
    ) + client.fetch_one().map(
        lambda i: i.map(lambda x: x.data[0])
        .bind_optional(lambda i: i if isinstance(i, datetime) else None)
        .to_result()
        .alt(
            lambda _: Exception(
                f"Expected a datetime; got {str(i)} of type {type(i)}"
            )
        )
        .alt(raise_exception)
        .unwrap()
    )


def _assert_str(val: PrimitiveVal) -> str:
    return Maybe.from_optional(val if isinstance(val, str) else None).unwrap()


def get_month_contributions(
    client: SqlClient, repo: RepoId, date: datetime
) -> Cmd[Stream[Contribution]]:
    stm = f"""
        SELECT
            author_name,
            author_email,
            hash,
            fa_hash,
            namespace,
            repository
        FROM code.commits
        WHERE
            repository = %(repository)s
        AND namespace = %(namespace)s
        AND TO_CHAR(seen_at, 'YYYY-MM') = %(seen_at)s
        AND hash != {COMMIT_HASH_SENTINEL}
    """
    args: Dict[str, PrimitiveVal] = {
        "repository": repo.repository,
        "namespace": repo.namespace,
        "seen_at": date.strftime("%Y-%m"),
    }

    def to_contrib(raw: RowData) -> Contribution:
        return Contribution(
            User(_assert_str(raw.data[0]), _assert_str(raw.data[1])),
            CommitDataId(
                repo,
                CommitId(_assert_str(raw.data[2]), _assert_str(raw.data[3])),
            ),
        )

    return client.execute(new_query(stm), freeze(args)).map(
        lambda _: client.data_stream(1000).map(to_contrib)
    )
