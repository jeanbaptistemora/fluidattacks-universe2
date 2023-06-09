from . import (
    _splitter,
)
from ._parallel import (
    in_threads,
)
from ._splitter import (
    GroupedRecords,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
    Result,
    ResultE,
    Stream,
)
from fa_purity.json.factory import (
    loads,
)
from fa_purity.pure_iter import (
    factory as PureIterFactory,
)
from fa_singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from fa_singer_io.singer.deserializer import (
    deserialize,
)
import logging
from target_s3.core import (
    CompletePlainRecord,
    PlainRecord,
    RecordGroup,
)
from target_s3.csv import (
    CsvKeeperFactory,
)
from target_s3.upload import (
    new_client,
    S3FileUploader,
)
from typing import (
    NoReturn,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _complete_record(
    schemas: FrozenDict[str, SingerSchema], record: SingerRecord
) -> ResultE[CompletePlainRecord]:
    schema = Maybe.from_optional(schemas.get(record.stream))
    return PlainRecord.from_singer(record).bind(
        lambda p: schema.to_result()
        .alt(lambda _: Exception(f"Missing {record.stream} on schemas map"))
        .bind(lambda sh: CompletePlainRecord.new(sh, p))
    )


def _assert_record(item: _T) -> ResultE[SingerRecord]:
    if isinstance(item, SingerRecord):
        return Result.success(item)
    err = Exception(f"Expected `SingerRecord` got `{type(item)}`")
    return Result.failure(err)


def _process_group(
    uploader: S3FileUploader,
    schemas: FrozenDict[str, SingerSchema],
    group: GroupedRecords,
) -> Cmd[None] | NoReturn:
    records = group.file.read().map(
        lambda i: loads(i)
        .alt(Exception)
        .bind(deserialize)
        .bind(_assert_record)
    )
    completed = records.map(
        lambda r: r.bind(lambda d: _complete_record(schemas, d))
    )
    schema = schemas[group.stream]
    r_group = RecordGroup.filter(schema, completed.map(lambda x: x.unwrap()))
    return uploader.upload_to_s3(r_group)


def main(
    bucket: str, prefix: str, data: Stream[str], str_limit: int
) -> Cmd[None] | NoReturn:
    client = new_client()
    keeper = CsvKeeperFactory.new(str_limit)
    uploader = client.map(lambda c: S3FileUploader(c, keeper, bucket, prefix))
    singer = data.map(
        lambda i: loads(i).alt(Exception).bind(deserialize).unwrap()
    )
    start = Cmd.from_cmd(lambda: LOG.info("Process groups started"))
    return uploader.bind(
        lambda u: _splitter.group_records(singer).bind(
            lambda t: start
            + in_threads(
                PureIterFactory.from_flist(
                    tuple(_process_group(u, t[0], g) for g in t[1])
                ),
                100,
            )
        )
    )
