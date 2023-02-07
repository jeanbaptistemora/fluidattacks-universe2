from code_etl._utils import (
    COMMIT_HASH_SENTINEL,
)
from code_etl.amend.core import (
    AmendUsers,
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
    DATE_NOW,
    EPOCH_START,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Maybe,
    PureIter,
)
from fa_purity.pure_iter.factory import (
    unsafe_from_cmd,
)
from fa_purity.pure_iter.transform import (
    until_empty,
)
from git.objects.commit import (
    Commit as GitCommit,
)
from git.repo.base import (
    Repo,
)
import logging
from typing import (
    cast,
    Iterable,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Extractor:
    _context: RepoContex
    _mailmap: Maybe[Mailmap]

    def _to_stamp(self, commit: GitCommit) -> Maybe[CommitStamp]:
        LOG.debug("_to_stamp commit %s", commit.hexsha)
        if commit.hexsha == self._context.last_commit:
            LOG.debug("last commit reached")
            return Maybe.empty()
        _obj = CommitDataFactory.from_commit(commit)
        obj = (
            self._mailmap.map(AmendUsers)
            .map(lambda a: a.amend_commit_users(_obj))
            .value_or(_obj)
        )
        data_id = CommitDataId(self._context.repo, obj.commit_id)
        stamp = CommitStamp(
            Commit(data_id, obj.data),
            EPOCH_START if self._context.is_new else DATE_NOW,
        )
        return Maybe.from_value(stamp)

    def extract_all(self, repo: Repo) -> PureIter[GitCommit]:
        # using `unsafe_from_cmd` assumes the repository
        # is read-only/unmodified
        _commits: Cmd[Iterable[GitCommit]] = Cmd.from_cmd(
            lambda: cast(
                Iterable[GitCommit],
                repo.iter_commits(no_merges=True, topo_order=True),
            ),
        )
        return unsafe_from_cmd(_commits)

    def extract_new_data(self, repo: Repo) -> PureIter[CommitStamp]:
        return until_empty(self.extract_all(repo).map(self._to_stamp))

    def extract_repo(self) -> Maybe[RepoRegistration]:
        if self._context.is_new:
            return Maybe.from_value(
                RepoRegistration(
                    CommitDataId(
                        self._context.repo, CommitId(COMMIT_HASH_SENTINEL, "")
                    ),
                    DATE_NOW,
                )
            )
        return Maybe.empty()
