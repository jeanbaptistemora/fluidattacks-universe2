from code_etl.client import (
    Client,
)
from code_etl.objs import (
    CommitStamp,
    RepoRegistration,
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


def register(client: Client, reg: Maybe[RepoRegistration]) -> Cmd[None]:
    none = Cmd.from_cmd(lambda: None)
    _register: Maybe[Cmd[None]] = reg.map(
        lambda i: client.register_repos((i,))
    )
    return _register.value_or(none)


def upload_stamps(client: Client, stamps: PureIter[CommitStamp]) -> Cmd[None]:
    actions: PureIter[Cmd[None]] = stamps.chunked(2000).map(
        client.insert_stamps
    )
    return consume(actions)
