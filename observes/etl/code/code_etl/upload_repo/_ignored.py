from code_etl.arm import (
    IgnoredPath,
)
from code_etl.objs import (
    CommitStamp,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Maybe,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from typing import (
    FrozenSet,
)


def _path_match(path: str, ignored: str) -> bool:
    return path.lstrip("/").startswith(ignored.lstrip("/"))


def _ignored_path(path: str, ignored: FrozenSet[str]) -> bool:
    return any(_path_match(path, i) for i in ignored)


@dataclass(frozen=True)
class IgnoredFilter:
    ignored: FrozenSet[IgnoredPath]

    def _ignored_paths(self, stamp: CommitStamp) -> FrozenSet[IgnoredPath]:
        ignored = from_flist(tuple(self.ignored)).filter(
            lambda i: i.nickname == stamp.commit.commit_id.repo.repository
            and i.group == stamp.commit.commit_id.repo.namespace
        )
        return frozenset(ignored)

    def filter_stamp(self, stamp: CommitStamp) -> Maybe[CommitStamp]:
        ignored = frozenset(i.file_path for i in self._ignored_paths(stamp))
        ignored_stamp = stamp.commit.data.files.map(
            lambda files: all(_ignored_path(f, ignored) for f in files)
        ).value_or(False)
        return Maybe.from_optional(None if ignored_stamp else stamp)
