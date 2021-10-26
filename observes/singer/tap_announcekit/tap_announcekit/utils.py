from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from purity.v1 import (
    FrozenList,
    InvalidType,
    PrimitiveFactory,
    Transform,
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

_T = TypeVar("_T")
to_opt_primitive = PrimitiveFactory.to_opt_primitive


def new_iter(raw: Union[Iterator[_T], List[_T]]) -> IO[Iterator[_T]]:
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

    @staticmethod
    def to_list(raw: Any) -> List[Any]:
        if isinstance(raw, list):
            return raw
        raise InvalidType(f"{type(raw)} expected List[Any]")

    @staticmethod
    def to_flist(raw: Any, convert: Transform[Any, _T]) -> FrozenList[_T]:
        if isinstance(raw, (tuple, list)):
            return tuple(convert(i) for i in raw)
        raise InvalidType(f"{type(raw)} expected List[Any]")
