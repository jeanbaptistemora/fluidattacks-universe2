from code_etl.compute_bills._getter import (
    get_commit_first_seen_at,
)
from code_etl.compute_bills.core import (
    ActiveUsersReport,
    Contribution,
)
from code_etl.objs import (
    User,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.stream.transform import (
    filter_opt,
    squash,
)
from redshift_client.sql_client.core import (
    SqlClient,
)
from typing import (
    Dict,
    Optional,
)


def filter_by_fa_hash(
    client: SqlClient, data: Stream[Contribution], month: int
) -> Stream[Contribution]:
    def contrib_filter(item: Contribution) -> Cmd[Optional[Contribution]]:
        return get_commit_first_seen_at(
            client, item.commit_id.hash.fa_hash
        ).map(lambda d: item if d.month == month else None)

    return data.map(contrib_filter).transform(lambda s: filter_opt(squash(s)))


def _extract_active_users(
    catalog: Dict[User, Contribution], item: Contribution
) -> Dict[User, Contribution]:
    if catalog.get(item.author) is not None:
        catalog[item.author] = item
    return catalog


def extract_active_users(data: Stream[Contribution]) -> Cmd[ActiveUsersReport]:
    empty: Dict[User, Contribution] = {}
    return (
        data.reduce(_extract_active_users, empty)
        .map(lambda i: freeze(i))
        .map(ActiveUsersReport)
    )
