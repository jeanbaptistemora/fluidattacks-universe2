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
from typing import (
    Any,
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


def from_stamp(stamp: CommitStamp) -> CommitTableRow:
    return from_objs(stamp.commit.data, stamp.commit.commit_id, stamp.seen_at)


def from_reg(reg: RepoRegistration) -> CommitTableRow:
    return from_objs(None, reg.commit_id, reg.seen_at)
