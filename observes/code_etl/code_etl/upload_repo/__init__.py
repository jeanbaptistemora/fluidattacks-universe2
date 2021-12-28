# pylint: skip-file

from code_etl.factories import (
    CommitDataFactory,
)
from code_etl.objs import (
    Commit,
    CommitDataId,
    CommitStamp,
    RepoId,
)
from code_etl.utils import (
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
from purity.v1.pure_iter.factory import (
    unsafe_from_generator,
)
from purity.v1.pure_iter.transform import (
    until_empty,
)
from purity.v2.pure_iter.core import (
    PureIter,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)


@dataclass(frozen=True)
class RepoContex:
    repo: RepoId
    last_commit: str
    is_new: bool


def _to_stamp(context: RepoContex, commit: GitCommit) -> Maybe[CommitStamp]:
    if commit.hexsha == context.last_commit:
        return Maybe.empty
    _id, data = CommitDataFactory.from_commit(commit)
    data_id = CommitDataId(
        context.repo.namespace, context.repo.repository, _id
    )
    stamp = CommitStamp(
        Commit(data_id, data),
        DATE_SENTINEL if context.is_new else DATE_NOW,
    )
    return Maybe.from_value(stamp)


def extract_data(context: RepoContex, repo: Repo) -> PureIter[CommitStamp]:
    commits: PureIter[GitCommit] = unsafe_from_generator(
        lambda: IO(repo.iter_commits(no_merges=True, topo_order=True))
    )
    return until_empty(commits.map(lambda c: _to_stamp(context, c)))
