from __future__ import (
    annotations,
)

from code_etl.client._assert import (
    assert_opt_type,
    assert_type,
)
from code_etl.objs import (
    CommitData,
    CommitDataId,
    CommitStamp,
    RepoRegistration,
)
from code_etl.str_utils import (
    truncate,
    TruncatedStr,
)
from code_etl.time_utils import (
    DatetimeUTC,
    to_utc,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.result import (
    Result,
    ResultE,
    UnwrapError,
)
from typing import (
    Any,
    cast,
    Dict,
    Literal,
    Optional,
    TypeVar,
    Union,
)


@dataclass(frozen=True)
class RawRow:
    # pylint: disable=too-many-instance-attributes
    author_name: Any
    author_email: Any
    authored_at: Any
    committer_email: Any
    committer_name: Any
    committed_at: Any
    message: Any
    summary: Any
    total_insertions: Any
    total_deletions: Any
    total_lines: Any
    total_files: Any
    namespace: Any
    repository: Any
    hash: Any
    fa_hash: Any
    seen_at: Any


@dataclass(frozen=True)
class CommitTableRow:
    # Represents commit table schema
    # pylint: disable=too-many-instance-attributes
    author_name: Optional[str]
    author_email: Optional[str]
    authored_at: Optional[DatetimeUTC]
    committer_name: Optional[str]
    committer_email: Optional[str]
    committed_at: Optional[DatetimeUTC]
    message: Optional[TruncatedStr[Literal[4096]]]
    summary: Optional[TruncatedStr[Literal[256]]]
    total_insertions: Optional[int]
    total_deletions: Optional[int]
    total_lines: Optional[int]
    total_files: Optional[int]
    namespace: str
    repository: str
    hash: str
    fa_hash: Optional[str]
    seen_at: DatetimeUTC


def from_objs(
    data: Optional[CommitData], commit_id: CommitDataId, seen_at: DatetimeUTC
) -> CommitTableRow:
    return CommitTableRow(
        data.author.name if data else None,
        data.author.email if data else None,
        data.authored_at if data else None,
        data.committer.name if data else None,
        data.committer.email if data else None,
        data.committed_at if data else None,
        data.message if data else None,
        data.summary if data else None,
        data.deltas.total_insertions if data else None,
        data.deltas.total_deletions if data else None,
        data.deltas.total_lines if data else None,
        data.deltas.total_files if data else None,
        commit_id.repo.namespace,
        commit_id.repo.repository,
        commit_id.hash.hash,
        commit_id.hash.fa_hash,
        seen_at,
    )


def from_raw(raw: RawRow) -> ResultE[CommitTableRow]:
    try:
        row = CommitTableRow(
            assert_opt_type(cast(str, raw.author_name), str).unwrap(),
            assert_opt_type(cast(str, raw.author_email), str).unwrap(),
            assert_opt_type(cast(datetime, raw.authored_at), datetime)
            .map(lambda d: to_utc(d) if d is not None else d)
            .unwrap(),
            assert_opt_type(cast(str, raw.committer_name), str).unwrap(),
            assert_opt_type(cast(str, raw.committer_email), str).unwrap(),
            assert_opt_type(cast(datetime, raw.committed_at), datetime)
            .map(lambda d: to_utc(d) if d is not None else d)
            .unwrap(),
            assert_opt_type(cast(str, raw.message), str)
            .map(lambda s: truncate(s, 4096) if s is not None else s)
            .unwrap(),
            assert_opt_type(cast(str, raw.summary), str)
            .map(lambda s: truncate(s, 256) if s is not None else s)
            .unwrap(),
            assert_opt_type(cast(int, raw.total_insertions), int).unwrap(),
            assert_opt_type(cast(int, raw.total_deletions), int).unwrap(),
            assert_opt_type(cast(int, raw.total_lines), int).unwrap(),
            assert_opt_type(cast(int, raw.total_files), int).unwrap(),
            assert_type(cast(str, raw.namespace), str).unwrap(),
            assert_type(cast(str, raw.repository), str).unwrap(),
            assert_type(cast(str, raw.hash), str).unwrap(),
            assert_opt_type(cast(str, raw.fa_hash), str).unwrap(),
            assert_type(cast(datetime, raw.seen_at), datetime)
            .map(to_utc)
            .unwrap(),
        )
        return Result.success(row)
    except UnwrapError[Any, Exception] as err:
        return Result.failure(err.container.unwrap_fail())


def from_stamp(stamp: CommitStamp) -> CommitTableRow:
    return from_objs(stamp.commit.data, stamp.commit.commit_id, stamp.seen_at)


def from_reg(reg: RepoRegistration) -> CommitTableRow:
    return from_objs(None, reg.commit_id, reg.seen_at)


def from_row_obj(item: Union[CommitStamp, RepoRegistration]) -> CommitTableRow:
    if isinstance(item, RepoRegistration):
        return from_reg(item)
    return from_stamp(item)


_T = TypeVar("_T")


def _from_opt(val: Optional[_T]) -> Maybe[_T]:
    return Maybe.from_optional(val)


def _encode_opt_datetime(date: Optional[DatetimeUTC]) -> Optional[str]:
    return _from_opt(date).map(lambda i: i.time.isoformat()).value_or(None)


def _encode_opt_int(num: Optional[int]) -> Optional[str]:
    return _from_opt(num).map(str).value_or(None)


def to_dict(row: CommitTableRow) -> Dict[str, Optional[str]]:
    return {
        "author_name": row.author_name,
        "author_email": row.author_email,
        "authored_at": _encode_opt_datetime(row.authored_at),
        "committer_email": row.committer_email,
        "committer_name": row.committer_name,
        "committed_at": _encode_opt_datetime(row.committed_at),
        "message": row.message.msg if row.message else None,
        "summary": row.summary.msg if row.summary else None,
        "total_insertions": _encode_opt_int(row.total_insertions),
        "total_deletions": _encode_opt_int(row.total_deletions),
        "total_lines": _encode_opt_int(row.total_lines),
        "total_files": _encode_opt_int(row.total_files),
        "namespace": row.namespace,
        "repository": row.repository,
        "hash": row.hash,
        "fa_hash": row.fa_hash,
        "seen_at": row.seen_at.time.isoformat(),
    }
