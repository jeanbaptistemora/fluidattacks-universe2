from code_etl import (
    _utils,
)
from code_etl.client import (
    Client,
)
from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
    RepoId,
)
from code_etl.upload_repo import (
    actions,
)
from code_etl.upload_repo.extractor import (
    Extractor,
)
from fa_purity.cmd import (
    Cmd,
    unsafe_unwrap,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.result import (
    Result,
    ResultE,
    ResultFactory,
)
from git.exc import (
    InvalidGitRepositoryError,
)
from git.repo.base import (
    Repo,
)
import logging
from pathlib import (
    Path,
)
from pathos.threading import (  # type: ignore[import]
    ThreadPool,
)
from redshift_client.sql_client import (
    new_client,
)
from redshift_client.sql_client.connection import (
    connect,
    Credentials,
    DatabaseId,
    DbConnection,
    IsolationLvl,
)
from typing import (
    Tuple,
)

LOG = logging.getLogger(__name__)


class NonexistentPath(Exception):
    pass


def upload_or_register(
    client: Client, extractor: Extractor, repo: Repo
) -> Cmd[None]:
    LOG.debug("upload_or_register")
    LOG.debug(extractor.extract_repo())
    _register = actions.register(client, extractor.extract_repo())
    _upload = actions.upload_stamps(client, extractor.extract_new_data(repo))
    return _register.bind(lambda _: _upload)


def _try_repo(raw: str) -> ResultE[Repo]:
    factory: ResultFactory[Repo, Exception] = ResultFactory()
    try:
        return factory.success(Repo(raw))
    except InvalidGitRepositoryError as err:
        return factory.failure(err)


def upload(
    client: Client,
    namespace: str,
    repo_path: Path,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    repo = _try_repo(str(repo_path))
    repo_id = RepoId(namespace, repo_path.name)
    info = Cmd.from_cmd(lambda: LOG.info("Uploading the repo: %s", repo_id))
    extractor = client.get_context(repo_id).map(
        lambda r: Extractor(r, mailmap)
    )
    report = Cmd.from_cmd(
        lambda: LOG.error("InvalidGitRepositoryError at %s", repo_id)
    )
    return repo.map(
        lambda r: info
        + extractor.bind(lambda ext: upload_or_register(client, ext, r))
    ).value_or(report)


def _upload_repos(
    connection: DbConnection,
    namespace: str,
    repo_paths: FrozenList[Path],
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    LOG.info("Uploading repos data")

    def _new_client(path: Path) -> Cmd[Client]:
        return new_client(connection, LOG.getChild(str(path))).map(Client.new)

    def _pair(path: Path) -> Cmd[Tuple[Client, Path]]:
        return _new_client(path).map(lambda c: (c, path))

    cmds = (
        from_flist(repo_paths)
        .map(_pair)
        .map(
            lambda a: a.bind(lambda t: upload(t[0], namespace, t[1], mailmap))
        )
    )
    return _utils.cmds_in_threads(cmds.to_list())


def upload_repos(
    db_id: DatabaseId,
    creds: Credentials,
    namespace: str,
    repo_paths: FrozenList[Path],
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    # pylint: disable=too-many-arguments
    connection = connect(
        db_id,
        creds,
        False,
        IsolationLvl.AUTOCOMMIT,
    )
    return _utils.wrap_connection(
        connection, lambda c: _upload_repos(c, namespace, repo_paths, mailmap)
    )
