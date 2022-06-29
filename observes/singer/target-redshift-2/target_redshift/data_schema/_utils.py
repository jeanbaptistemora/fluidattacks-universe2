from fa_purity import (
    JsonObj,
    Maybe,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


def opt_transform(
    obj: JsonObj, key: str, transform: Callable[[Unfolder], _T]
) -> Maybe[_T]:
    return Maybe.from_optional(obj.get(key)).map(
        lambda p: transform(Unfolder(p))
    )
