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
from git.repo.base import (
    Repo,
)
import logging
from pathlib import (
    Path,
)
from pathos.threading import (
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

LOG = logging.getLogger(__name__)


class NonexistentPath(Exception):
    pass


def upload_or_register(
    client: Client, extractor: Extractor, repo: Repo
) -> Cmd[None]:
    _register = actions.register(client, extractor.extract_repo())
    _upload = actions.upload_stamps(client, extractor.extract_data(repo))
    return _register.bind(lambda _: _upload)


def upload(
    client: Client,
    namespace: str,
    repo_path: Path,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    repo = Repo(str(repo_path))
    repo_id = RepoId(namespace, repo_path.name)
    info = Cmd.from_cmd(lambda: LOG.info("Uploading %s", repo_id))
    extractor = client.get_context(repo_id).map(
        lambda r: Extractor(r, mailmap)
    )
    return info.bind(
        lambda _: extractor.bind(
            lambda ext: upload_or_register(client, ext, repo)
        )
    )


def upload_repos(
    db_id: DatabaseID,
    creds: Credentials,
    target: TableID,
    namespace: str,
    repo_paths: FrozenList[Path],
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    # pylint: disable=too-many-arguments
    LOG.info(
        "Uploading repos data into %s.%s", target.schema, target.table_name
    )
    client_paths = tuple(
        (Client(ClientFactory().from_creds(db_id, creds), target), p)
        for p in repo_paths
    )
    pool = ThreadPool()

    def _action() -> None:
        pool.map(
            lambda i: unsafe_unwrap(upload(i[0], namespace, i[1], mailmap)),
            client_paths,
        )

    jobs = Cmd.from_cmd(_action)
    return jobs
