from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_singer_io.singer import (
    SingerSchema,
)
from target_s3.plain_record import (
    PlainRecord,
)


@dataclass(frozen=True)
class _CompletePlainRecord:
    schema: SingerSchema
    record: PlainRecord


@dataclass(frozen=True)
class CompletePlainRecord:
    """
    `PlainRecord` that has all the fields specified on the related schema.
    """

    _inner: _CompletePlainRecord

    @property
    def record(self) -> PlainRecord:
        return self._inner.record

    @property
    def schema(self) -> SingerSchema:
        return self._inner.schema

    @staticmethod
    def new(
        schema: SingerSchema, record: PlainRecord
    ) -> ResultE[CompletePlainRecord]:
        """
        Fills missing record fields (according to the schema) with `None` values
        """
        if schema.stream != record.stream:
            err = ValueError(
                f"Stream mismatch between schema and record: {schema.stream} != {record.stream}"
            )
            return Result.failure(err)
        return (
            Maybe.from_optional(schema.schema.encode().get("properties"))
            .to_result()
            .alt(
                lambda _: ValueError(
                    f"Missing `properties` key at schema of stream `{schema.stream}`"
                )
            )
            .alt(Exception)
            .bind(
                lambda p: Unfolder(p)
                .to_json()
                .alt(Exception)
                .map(
                    lambda d: FrozenDict(
                        {i: None for i in d} | dict(record.record)
                    )
                )
            )
            .map(
                lambda f: CompletePlainRecord(
                    _CompletePlainRecord(
                        schema, PlainRecord.new(schema.stream, f)
                    )
                )
            )
        )
