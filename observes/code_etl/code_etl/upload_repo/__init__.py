# pylint: skip-file

from code_etl.client import (
    get_context,
    insert_stamps,
    register_repos,
)
from code_etl.factories import (
    CommitDataFactory,
)
from code_etl.objs import (
    Commit,
    CommitDataId,
    CommitId,
    CommitStamp,
    RepoContex,
    RepoId,
    RepoRegistration,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
    DATE_NOW,
    DATE_SENTINEL,
)
from git.objects import (
    Commit as GitCommit,
)
from git.repo.base import (
    Repo,
)
from pathlib import (
    Path,
)
from postgres_client.client import (
    Client,
)
from postgres_client.ids import (
    TableID,
)
from purity.v1.pure_iter.factory import (
    unsafe_from_generator,
)
from purity.v1.pure_iter.transform import (
    until_empty,
)
from purity.v1.pure_iter.transform.io import (
    consume,
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
from returns.result import (
    Failure,
    ResultE,
)


class NonexistentPath(Exception):
    pass


def _to_stamp(context: RepoContex, commit: GitCommit) -> Maybe[CommitStamp]:
    if commit.hexsha == context.last_commit:
        return Maybe.empty
    _id, data = CommitDataFactory.from_commit(commit)
    data_id = CommitDataId(context.repo, _id)
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


def extract_repo(context: RepoContex) -> Maybe[RepoRegistration]:
    if context.is_new:
        return Maybe.from_value(
            RepoRegistration(
                CommitDataId(context.repo, CommitId(COMMIT_HASH_SENTINEL, "")),
                DATE_NOW,
            )
        )
    return Maybe.empty


def register(
    client: Client, target: TableID, context: RepoContex
) -> Maybe[IO[None]]:
    return extract_repo(context).map(
        lambda i: register_repos(client, target, (i,))
    )


def upload_repo(
    client: Client, target: TableID, context: RepoContex, repo: Repo
) -> IO[None]:
    actions = (
        extract_data(context, repo)
        .chunked(2000)
        .map(lambda s: insert_stamps(client, target, tuple(s)))
    )
    return consume(actions)


def upload_or_register(
    client: Client, target: TableID, context: RepoContex, repo: Repo
) -> IO[None]:
    register(client, target, context)
    return upload_repo(client, target, context, repo)


def upload(
    client: Client, target: TableID, namespace: str, repo_path: Path
) -> IO[ResultE[IO[None]]]:
    if not repo_path.exists():
        return IO(Failure(NonexistentPath(str(repo_path))))
    repo = Repo(str(repo_path))
    repo_id = RepoId(namespace, repo_path.name)
    return get_context(client, target, repo_id).map(
        lambda r_context: r_context.map(
            lambda context: upload_or_register(client, target, context, repo)
        )
    )
