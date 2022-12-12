from __future__ import (
    annotations,
)

from ._raw import (
    RawClient,
)
from code_etl.client import (
    encoder,
)
from code_etl.objs import (
    Commit,
    CommitDataId,
    CommitStamp,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from logging import (
    Logger,
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

    def delta_update(self, log: Logger, raw: RawClient) -> Cmd[None]:
        if self.is_diff():
            info = Cmd.from_cmd(
                lambda: log.info("delta update %s", self.commit_id)
            )
            return info + raw.delta_update(
                encoder.from_stamp(self.old),
                encoder.from_stamp(self.new),
            )
        return Cmd.from_cmd(lambda: None)
