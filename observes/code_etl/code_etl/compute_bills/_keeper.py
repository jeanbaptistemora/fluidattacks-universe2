from ._getter import (
    get_org,
)
from code_etl._patch import (
    Patch,
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


@dataclass(frozen=True)
class _ReportKeeper:
    _writer: DictWriter[str]
    _get_org: Patch[Callable[[GroupId], Optional[OrgId]]]


@dataclass(frozen=True)
class ReportKeeper(_ReportKeeper):
    def __init__(self, obj: _ReportKeeper) -> None:
        super().__init__(**obj.__dict__)  # type: ignore[misc]

    def _write_row(
        self,
        current: GroupId,
        row: ReportRow,
    ) -> Cmd[None]:
        if current not in row.groups:
            raise Exception(
                f"A user in the final report does not belong to the group: {current.name}"
            )
        org = self._get_org.unwrap(current)

        def _group_filter(grp: GroupId) -> bool:
            return self._get_org.unwrap(grp) == org

        if org:
            groups_contributed = frozenset(filter(_group_filter, row.groups))
            data: Dict[str, str] = {
                "actor": row.user.name + " <" + row.user.email + ">",
                "groups": ", ".join(map(_group_to_str, groups_contributed)),
                "commit": row.contrib.commit_id.hash.hash,
                "repository": row.contrib.commit_id.repo.repository,
            }
            return Cmd.from_cmd(
                lambda: cast(None, self._writer.writerow(data))
            ).map(lambda _: None)
        return Cmd.from_cmd(
            lambda: LOG.warning("Skipped group contribution: %s", current.name)
        )

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
            lambda: cast(None, self._writer.writeheader())
        ) + serial_merge(write_rows).map(lambda _: None)


def new_keeper(file: IO[str], token: str) -> ReportKeeper:
    file_columns = frozenset(["actor", "groups", "commit", "repository"])
    writer = DictWriter(
        file,
        file_columns,
        quoting=QUOTE_NONNUMERIC,
    )

    def _get_org(grp: GroupId) -> Optional[OrgId]:
        org = get_org(token, grp.name)
        return OrgId(org) if org is not None else None

    draft = _ReportKeeper(writer, Patch(_get_org))
    return ReportKeeper(draft)
