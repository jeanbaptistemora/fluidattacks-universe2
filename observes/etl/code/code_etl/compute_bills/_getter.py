from ._retry import (
    api_handler,
    retry_cmd,
)
from code_etl._utils import (
    COMMIT_HASH_SENTINEL,
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
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    JsonObj,
    JsonValue,
    Maybe,
    Result,
    ResultE,
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
from redshift_client.sql_client import (
    QueryValues,
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
    NoReturn,
    Optional,
)

LOG = logging.getLogger(__name__)


class UnexpectedResponse(Exception):
    pass


def _log_and_raise(log: Cmd[None], err: Exception) -> NoReturn:
    unsafe_unwrap(log)
    raise err


@dataclass(frozen=True)
class ApiError(Exception):
    errors: JsonValue

    def to_exception(self) -> Exception:
        return Exception(self)


def _from_raw_json(data: JsonObj) -> ResultE[str]:
    errors = (
        try_get(data, "errors")
        .alt(lambda _: None)
        .swap()
        .alt(lambda m: ApiError(m).to_exception())
    )
    group = errors.bind(
        lambda _: try_get(data, "data").bind(
            lambda x: Unfolder(x).get("group")
        )
    )
    return group.bind(
        lambda g: Unfolder(g)
        .uget("organization")
        .bind(lambda u: u.to_primitive(str).alt(Exception))
    )


@RateLimiter(max_calls=60, period=60)  # type: ignore[misc]
def _get_group_org(token: str, group: str) -> Cmd[ResultE[str]]:  # type: ignore[misc]
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
        headers: Dict[str, str] = {"Authorization": f"Bearer {token}"}
        result = requests.post(
            "https://app.fluidattacks.com/api",
            json=json_data,
            headers=headers,
        )
        result.raise_for_status()
        return result

    req = retry_cmd(
        api_handler(Cmd.from_cmd(_request)), 10, lambda i: (i + 1) ^ 2
    )
    result = req.map(
        lambda r: from_any(r.json()).alt(Exception)  # type: ignore[misc]
    ).map(lambda r: r.bind(_from_raw_json))
    return result.map(
        lambda r: r.alt(
            lambda e: _log_and_raise(
                Cmd.from_cmd(
                    lambda: LOG.error(
                        "Api call fail _get_group_org(%s) i.e. %s", group, e
                    )
                ),
                e,
            )
        )
    )


@lru_cache(maxsize=None)  # type: ignore[misc]
def _get_group_org_cached(token: str, group: str) -> Optional[str]:
    result: Optional[str] = unsafe_unwrap(
        _get_group_org(token, group)  # type: ignore[misc]
    )
    return result


def get_org(token: str, group: str) -> Optional[str]:
    return _get_group_org_cached(token, group)


def get_commit_first_seen_at(client: SqlClient, fa_hash: str) -> Cmd[datetime]:
    stm = """
        SELECT seen_at FROM code.commits
        WHERE fa_hash = %(fa_hash)s ORDER BY seen_at ASC LIMIT 1
    """
    return client.execute(
        new_query(stm), QueryValues(freeze({"fa_hash": fa_hash}))
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
    stm = """
        SELECT DISTINCT
            namespace
        FROM code.commits
        WHERE
            TO_CHAR(seen_at, 'YYYY-MM') = %(seen_at)s
        AND hash != %(sentinel)s
    """
    args: Dict[str, PrimitiveVal] = {
        "seen_at": date.strftime("%Y-%m"),
        "sentinel": COMMIT_HASH_SENTINEL,
    }

    def _to_group_id(row: RowData) -> GroupId:
        return GroupId(_assert_str(row.data[0]))

    return client.execute(
        new_query(stm),
        QueryValues(freeze(args)),
    ) + client.fetch_all().map(lambda d: frozenset(map(_to_group_id, d)))


def get_month_contributions(
    client: SqlClient, group: GroupId, date: datetime
) -> Cmd[Stream[Contribution]]:
    stm = """
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

    return client.execute(new_query(stm), QueryValues(freeze(args))).map(
        lambda _: client.data_stream(1000).map(to_contrib)
    )
