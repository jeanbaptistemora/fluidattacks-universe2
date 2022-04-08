from ._getter import (
    get_month_contributions,
)
from ._report import (
    extract_active_users,
    filter_by_fa_hash,
    final_reports,
)
from code_etl.compute_bills.core import (
    ActiveUsersReport,
    FinalActiveUsersReport,
)
from code_etl.objs import (
    GroupId,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    FrozenDict,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
from fa_purity.frozen import (
    freeze,
)
from redshift_client.sql_client.core import (
    SqlClient,
)
from typing import (
    FrozenSet,
    Tuple,
)


def gen_final_reports(
    client: SqlClient,
    client_2: SqlClient,
    date: datetime,
    groups: FrozenSet[GroupId],
) -> Cmd[FrozenDict[GroupId, FinalActiveUsersReport]]:
    def process_group(
        group: GroupId,
    ) -> Cmd[Tuple[GroupId, ActiveUsersReport]]:
        return (
            get_month_contributions(client, group, date)
            .map(lambda x: filter_by_fa_hash(client_2, x, date.month))
            .bind(extract_active_users)
            .map(lambda u: (group, u))
        )

    reports = tuple(map(process_group, groups))
    return (
        serial_merge(reports).map(lambda x: freeze(dict(x))).map(final_reports)
    )
