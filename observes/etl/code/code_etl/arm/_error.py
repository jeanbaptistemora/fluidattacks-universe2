from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenList,
    JsonValue,
)


@dataclass(frozen=True)
class ApiError:
    errors: FrozenList[JsonValue]


@dataclass(frozen=True)
class DecodeError:
    description: str
    value: str
    previous: Exception
