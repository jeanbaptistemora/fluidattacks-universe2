from ._utils import (
    DateInterval,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Maybe,
)


@dataclass(frozen=True)
class EtlState:
    results: Maybe[DateInterval]  # check results stream
