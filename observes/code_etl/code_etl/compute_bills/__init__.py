from ._getter import (
    get_month_contributions,
    get_month_repos,
)
from ._keeper import (
    new_keeper,
)
from ._report import (
    extract_active_users,
    filter_by_fa_hash,
    final_reports,
)
from charset_normalizer import (
    logging,
)
from code_etl.compute_bills.core import (
    ActiveUsersReport,
    FinalActiveUsersReport,
)
from code_etl.objs import (
    GroupId,
)
from code_etl.utils import (
    DB_CREDS,
    DB_ID,
    log_info,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    FrozenDict,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
from fa_purity.frozen import (
    freeze,
)
from pathlib import (
    Path,
)
from redshift_client.sql_client.connection import (
    connect,
    IsolationLvl,
)
from redshift_client.sql_client.core import (
    new_client,
    SqlClient,
)
from typing import (
    FrozenSet,
    Tuple,
)

LOG = logging.getLogger(__name__)


def gen_final_reports(
    client: SqlClient,
    client_2: SqlClient,
    date: datetime,
    groups: FrozenSet[GroupId],
) -> Cmd[FrozenDict[GroupId, FinalActiveUsersReport]]:
    def process_group(
        group: GroupId,
    ) -> Cmd[Tuple[GroupId, ActiveUsersReport]]:
        start = log_info(LOG, "Generating report for group: %s", group.name)
        extract = log_info(LOG, "Calculating active users of: %s", group.name)
        end = log_info(LOG, "Report for %s done!", group.name)
        return start + (
            get_month_contributions(client, group, date)
            .map(lambda x: filter_by_fa_hash(client_2, x, date.month))
            .bind(lambda x: extract + Cmd.from_cmd(lambda: x))
            .bind(extract_active_users)
            .map(lambda u: (group, u))
            .bind(lambda x: end + Cmd.from_cmd(lambda: x))
        )

    reports = tuple(map(process_group, groups))
    start = log_info(LOG, "Generating final report...")
    return (
        serial_merge(reports)
        .map(lambda x: freeze(dict(x)))
        .bind(lambda x: start + Cmd.from_cmd(lambda: x))
        .map(final_reports)
    )


def save_all(
    token: str, folder: Path, data: FrozenDict[GroupId, FinalActiveUsersReport]
) -> Cmd[None]:
    def _action(grp: GroupId, report: FinalActiveUsersReport) -> None:
        with open(
            str(folder.joinpath(grp.name + ".csv")), "w", encoding="UTF-8"
        ) as file:
            unsafe_unwrap(new_keeper(file, token).save(grp, report))

    def _save(items: Tuple[GroupId, FinalActiveUsersReport]) -> Cmd[None]:
        return Cmd.from_cmd(lambda: _action(items[0], items[1]))

    start = log_info(LOG, "Saving reports...")
    end = log_info(LOG, "Saved!")
    return start + serial_merge(tuple(map(_save, data.items()))) + end


def main(token: str, folder: Path, date: datetime) -> Cmd[None]:
    connection = connect(DB_ID, DB_CREDS, True, IsolationLvl.AUTOCOMMIT)
    client_1 = connection.bind(
        lambda c: new_client(c, LOG.getChild("client_1"))
    )
    client_2 = connection.bind(
        lambda c: new_client(c, LOG.getChild("client_2"))
    )
    return client_1.bind(
        lambda c1: client_2.bind(
            lambda c2: get_month_repos(c1, date)
            .bind(
                lambda i: log_info(
                    LOG, "Contributing groups this month: %s", str(i)
                )
                + Cmd.from_cmd(lambda: i)
            )
            .bind(
                lambda groups: gen_final_reports(c1, c2, date, groups).bind(
                    lambda d: save_all(token, folder, d)
                )
            )
        )
    )
