from purity.v2 import (
    _iter_factory,
)
from purity.v2.cmd import (
    Cmd,
)
from purity.v2.pure_iter.core import (
    PureIter,
)
from purity.v2.stream.core import (
    _Stream,
    Stream,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def from_piter(piter: PureIter[Cmd[_T]]) -> Stream[_T]:
    draft = _Stream(Cmd.from_cmd(lambda: _iter_factory.squash(piter)))
    return Stream(draft)
