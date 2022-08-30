from . import (
    _utils,
)
import csv
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    JsonValue,
    Maybe,
    PureIter,
    Result,
    ResultE,
)
from fa_purity.json.primitive.core import (
    Primitive,
)
from fa_purity.json.primitive.factory import (
    to_opt_primitive,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
import logging
from target_s3.core import (
    CompletePlainRecord,
    PlainRecord,
    RecordGroup,
    TempReadOnlyFile,
)
from typing import (
    FrozenSet,
    IO,
    Tuple,
)

LOG = logging.getLogger(__name__)


def _save(data: PureIter[FrozenList[Primitive]]) -> Cmd[TempReadOnlyFile]:
    def write_cmd(file: IO[str]) -> Cmd[None]:
        def _action() -> None:
            writer = csv.writer(
                file,
                delimiter=",",
                quotechar='"',
                doublequote=True,
                escapechar="\\",
                quoting=csv.QUOTE_MINIMAL,
            )
            for row in data:
                try:
                    writer.writerow(row)
                except Exception as err:
                    LOG.error(
                        "writerow error: %s\n at data: %s", str(err), str(row)
                    )
                    raise err

        return Cmd.from_cmd(_action)

    return TempReadOnlyFile.from_cmd(write_cmd)


def _ordered_data(record: CompletePlainRecord) -> FrozenList[Primitive]:
    def _key(item: Tuple[str, Primitive]) -> str:
        return item[0]

    items = tuple(record.record.record.items())
    ordered = sorted(items, key=_key)
    return tuple(i[1] for i in ordered)


def _is_datetime(schema: JsonValue) -> ResultE[bool]:
    def _inner(data: FrozenDict[str, Unfolder]) -> ResultE[bool]:
        _type = (
            Maybe.from_optional(data.get("type"))
            .to_result()
            .alt(lambda _: Exception("Missing `type` key"))
            .bind(lambda u: u.to_primitive(str).alt(Exception))
        )
        _format: ResultE[Maybe[str]] = (
            Maybe.from_optional(data.get("format"))
            .map(
                lambda u: u.to_primitive(str)
                .alt(lambda _: Exception("Expected `str` at `format` key"))
                .map(lambda x: Maybe.from_value(x))
            )
            .value_or(Result.success(Maybe.empty()))
        )
        return _type.bind(
            lambda t: _format.map(
                lambda f: t == "string" and f.value_or(None) == "date-time"
            )
        )

    return Unfolder(schema).to_unfolder_dict().alt(Exception).bind(_inner)


def _reformat_group_records(
    datetime_props: FrozenSet[str], record: CompletePlainRecord
) -> ResultE[CompletePlainRecord]:
    def _to_prim(item: str) -> Primitive:
        return item

    def _adjust(key: str, value: Primitive) -> ResultE[Primitive]:
        if key in datetime_props:
            return (
                to_opt_primitive(value, str)
                .map(
                    lambda x: _to_prim(
                        isoparse(x).strftime("%Y-%m-%d %H:%M:%S")
                    )
                    if x
                    else None
                )
                .alt(Exception)
            )
        return Result.success(value)

    _records = all_ok(
        pure_map(
            lambda p: _adjust(p[0], p[1]).map(lambda a: (p[0], a)),
            tuple(record.record.record.items()),
        ).transform(lambda x: tuple(x))
    ).map(lambda l: FrozenDict(dict(l)))
    return _records.bind(
        lambda r: CompletePlainRecord.new(
            record.schema, PlainRecord.new(record.schema.stream, r)
        )
    )


def _reformat_group(group: RecordGroup) -> RecordGroup:
    datetime_properties = (
        Maybe.from_optional(group.schema.schema.encode().get("properties"))
        .to_result()
        .alt(lambda _: Exception("Missing `properties` key"))
        .bind(lambda j: Unfolder(j).to_json().alt(Exception))
        .map(lambda d: tuple(d.items()))
        .map(
            lambda p: tuple(
                pure_map(
                    lambda i: _is_datetime(i[1]).map(lambda b: (i[0], b)), p
                )
            )
        )
        .bind(lambda x: all_ok(x).map(lambda y: from_flist(y)))
        .map(lambda p: p.filter(lambda t: t[1]).map(lambda x: x[0]))
        .map(lambda x: frozenset(x))
    )
    records = datetime_properties.map(
        lambda p: group.records.map(
            lambda c: _reformat_group_records(p, c).unwrap()
        )
    ).unwrap()
    return RecordGroup.new(group.schema, records)


def save(
    group: RecordGroup,
) -> Cmd[TempReadOnlyFile]:
    _group = _reformat_group(group)
    msg = _utils.log_cmd(
        lambda: LOG.info(
            "Saving stream `%s` data into temp", _group.schema.stream
        ),
        None,
    )
    return msg + _group.records.map(_ordered_data).transform(
        lambda x: _save(x)
    ).bind(
        lambda t: _utils.log_cmd(
            lambda: LOG.info(
                "Stream `%s` saved into temp file!", _group.schema.stream
            ),
            t,
        )
    )
