from __future__ import (
    annotations,
)

from ._complete_record import (
    CompletePlainRecord,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    PureIter,
    Result,
)
from fa_purity.utils import (
    raise_exception,
)
from fa_singer_io.singer import (
    SingerSchema,
)
from typing import (
    NoReturn,
)


@dataclass(frozen=True)
class _RecordGroup:
    schema: SingerSchema
    records: PureIter[CompletePlainRecord]


@dataclass(frozen=True)
class RecordGroup:
    """
    Group of CompletePlainRecord that share same schema
    """

    _inner: _RecordGroup

    @property
    def schema(self) -> SingerSchema:
        return self._inner.schema

    @property
    def records(self) -> PureIter[CompletePlainRecord]:
        return self._inner.records

    @staticmethod
    def filter(
        schema: SingerSchema, records: PureIter[CompletePlainRecord]
    ) -> RecordGroup:
        items = records.filter(lambda r: r.schema == schema)
        return RecordGroup(_RecordGroup(schema, items))

    @staticmethod
    def new(
        schema: SingerSchema, records: PureIter[CompletePlainRecord]
    ) -> RecordGroup | NoReturn:
        items = (
            records.map(
                lambda r: Result.success(r, CompletePlainRecord)
                if r.schema == schema
                else Result.failure(r, CompletePlainRecord)
            )
            .map(
                lambda r: r.alt(
                    lambda x: ValueError(
                        f"A record does not belong to the RecordGroup. Expected schema `{schema}` but got `{x.schema}`"
                    )
                )
            )
            .map(lambda r: r.alt(raise_exception).unwrap())
        )
        return RecordGroup(_RecordGroup(schema, items))
