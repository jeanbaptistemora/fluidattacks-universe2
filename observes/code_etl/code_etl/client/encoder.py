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
    Optional,
)


@dataclass(frozen=True)
class CommitTableRow:
    # pylint: disable=too-many-instance-attributes
    author_name: Optional[str]
    author_email: Optional[str]
    authored_at: Optional[str]
    committer_email: Optional[str]
    committer_name: Optional[str]
    committed_at: Optional[str]
    message: Optional[str]
    summary: Optional[str]
    total_insertions: Optional[int]
    total_deletions: Optional[int]
    total_lines: Optional[int]
    total_files: Optional[int]
    namespace: str
    repository: str
    hash: str
    fa_hash: str
    seen_at: str


def from_objs(
    data: Optional[CommitData], commit_id: CommitDataId, seen_at: datetime
) -> CommitTableRow:
    return CommitTableRow(
        data.author.name if data else None,
        data.author.email if data else None,
        data.authored_at.isoformat() if data else None,
        data.committer.name if data else None,
        data.committer.email if data else None,
        data.committed_at.isoformat() if data else None,
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
        seen_at.isoformat(),
    )


def from_stamp(stamp: CommitStamp) -> CommitTableRow:
    return from_objs(stamp.commit.data, stamp.commit.commit_id, stamp.seen_at)


def from_reg(reg: RepoRegistration) -> CommitTableRow:
    return from_objs(None, reg.commit_id, reg.seen_at)
