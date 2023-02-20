from __future__ import (
    annotations,
)

from ._getter import (
    get_org,
)
from code_etl._patch import (
    Patch,
)
from code_etl.arm import (
    ArmClient,
)
from code_etl.compute_bills.core import (
    Contribution,
    FinalActiveUsersReport,
)
from code_etl.objs import (
    GroupId,
    OrgId,
    User,
)
from csv import (
    DictWriter,
    QUOTE_NONNUMERIC,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
import logging
from typing import (
    Callable,
    cast,
    Dict,
    FrozenSet,
    IO,
    Optional,
    Tuple,
)

LOG = logging.getLogger(__name__)


def _group_to_str(grp: GroupId) -> str:
    return grp.name


@dataclass(frozen=True)
class ReportRow:
    user: User
    contrib: Contribution
    groups: FrozenSet[GroupId]


@dataclass(frozen=True)  # type: ignore[misc]
class _ReportKeeper:
    writer: DictWriter  # type: ignore[type-arg]
    get_org: Patch[Callable[[GroupId], Optional[OrgId]]]


@dataclass(frozen=True)
class ReportKeeper:
    _inner: _ReportKeeper

    def _write_row(
        self,
        current: GroupId,
        row: ReportRow,
    ) -> Cmd[None]:
        if current not in row.groups:
            title = "A user in the final report does not belong to the group"
            raise Exception(f"{title}: {current.name}")
        org = self._inner.get_org.unwrap(current)

        def _group_filter(grp: GroupId) -> bool:
            return self._inner.get_org.unwrap(grp) == org

        groups_contributed = (
            frozenset(filter(_group_filter, row.groups)) if org else row.groups
        )
        data: Dict[str, str] = {
            "actor": row.user.name + " <" + row.user.email + ">",
            "groups": ", ".join(map(_group_to_str, groups_contributed)),
            "commit": row.contrib.commit_id.hash.hash,
            "repository": row.contrib.commit_id.repo.repository,
        }
        return Cmd.from_cmd(
            lambda: cast(None, self._inner.writer.writerow(data))  # type: ignore[misc]
        ).map(lambda _: None)

    def save(
        self,
        group: GroupId,
        report: FinalActiveUsersReport,
    ) -> Cmd[None]:
        def _write(
            item: Tuple[User, Tuple[Contribution, FrozenSet[GroupId]]]
        ) -> Cmd[None]:
            return self._write_row(
                group, ReportRow(item[0], item[1][0], item[1][1])
            )

        write_rows = tuple(map(_write, report.data.items()))
        return Cmd.from_cmd(
            lambda: cast(None, self._inner.writer.writeheader())  # type: ignore[misc]
        ) + serial_merge(write_rows).map(lambda _: None)

    @staticmethod
    def new(file: IO[str], client: ArmClient) -> ReportKeeper:
        file_columns = frozenset(["actor", "groups", "commit", "repository"])
        writer = DictWriter(
            file,
            sorted(list(file_columns)),
            quoting=QUOTE_NONNUMERIC,
        )

        def _get_org(grp: GroupId) -> Optional[OrgId]:
            org = (
                get_org(client, grp.name)
                .alt(
                    lambda e: LOG.error(
                        "Api call fail get_org(%s) i.e. %s", grp.name, e
                    )
                )
                .value_or(None)
            )
            return OrgId(org) if org is not None else None

        return ReportKeeper(_ReportKeeper(writer, Patch(_get_org)))
