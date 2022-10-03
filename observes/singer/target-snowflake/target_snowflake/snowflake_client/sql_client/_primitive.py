# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from . import (
    _assert,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.json.primitive.core import (
    is_primitive,
    Primitive as JsonPrimitive,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from typing import (
    Callable,
    TypeGuard,
    TypeVar,
)

_T = TypeVar("_T")

UnfoldedPrimitive = JsonPrimitive | datetime


@dataclass(frozen=True)
class Primitive:
    value: UnfoldedPrimitive

    @staticmethod
    def from_any(raw: _T) -> ResultE[Primitive]:
        if is_primitive(raw) or isinstance(raw, datetime):
            return Result.success(Primitive(raw))
        return Result.failure(
            TypeError(f"Expected a `Primitive` but got {type(raw)}")
        )

    @classmethod
    def assert_primitive_list(
        cls, items: FrozenList[_T]
    ) -> ResultE[FrozenList[Primitive]]:
        return _assert.to_list_of(items, lambda i: cls.from_any(i))

    def to_json_primitive(self) -> ResultE[JsonPrimitive]:
        if is_primitive(self.value):
            return Result.success(self.value)
        return Result.failure(
            TypeError(f"Expected `Primitive`(json) got {type(self.value)}")
        )

    def to_str(self) -> ResultE[str]:
        def _inner(item: JsonPrimitive) -> ResultE[str]:
            if isinstance(item, str):
                return Result.success(item)
            return Result.failure(
                TypeError(f"Expected `str` got {type(self.value)}")
            )

        return self.to_json_primitive().bind(_inner)

    def to_bool(self) -> ResultE[bool]:
        def _inner(item: JsonPrimitive) -> ResultE[bool]:
            if isinstance(item, bool):
                return Result.success(item)
            return Result.failure(
                TypeError(f"Expected `str` got {type(self.value)}")
            )

        return self.to_json_primitive().bind(_inner)
