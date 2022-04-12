from ._retry import (
    api_handler,
    retry_cmd,
)
from code_etl.compute_bills.core import (
    Contribution,
)
from code_etl.objs import (
    CommitDataId,
    CommitId,
    GroupId,
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
    JsonObj,
    Maybe,
    Stream,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.factory import (
    from_any,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.result.factory import (
    try_get,
)
from fa_purity.union import (
    inl,
)
from fa_purity.utils import (
    raise_exception,
)
from functools import (
    lru_cache,
)
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
    Dict,
    FrozenSet,
    Optional,
)

LOG = logging.getLogger(__name__)


class UnexpectedResponse(Exception):
    pass


class ApiError(Exception):
    pass


def _from_raw_json(data: JsonObj) -> Optional[str]:
    errors = (
        try_get(data, "errors")
        .alt(lambda _: None)
        .swap()
        .alt(lambda m: ApiError(m))
        .alt(Exception)
    )
    group = errors.bind(
        lambda _: try_get(data, "data").bind(
            lambda x: Unfolder(x).get("group")
        )
    )
    LOG.debug(data)
    return (
        group.map(
            lambda g: Maybe.from_result(
                Unfolder(g).get("organization").alt(lambda _: None)
            )
            .map(
                lambda o: Unfolder(o)
                .to_primitive(str)
                .map(lambda x: inl(x, type(None)))
                .lash(
                    lambda e: Unfolder(o).to_none().map(lambda x: inl(x, str))
                )
                .alt(raise_exception)
                .unwrap()
            )
            .to_result()
            .to_union()
        )
        .alt(raise_exception)
        .unwrap()
    )


@RateLimiter(max_calls=60, period=60)
def _get_group_org(token: str, group: str) -> Cmd[Optional[str]]:
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

    def _request() -> requests.Response:
        result = requests.post(
            "https://app.fluidattacks.com/api",
            json=json_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        result.raise_for_status()
        return result

    req = retry_cmd(
        api_handler(Cmd.from_cmd(_request)), 10, lambda i: (i + 1) ^ 2
    )
    return req.map(lambda r: from_any(r.json()).unwrap()).map(_from_raw_json)


@lru_cache(maxsize=None)
def _get_group_org_cached(token: str, group: str) -> Optional[str]:
    result: Optional[str] = unsafe_unwrap(_get_group_org(token, group))
    return result


def get_org(token: str, group: str) -> Optional[str]:
    return _get_group_org_cached(token, group)


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


def get_month_repos(
    client: SqlClient, date: datetime
) -> Cmd[FrozenSet[GroupId]]:
    stm = f"""
        SELECT DISTINCT
            namespace
        FROM code.commits
        WHERE
            TO_CHAR(seen_at, 'YYYY-MM') = %(seen_at)s
        AND hash != %(sentinel)s
    """
    return client.execute(
        new_query(stm),
        freeze(
            {
                "seen_at": date.strftime("%Y-%m"),
                "sentinel": COMMIT_HASH_SENTINEL,
            }
        ),
    ) + client.fetch_all().map(
        lambda l: frozenset(
            map(
                lambda r: GroupId(_assert_str(r.data[0])),
                l,
            )
        )
    )


def get_month_contributions(
    client: SqlClient, group: GroupId, date: datetime
) -> Cmd[Stream[Contribution]]:
    stm = f"""
        SELECT
            author_name,
            author_email,
            repository,
            hash,
            fa_hash
        FROM code.commits
        WHERE
            namespace = %(namespace)s
        AND TO_CHAR(seen_at, 'YYYY-MM') = %(seen_at)s
        AND hash != %(sentinel)s
    """
    args: Dict[str, PrimitiveVal] = {
        "namespace": group.name,
        "seen_at": date.strftime("%Y-%m"),
        "sentinel": COMMIT_HASH_SENTINEL,
    }

    def to_contrib(raw: RowData) -> Contribution:
        return Contribution(
            User(_assert_str(raw.data[0]), _assert_str(raw.data[1])),
            CommitDataId(
                RepoId(group.name, _assert_str(raw.data[2])),
                CommitId(_assert_str(raw.data[3]), _assert_str(raw.data[4])),
            ),
        )

    return client.execute(new_query(stm), freeze(args)).map(
        lambda _: client.data_stream(1000).map(to_contrib)
    )
