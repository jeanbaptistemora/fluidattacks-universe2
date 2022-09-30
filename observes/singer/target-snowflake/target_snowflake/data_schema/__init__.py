# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._data_types import (
    jschema_type_handler,
)
from ._utils import (
    opt_transform,
)
from fa_purity import (
    FrozenDict,
    JsonObj,
    PureIter,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_singer_io.singer import (
    SingerSchema,
)
from target_snowflake.snowflake_client.column import (
    Column,
)
from target_snowflake.snowflake_client.sql_client import (
    Identifier,
)
from target_snowflake.snowflake_client.table import (
    ColumnId,
    ColumnObj,
    Table,
)
from typing import (
    FrozenSet,
)


def _to_columns(properties: JsonObj) -> PureIter[ColumnObj]:
    result = tuple(
        ColumnObj(
            ColumnId(Identifier.from_raw(name)),
            Unfolder(data_type)
            .to_json()
            .alt(Exception)
            .bind(jschema_type_handler)
            .unwrap(),
        )
        for name, data_type in properties.items()
    )
    return from_flist(result)


def _set_nullable(
    column: ColumnObj, required: FrozenSet[ColumnId]
) -> ColumnObj:
    if column.id_obj not in required:
        return ColumnObj(
            column.id_obj, Column(column.column.data_type, True, None)
        )
    return column


def extract_table(schema: SingerSchema) -> ResultE[Table]:
    encoded = schema.schema.encode()
    properties = (
        opt_transform(encoded, "properties", lambda u: u.to_json())
        .to_result()
        .alt(lambda _: Exception("Missing properties"))
        .bind(lambda b: b.alt(Exception))
    )
    required: ResultE[FrozenSet[ColumnId]] = opt_transform(
        encoded,
        "required",
        lambda t: t.to_list_of(str)
        .alt(Exception)
        .map(lambda l: frozenset(ColumnId(Identifier.from_raw(i)) for i in l)),
    ).value_or(Result.success(frozenset()))
    return (
        properties.map(_to_columns)
        .bind(
            lambda c: required.map(
                lambda req: c.map(lambda g: _set_nullable(g, req))
            )
        )
        .bind(
            lambda columns: Table.new(
                tuple(c.id_obj for c in columns),
                FrozenDict(dict(columns.map(lambda o: (o.id_obj, o.column)))),
                frozenset(
                    ColumnId(Identifier.from_raw(pk))
                    for pk in schema.key_properties
                ),
            )
        )
    )
