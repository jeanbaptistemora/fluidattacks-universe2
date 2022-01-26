# pylint: skip-file

from code_etl.amend.core import (
    amend_commit_users,
)
from code_etl.factories import (
    CommitDataFactory,
)
from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
    Commit,
    CommitDataId,
    CommitId,
    CommitStamp,
    RepoContex,
    RepoRegistration,
)
from code_etl.time_utils import (
    to_utc,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
    DATE_NOW,
    DATE_SENTINEL,
)
from dataclasses import (
    dataclass,
)
from git.objects import (
    Commit as GitCommit,
)
from git.repo.base import (
    Repo,
)
from purity.v1.pure_iter.core import (
    PureIter,
)
from purity.v1.pure_iter.factory import (
    unsafe_from_generator,
)
from purity.v1.pure_iter.transform import (
    until_empty,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)


@dataclass(frozen=True)
class Extractor:
    _context: RepoContex
    _mailmap: Maybe[Mailmap]

    def _to_stamp(self, commit: GitCommit) -> Maybe[CommitStamp]:
        if commit.hexsha == self._context.last_commit:
            return Maybe.empty
        _obj = CommitDataFactory.from_commit(commit)
        obj = self._mailmap.map(
            lambda m: amend_commit_users(m, _obj)
        ).value_or(_obj)
        data_id = CommitDataId(self._context.repo, obj.commit_id)
        stamp = CommitStamp(
            Commit(data_id, obj.data),
            to_utc(DATE_SENTINEL if self._context.is_new else DATE_NOW),
        )
        return Maybe.from_value(stamp)

    def extract_data(self, repo: Repo) -> PureIter[CommitStamp]:
        commits: PureIter[GitCommit] = unsafe_from_generator(
            lambda: IO(repo.iter_commits(no_merges=True, topo_order=True))
        )
        return until_empty(commits.map(self._to_stamp))

    def extract_repo(self) -> Maybe[RepoRegistration]:
        if self._context.is_new:
            return Maybe.from_value(
                RepoRegistration(
                    CommitDataId(
                        self._context.repo, CommitId(COMMIT_HASH_SENTINEL, "")
                    ),
                    to_utc(DATE_NOW),
                )
            )
        return Maybe.empty
