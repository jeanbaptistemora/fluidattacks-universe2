from ._data_types import (
    jschema_type_handler,
)
from ._utils import (
    opt_transform,
)
from fa_purity import (
    FrozenDict,
    FrozenList,
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
from redshift_client.column import (
    Column,
    ColumnId,
)
from redshift_client.table.core import (
    new as new_table,
    Table,
)
from typing import (
    FrozenSet,
    Tuple,
)


def _to_columns(properties: JsonObj) -> PureIter[Tuple[ColumnId, Column]]:
    result = tuple(
        (
            ColumnId(name),
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
    column: Tuple[ColumnId, Column], required: FrozenSet[ColumnId]
) -> Tuple[ColumnId, Column]:
    if column[0] not in required:
        return (column[0], Column(column[1].data_type, True, None))
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
        .map(lambda l: frozenset(ColumnId(i) for i in l)),
    ).value_or(Result.success(frozenset()))
    return (
        properties.map(_to_columns)
        .bind(
            lambda c: required.map(
                lambda req: c.map(lambda g: _set_nullable(g, req))
            )
        )
        .bind(
            lambda columns: new_table(
                tuple(c[0] for c in columns),
                FrozenDict(dict(columns)),
                frozenset(ColumnId(pk) for pk in schema.key_properties),
            )
        )
    )
