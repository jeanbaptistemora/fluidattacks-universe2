from fa_purity import (
    Cmd,
    Maybe,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    consume,
    filter_maybe,
    until_empty,
)
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from typing import (
    FrozenSet,
)


def _exist(client: SchemaClient, schema: SchemaId) -> Cmd[Maybe[SchemaId]]:
    return client.exist(schema).map(
        lambda b: Maybe.from_optional(schema if b else None)
    )


def merge_parts(
    client: SchemaClient, schema_part_prefix: str, target: SchemaId
) -> Cmd[None]:
    schemas = (
        infinite_range(0, 1)
        .map(lambda i: _exist(client, SchemaId(f"{schema_part_prefix}{i}")))
        .transform(lambda p: until_empty(from_piter(p)))
    )
    return consume(schemas.map(lambda s: client.move(s, target)))


def merge_dynamo_tables(
    client: SchemaClient, tables: FrozenSet[str], target: SchemaId
) -> Cmd[None]:
    schemas = (
        from_flist(tuple(tables))
        .map(lambda table: _exist(client, SchemaId(f"dynamodb_{table}")))
        .transform(lambda p: filter_maybe(from_piter(p)))
    )
    return consume(schemas.map(lambda s: client.migrate(s, target)))
