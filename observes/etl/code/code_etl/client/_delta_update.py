from __future__ import (
    annotations,
)

from code_etl.objs import (
    Commit,
    CommitDataId,
    CommitStamp,
)
from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class CommitStampDiff:
    """Wraps two `CommitStamp` objects that share the same `CommitDataId`"""

    _private: _Private
    old: CommitStamp
    new: CommitStamp

    @staticmethod
    def from_stamps(old: CommitStamp, new: CommitStamp) -> CommitStampDiff:
        """Create new `CommitStampDiff` with old stamp `CommitDataId` as common id"""
        return CommitStampDiff(
            _Private(),
            old,
            CommitStamp(
                Commit(old.commit.commit_id, new.commit.data), new.seen_at
            ),
        )

    def commit_id(self) -> CommitDataId:
        return self.old.commit.commit_id

    def is_diff(self) -> bool:
        return self.old != self.new
