# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
    JsonValue,
    PureIter,
)
from fa_singer_io.json_schema import (
    factory as JSchemaFactory,
)
from fa_singer_io.json_schema.core import (
    JsonSchema,
)
from fa_singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from typing import (
    Callable,
    Generic,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


@dataclass(frozen=True)
class SingerEncoder(Generic[_T]):
    schemas: PureIter[SingerSchema]
    _records: _Patch[Callable[[_T], PureIter[SingerRecord]]]

    def records(self, item: _T) -> PureIter[SingerRecord]:
        return self._records.inner(item)

    @staticmethod
    def new(
        schemas: PureIter[SingerSchema],
        records: Callable[[_T], PureIter[SingerRecord]],
    ) -> SingerEncoder[_T]:
        return SingerEncoder(
            schemas,
            _Patch(records),
        )


@dataclass(frozen=True)
class JsonSchemaFactory:
    @staticmethod
    def obj_schema(props: FrozenDict[str, JsonSchema]) -> JsonSchema:
        _props = FrozenDict(
            {k: JsonValue(v.encode()) for k, v in props.items()}
        )
        raw = {
            "properties": JsonValue(_props),
            "required": JsonValue(tuple(JsonValue(k) for k in _props.keys())),
        }
        return JSchemaFactory.from_json(FrozenDict(raw)).unwrap()
