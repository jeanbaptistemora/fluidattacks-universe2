from code_etl._utils import (
    COMMIT_HASH_SENTINEL,
)
from code_etl.arm import (
    ApiError,
    ArmClient,
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
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    Maybe,
    Result,
    Stream,
)
from fa_purity.cmd import (
    unsafe_unwrap,
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
from typing import (
    Dict,
    FrozenSet,
)


class UnexpectedResponse(Exception):
    pass


@RateLimiter(max_calls=60, period=60)  # type: ignore[misc]
def _get_group_org(client: ArmClient, group: str) -> Cmd[Result[str, ApiError]]:  # type: ignore[misc]
    return client.get_org(group)


@lru_cache(maxsize=None)  # type: ignore[misc]
def _get_group_org_cached(
    client: ArmClient, group: str
) -> Result[str, ApiError]:
    result: Result[str, ApiError] = unsafe_unwrap(
        _get_group_org(client, group)  # type: ignore[misc]
    )
    return result


def get_org(client: ArmClient, group: str) -> Result[str, ApiError]:
    return _get_group_org_cached(client, group)


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
