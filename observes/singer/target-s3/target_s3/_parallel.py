from fa_purity import (
    Cmd,
    PureIter,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
from pathos.threading import (
    ThreadPool,
)


def in_threads(cmds: PureIter[Cmd[None]], workers: int) -> Cmd[None]:
    def _action(act: CmdUnwrapper) -> None:
        pool = ThreadPool(workers)  # type: ignore[misc]
        jobs = pool.imap(lambda c: act.unwrap(c), cmds)  # type: ignore[misc]
        for _ in jobs:  # type: ignore[misc]
            # Consume pool map
            pass

    return new_cmd(_action)
