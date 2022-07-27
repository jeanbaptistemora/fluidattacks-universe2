from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    PureIter,
    Result,
)
from target_s3.plain_record import (
    PlainRecord,
)


@dataclass(frozen=True)
class _RecordGroup:
    stream: str
    records: PureIter[PlainRecord]


@dataclass(frozen=True)
class RecordGroup:
    """
    Group of PlainRecord that share same stream
    """

    _inner: _RecordGroup

    @property
    def stream(self) -> str:
        return self._inner.stream

    @property
    def records(self) -> PureIter[PlainRecord]:
        return self._inner.records

    @staticmethod
    def filter(stream: str, records: PureIter[PlainRecord]) -> RecordGroup:
        items = records.filter(lambda r: r.stream == stream)
        return RecordGroup(_RecordGroup(stream, items))

    @staticmethod
    def new(stream: str, records: PureIter[PlainRecord]) -> RecordGroup:
        items = records.map(
            lambda r: Result.success(r, PlainRecord)
            if r.stream == stream
            else Result.failure(r, PlainRecord)
        ).map(
            lambda r: r.alt(
                lambda x: ValueError(
                    f"A record does not belong to the RecordGroup. Expected stream `{stream}` but got `{x.stream}`"
                )
            ).unwrap()
        )
        return RecordGroup(_RecordGroup(stream, items))
