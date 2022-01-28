from code_etl.client.v2 import (
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
from purity.v2.cmd import (
    Cmd,
)
from purity.v2.maybe import (
    Maybe,
)
from purity.v2.pure_iter.core import (
    PureIter,
)
from purity.v2.pure_iter.transform import (
    consume,
)


def register(
    client: Client, target: TableID, reg: Maybe[RepoRegistration]
) -> Cmd[None]:
    none = Cmd.from_cmd(lambda: None)
    _register: Maybe[Cmd[None]] = reg.map(
        lambda i: register_repos(client, target, (i,))
    )
    return _register.value_or(none)


def upload_stamps(
    client: Client, target: TableID, stamps: PureIter[CommitStamp]
) -> Cmd[None]:
    actions: PureIter[Cmd[None]] = stamps.chunked(2000).map(
        lambda s: insert_stamps(client, target, tuple(s))
    )
    return consume(actions)
