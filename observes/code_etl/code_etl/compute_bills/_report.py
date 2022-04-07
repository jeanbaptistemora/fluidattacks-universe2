from code_etl.compute_bills._getter import (
    get_commit_first_seen_at,
)
from code_etl.compute_bills.core import (
    ActiveUsersReport,
    Contribution,
    FinalActiveUsersReport,
)
from code_etl.objs import (
    GroupId,
    User,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    Stream,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.stream.transform import (
    filter_opt,
    squash,
)
from functools import (
    reduce,
)
from redshift_client.sql_client.core import (
    SqlClient,
)
from typing import (
    Dict,
    FrozenSet,
    Optional,
    Set,
    Tuple,
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
    if catalog.get(item.author) is None:
        catalog[item.author] = item
    return catalog


def extract_active_users(data: Stream[Contribution]) -> Cmd[ActiveUsersReport]:
    empty: Dict[User, Contribution] = {}
    return (
        data.reduce(_extract_active_users, empty)
        .map(lambda i: freeze(i))
        .map(ActiveUsersReport)
    )


def _calc_user_groups(
    catalog: Dict[User, Set[GroupId]], item: Tuple[GroupId, ActiveUsersReport]
) -> Dict[User, Set[GroupId]]:
    for user in item[1].data:
        if catalog.get(user) is None:
            catalog[user] = set([item[0]])
        else:
            catalog[user].add(item[0])
    return catalog


def calc_user_groups(
    reports: FrozenDict[GroupId, ActiveUsersReport]
) -> FrozenDict[User, FrozenSet[GroupId]]:
    empty: Dict[User, Set[GroupId]] = {}
    user_groups = reduce(_calc_user_groups, reports.items(), empty)
    return freeze({k: frozenset(v) for k, v in user_groups.items()})


def calc_final_report(
    report: ActiveUsersReport,
    user_groups: FrozenDict[User, FrozenSet[GroupId]],
) -> FinalActiveUsersReport:
    draft = freeze({u: (c, user_groups[u]) for u, c in report.data.items()})
    return FinalActiveUsersReport(draft)


def final_reports(
    reports: FrozenDict[GroupId, ActiveUsersReport]
) -> FrozenDict[GroupId, FinalActiveUsersReport]:
    user_groups = calc_user_groups(reports)
    return freeze(
        {k: calc_final_report(v, user_groups) for k, v in reports.items()}
    )
