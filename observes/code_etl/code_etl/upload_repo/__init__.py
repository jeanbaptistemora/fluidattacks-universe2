from code_etl.client import (
    Client,
    LegacyAdapters,
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
from fa_purity.result import (
    Result,
    ResultE,
)
from git import (
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
from postgres_client.client import (
    ClientFactory,
)
from postgres_client.connection import (
    Credentials,
    DatabaseID,
)
from postgres_client.ids import (
    TableID,
)
from redshift_client.sql_client import (
    new_client,
)
from redshift_client.sql_client.connection import (
    connect,
    DbConnection,
    IsolationLvl,
)

LOG = logging.getLogger(__name__)


class NonexistentPath(Exception):
    pass


def upload_or_register(
    client: Client, extractor: Extractor, repo: Repo
) -> Cmd[None]:
    _register = actions.register(client, extractor.extract_repo())
    _upload = actions.upload_stamps(client, extractor.extract_data(repo))
    return _register.bind(lambda _: _upload)


def _try_repo(raw: str) -> ResultE[Repo]:
    try:
        return Result.success(Repo(raw))
    except InvalidGitRepositoryError as err:
        return Result.failure(err)


def upload(
    client: Client,
    namespace: str,
    repo_path: Path,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    repo = _try_repo(str(repo_path))
    repo_id = RepoId(namespace, repo_path.name)
    info = Cmd.from_cmd(lambda: LOG.info("Uploading %s", repo_id))
    extractor = client.get_context(repo_id).map(
        lambda r: Extractor(r, mailmap)
    )
    report = Cmd.from_cmd(
        lambda: LOG.error("InvalidGitRepositoryError at %s", repo_id)
    )
    return repo.map(
        lambda r: info.bind(
            lambda _: extractor.bind(
                lambda ext: upload_or_register(client, ext, r)
            )
        )
    ).value_or(report)


def _upload_repos(
    connection: DbConnection,
    db_id: DatabaseID,
    creds: Credentials,
    target: TableID,
    namespace: str,
    repo_paths: FrozenList[Path],
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    LOG.info(
        "Uploading repos data into %s.%s", target.schema, target.table_name
    )

    def _new_client(path: Path) -> Cmd[Client]:
        return new_client(connection, LOG.getChild(str(path))).map(
            lambda c: Client(
                ClientFactory().from_creds(db_id, creds), c, target
            )
        )

    client_paths = tuple(
        _new_client(p).map(lambda c: (c, p)) for p in repo_paths
    )
    pool = ThreadPool()  # type: ignore[misc]

    def _action() -> None:
        pool.map(  # type: ignore[misc]
            lambda i: unsafe_unwrap(i.map(lambda t: upload(t[0], namespace, t[1], mailmap))),  # type: ignore[misc]
            client_paths,
        )

    jobs = Cmd.from_cmd(_action)
    return jobs


def upload_repos(
    db_id: DatabaseID,
    creds: Credentials,
    target: TableID,
    namespace: str,
    repo_paths: FrozenList[Path],
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    # pylint: disable=too-many-arguments
    connection = connect(
        LegacyAdapters.db_id(db_id),
        LegacyAdapters.db_creds(creds),
        False,
        IsolationLvl.AUTOCOMMIT,
    )

    def _action() -> None:
        conn = unsafe_unwrap(connection)
        try:
            unsafe_unwrap(
                _upload_repos(
                    conn, db_id, creds, target, namespace, repo_paths, mailmap
                )
            )
        finally:
            unsafe_unwrap(conn.close())

    return Cmd.from_cmd(_action)
