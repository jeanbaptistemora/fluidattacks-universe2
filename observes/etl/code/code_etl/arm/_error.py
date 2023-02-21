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


@dataclass(frozen=True)
class DecodeError(Exception):
    description: str
    value: str
    previous: Exception

    def __str__(self) -> str:
        return "DecodeError: " + super().__str__()
