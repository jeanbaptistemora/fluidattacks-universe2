# pylint: skip-file

from code_etl.client.v2 import (
    get_context,
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
    Client,
    ClientFactory,
)
from postgres_client.connection import (
    Credentials,
    DatabaseID,
)
from postgres_client.ids import (
    TableID,
)
from purity.v2.adapters import (
    from_returns,
)
from purity.v2.cmd import (
    Cmd,
    unsafe_unwrap,
)
from purity.v2.frozen import (
    FrozenList,
)
from returns.maybe import (
    Maybe,
)

LOG = logging.getLogger(__name__)


class NonexistentPath(Exception):
    pass


def upload_or_register(
    client: Client, target: TableID, extractor: Extractor, repo: Repo
) -> Cmd[None]:
    _register = actions.register(
        client, target, from_returns(extractor.extract_repo())
    )
    _upload = actions.upload_stamps(
        client, target, extractor.extract_data(repo)
    )
    return _register.bind(lambda _: _upload)


def upload(
    client: Client,
    target: TableID,
    namespace: str,
    repo_path: Path,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    repo = Repo(str(repo_path))
    repo_id = RepoId(namespace, repo_path.name)
    info = Cmd.from_cmd(lambda: LOG.info("Uploading %s", repo_id))
    extractor = get_context(client, target, repo_id).map(
        lambda r: Extractor(r, mailmap)
    )
    return info.bind(
        lambda _: extractor.bind(
            lambda ext: upload_or_register(client, target, ext, repo)
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
    LOG.info(
        "Uploading repos data into %s.%s", target.schema, target.table_name
    )
    client_paths = tuple(
        (ClientFactory().from_creds(db_id, creds), p) for p in repo_paths
    )
    pool = ThreadPool()

    def _action() -> None:
        pool.map(
            lambda i: unsafe_unwrap(
                upload(i[0], target, namespace, i[1], mailmap)
            ),
            client_paths,
        )

    jobs = Cmd.from_cmd(lambda: _action())
    return jobs
