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
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
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
    Tuple,
)


def _to_columns(properties: JsonObj) -> FrozenList[Tuple[ColumnId, Column]]:
    return tuple(
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


def extract_table(schema: SingerSchema) -> ResultE[Table]:
    schema.key_properties
    properties = (
        opt_transform(
            schema.schema.encode(), "properties", lambda u: u.to_json()
        )
        .to_result()
        .alt(lambda _: Exception("Missing properties"))
        .bind(lambda b: b.alt(Exception))
    )
    return properties.map(_to_columns).bind(
        lambda columns: new_table(
            tuple(c[0] for c in columns),
            FrozenDict(dict(columns)),
            frozenset(ColumnId(pk) for pk in schema.key_properties),
        )
    )
