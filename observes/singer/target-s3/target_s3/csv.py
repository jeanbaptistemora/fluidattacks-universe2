# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _utils,
)
import csv
from dataclasses import (
    dataclass,
)
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
    Callable,
    FrozenSet,
    Generic,
    IO,
    Tuple,
    TypeVar,
)

_T = TypeVar("_T")
LOG = logging.getLogger(__name__)


def _truncate_row(
    row: FrozenList[Primitive], _limit: int
) -> FrozenList[Primitive]:
    limit = _limit if _limit >= -1 else -1

    def _truncate(prim: Primitive) -> Primitive:
        if isinstance(prim, str):
            return prim[0:limit] if limit >= 0 else prim
        return prim

    return tuple(_truncate(r) for r in row)


def _save(
    data: PureIter[FrozenList[Primitive]], str_limit: int
) -> Cmd[TempReadOnlyFile]:
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
            for _row in data:
                row = _truncate_row(_row, str_limit)
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


def _save_group(
    group: RecordGroup,
    str_limit: int,
) -> Cmd[TempReadOnlyFile]:
    _group = _reformat_group(group)
    msg = _utils.log_cmd(
        lambda: LOG.info(
            "Saving stream `%s` data into temp", _group.schema.stream
        ),
        None,
    )
    return msg + _group.records.map(_ordered_data).transform(
        lambda x: _save(x, str_limit)
    ).bind(
        lambda t: _utils.log_cmd(
            lambda: LOG.info(
                "Stream `%s` saved into temp file!", _group.schema.stream
            ),
            t,
        )
    )


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


@dataclass(frozen=True)
class CsvKeeper:
    _save: _Patch[Callable[[RecordGroup], Cmd[TempReadOnlyFile]]]

    def save(self, group: RecordGroup) -> Cmd[TempReadOnlyFile]:
        return self._save.inner(group)


@dataclass(frozen=True)
class CsvKeeperFactory:
    str_limit: int

    def _save(self, group: RecordGroup) -> Cmd[TempReadOnlyFile]:
        return _save_group(group, self.str_limit)

    @staticmethod
    def new(str_limit: int) -> CsvKeeper:
        return CsvKeeper(_Patch(CsvKeeperFactory(str_limit)._save))
