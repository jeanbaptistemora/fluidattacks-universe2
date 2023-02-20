from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenList,
    JsonValue,
)


@dataclass(frozen=True)
class ApiError(Exception):
    errors: FrozenList[JsonValue]

    def to_exception(self) -> Exception:
        return Exception(self)
