# Iterable builders
# should always return a new instance because Iterables are mutable
from itertools import (
    chain,
)
from purity.v1._pure_iter._obj import (
    Mappable,
    PureIter,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Iterable,
    TypeVar,
)

_I = TypeVar("_I")


class IterableFactoryIO:
    # pylint: disable=too-few-public-methods
    @staticmethod
    def chain_io(
        unchained: PureIter[IO[Mappable[_I]]],
    ) -> Iterable[IO[_I]]:
        iters = (unsafe_perform_io(i) for i in iter(unchained))
        return map(IO, chain.from_iterable(iters))
