# pylint: skip-file

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
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from returns.functions import (
    raise_exception,
)
from returns.maybe import (
    Maybe,
)
from returns.result import (
    Failure,
    ResultE,
    Success,
)
from typing import (
    Any,
    Dict,
    Optional,
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
    authored_at: Optional[datetime]
    committer_email: Optional[str]
    committer_name: Optional[str]
    committed_at: Optional[datetime]
    message: Optional[str]
    summary: Optional[str]
    total_insertions: Optional[int]
    total_deletions: Optional[int]
    total_lines: Optional[int]
    total_files: Optional[int]
    namespace: str
    repository: str
    hash: str
    fa_hash: Optional[str]
    seen_at: datetime


def from_objs(
    data: Optional[CommitData], commit_id: CommitDataId, seen_at: datetime
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
        commit_id.namespace,
        commit_id.repository,
        commit_id.hash.hash,
        commit_id.hash.fa_hash,
        seen_at,
    )


def from_raw(raw: RawRow) -> ResultE[CommitTableRow]:
    try:
        row = CommitTableRow(
            assert_opt_type(raw.author_name, str)
            .alt(raise_exception)
            .unwrap(),
            assert_opt_type(raw.author_email, str)
            .alt(raise_exception)
            .unwrap(),
            assert_opt_type(raw.authored_at, datetime)
            .alt(raise_exception)
            .unwrap(),
            assert_opt_type(raw.committer_email, str)
            .alt(raise_exception)
            .unwrap(),
            assert_opt_type(raw.committer_name, str)
            .alt(raise_exception)
            .unwrap(),
            assert_opt_type(raw.committed_at, datetime)
            .alt(raise_exception)
            .unwrap(),
            assert_opt_type(raw.message, str).alt(raise_exception).unwrap(),
            assert_opt_type(raw.summary, str).alt(raise_exception).unwrap(),
            assert_opt_type(raw.total_insertions, int)
            .alt(raise_exception)
            .unwrap(),
            assert_opt_type(raw.total_deletions, int)
            .alt(raise_exception)
            .unwrap(),
            assert_opt_type(raw.total_lines, int)
            .alt(raise_exception)
            .unwrap(),
            assert_opt_type(raw.total_files, int)
            .alt(raise_exception)
            .unwrap(),
            assert_type(raw.namespace, str).alt(raise_exception).unwrap(),
            assert_type(raw.repository, str).alt(raise_exception).unwrap(),
            assert_type(raw.hash, str).alt(raise_exception).unwrap(),
            assert_opt_type(raw.fa_hash, str).alt(raise_exception).unwrap(),
            assert_type(raw.seen_at, datetime).alt(raise_exception).unwrap(),
        )
        return Success(row)
    except TypeError as err:
        return Failure(err)


def from_stamp(stamp: CommitStamp) -> CommitTableRow:
    return from_objs(stamp.commit.data, stamp.commit.commit_id, stamp.seen_at)


def from_reg(reg: RepoRegistration) -> CommitTableRow:
    return from_objs(None, reg.commit_id, reg.seen_at)


def _encode_opt_datetime(date: Optional[datetime]) -> Optional[str]:
    return (
        Maybe.from_optional(date).map(lambda i: i.isoformat()).value_or(None)
    )


def _encode_opt_int(num: Optional[int]) -> Optional[str]:
    return Maybe.from_optional(num).map(lambda i: str(i)).value_or(None)


def to_dict(row: CommitTableRow) -> Dict[str, Optional[str]]:
    return {
        "author_name": row.author_name,
        "author_email": row.author_email,
        "authored_at": _encode_opt_datetime(row.authored_at),
        "committer_email": row.committer_email,
        "committer_name": row.committer_name,
        "committed_at": _encode_opt_datetime(row.committed_at),
        "message": row.message,
        "summary": row.summary,
        "total_insertions": _encode_opt_int(row.total_insertions),
        "total_deletions": _encode_opt_int(row.total_deletions),
        "total_lines": _encode_opt_int(row.total_lines),
        "total_files": _encode_opt_int(row.total_files),
        "namespace": row.namespace,
        "repository": row.repository,
        "hash": row.hash,
        "fa_hash": row.fa_hash,
        "seen_at": row.seen_at.isoformat(),
    }
