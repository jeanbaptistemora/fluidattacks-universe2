from ._ignored import (
    IgnoredFilter,
)
from code_etl.arm import (
    ArmClient,
)
from code_etl.client import (
    Client,
)
from code_etl.objs import (
    CommitStamp,
    RepoRegistration,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.pure_iter.core import (
    PureIter,
)
from fa_purity.pure_iter.transform import (
    consume,
)


def register(client: Client, reg: Maybe[RepoRegistration]) -> Cmd[None]:
    none = Cmd.from_cmd(lambda: None)
    _register: Maybe[Cmd[None]] = reg.map(
        lambda i: client.register_repos((i,))
    )
    return _register.value_or(none)


def filter_ignored(
    client: ArmClient, group: str, stamp: CommitStamp
) -> Cmd[Maybe[CommitStamp]]:
    ignored_paths = client.get_ignored_paths(group)
    return ignored_paths.map(lambda i: IgnoredFilter(i).filter_stamp(stamp))


def upload_stamps(client: Client, stamps: PureIter[CommitStamp]) -> Cmd[None]:
    actions: PureIter[Cmd[None]] = stamps.chunked(2000).map(
        client.insert_stamps
    )
    return consume(actions)
