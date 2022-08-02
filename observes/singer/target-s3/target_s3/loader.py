from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
    PureIter,
    Result,
    ResultE,
    Stream,
)
from fa_purity.json.factory import (
    loads,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    consume,
    filter_opt,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.utils import (
    raise_exception,
)
from fa_singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from fa_singer_io.singer.deserializer import (
    deserialize,
)
from target_s3.core import (
    CompletePlainRecord,
    PlainRecord,
    RecordGroup,
    TempReadOnlyFile,
)
from target_s3.csv import (
    save,
)
from target_s3.in_buffer import (
    stdin_buffer,
)
from target_s3.upload import (
    new_client,
    S3FileUploader,
)
from typing import (
    FrozenSet,
    Tuple,
)


def _gen_schema_map(
    schemas: PureIter[SingerSchema],
) -> ResultE[FrozenDict[str, SingerSchema]]:
    streams = schemas.map(lambda x: x.stream)
    if len(frozenset(streams)) != len(tuple(streams)):
        err = ValueError("Detected more than one schema for the same stream")
        return Result.failure(err)
    return Result.success(FrozenDict({s.stream: s for s in schemas}))


def _transform_records(
    schema_map: FrozenDict[str, SingerSchema], records: PureIter[SingerRecord]
) -> ResultE[PureIter[CompletePlainRecord]]:
    def _get_schema(stream: str) -> ResultE[SingerSchema]:
        return (
            Maybe.from_optional(schema_map.get(stream))
            .to_result()
            .alt(
                lambda _: ValueError(
                    f"A record is referring to a stream with missing schema i.e. `{stream}`"
                )
            )
        )

    return records.map(
        lambda s: PlainRecord.from_singer(s).bind(
            lambda p: _get_schema(p.stream).bind(
                lambda sh: CompletePlainRecord.new(sh, p)
            )
        )
    ).transform(lambda x: all_ok(tuple(x)).map(lambda y: from_flist(y)))


def _extract(
    file: TempReadOnlyFile,
) -> ResultE[
    Tuple[FrozenDict[str, SingerSchema], PureIter[CompletePlainRecord]]
]:
    msgs = file.read().map(
        lambda i: loads(i).alt(Exception).bind(deserialize).unwrap()
    )
    schemas = (
        msgs.map(lambda s: s if isinstance(s, SingerSchema) else None)
        .transform(lambda x: filter_opt(x))
        .transform(
            lambda p: from_flist(
                tuple(p)
            )  # this will save schemas into a tuple instead of computing everytime from the raw file
        )
        .transform(_gen_schema_map)
    )
    records = msgs.map(
        lambda s: s if isinstance(s, SingerRecord) else None
    ).transform(lambda x: filter_opt(x))
    return schemas.bind(
        lambda s_map: _transform_records(s_map, records).map(
            lambda p: (s_map, p)
        )
    )


def _group(
    schemas: FrozenSet[SingerSchema], records: PureIter[CompletePlainRecord]
) -> PureIter[RecordGroup]:
    return from_flist(tuple(schemas)).map(
        lambda s: RecordGroup.filter(s, records)
    )


def _process(
    uploader: S3FileUploader, data: TempReadOnlyFile
) -> ResultE[Cmd[None]]:
    extraction = _extract(data)
    return extraction.map(
        lambda t: _group(frozenset(v for _, v in t[0].items()), t[1])
        .transform(
            lambda p: p.map(
                lambda g: save(g).bind(lambda t: uploader.upload_to_s3(g, t))
            )
        )
        .transform(lambda p: consume(p))
    )


def main(
    bucket: str, prefix: str, data: Stream[str]
) -> Cmd[ResultE[Cmd[None]]]:
    client = new_client()
    uploader = client.map(lambda c: S3FileUploader(c, bucket, prefix))
    return TempReadOnlyFile.save(data).bind(
        lambda x: uploader.map(lambda u: _process(u, x))
    )
