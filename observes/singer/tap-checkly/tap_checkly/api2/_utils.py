# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    ResultE,
    Stream,
)
from fa_purity.json.primitive.core import (
    NotNonePrimTvar,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_none,
)
from typing import (
    Callable,
    Type,
    TypeVar,
)

_T = TypeVar("_T")


def paginate_all(
    list_items: Callable[[int], Cmd[FrozenList[_T]]]
) -> Stream[_T]:
    return (
        infinite_range(1, 1)
        .map(list_items)
        .transform(lambda x: from_piter(x))
        .map(lambda i: i if bool(i) else None)
        .transform(lambda x: until_none(x))
        .map(lambda x: from_flist(x))
        .transform(lambda x: chain(x))
    )


@dataclass(frozen=True)
class ExtendedUnfolder:
    json: JsonObj

    def get(self, key: str) -> Maybe[JsonValue]:
        return Maybe.from_optional(self.json.get(key))

    def get_required(self, key: str) -> ResultE[JsonValue]:
        return (
            self.get(key)
            .to_result()
            .alt(lambda _: KeyError(key))
            .alt(Exception)
        )

    def require_primitive(
        self, key: str, prim_type: Type[NotNonePrimTvar]
    ) -> ResultE[NotNonePrimTvar]:
        return (
            self.get_required(key)
            .map(Unfolder)
            .bind(
                lambda u: u.to_primitive(prim_type).alt(
                    lambda e: TypeError(f"At `{key}` i.e. {e}")
                )
            )
        )

    def require_float(self, key: str) -> ResultE[float]:
        return (
            self.get_required(key)
            .map(Unfolder)
            .bind(
                lambda u: u.to_primitive(float)
                .alt(Exception)
                .lash(
                    lambda _: u.to_primitive(int)
                    .map(float)
                    .alt(lambda e: TypeError(f"At `{key}` i.e. {e}"))
                )
            )
        )
