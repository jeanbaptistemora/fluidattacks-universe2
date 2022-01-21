# pylint: skip-file

from code_etl.client import (
    insert_stamps,
    register_repos,
)
from code_etl.objs import (
    CommitStamp,
    RepoRegistration,
)
from postgres_client.client import (
    Client,
)
from postgres_client.ids import (
    TableID,
)
from purity.v1.pure_iter.core import (
    PureIter,
)
from purity.v1.pure_iter.transform.io import (
    consume,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)


def register(
    client: Client, target: TableID, reg: Maybe[RepoRegistration]
) -> Maybe[IO[None]]:
    return reg.map(lambda i: register_repos(client, target, (i,)))


def upload_stamps(
    client: Client, target: TableID, stamps: PureIter[CommitStamp]
) -> IO[None]:
    actions = stamps.chunked(2000).map(
        lambda s: insert_stamps(client, target, tuple(s))
    )
    return consume(actions)
