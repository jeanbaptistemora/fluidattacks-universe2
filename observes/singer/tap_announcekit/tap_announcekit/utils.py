from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from purity.v1 import (
    InvalidType,
    PrimitiveFactory,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    TypeVar,
    Union,
)

DataType = TypeVar("DataType")
to_opt_primitive = PrimitiveFactory.to_opt_primitive


def new_iter(
    raw: Union[Iterator[DataType], List[DataType]]
) -> IO[Iterator[DataType]]:
    if isinstance(raw, list):
        return IO(iter(raw))
    return IO(raw)


@dataclass(frozen=True)
class CastUtils:
    @staticmethod
    def to_datetime(raw: Any) -> datetime:
        if isinstance(raw, datetime):
            return raw
        raise InvalidType(f"{type(raw)} expected datetime")

    @classmethod
    def to_opt_dt(cls, raw: Any) -> Optional[datetime]:
        return cls.to_datetime(raw) if raw else None

    @staticmethod
    def to_maybe_str(raw: Any) -> Maybe[str]:
        return Maybe.from_optional(to_opt_primitive(raw, str) if raw else None)
