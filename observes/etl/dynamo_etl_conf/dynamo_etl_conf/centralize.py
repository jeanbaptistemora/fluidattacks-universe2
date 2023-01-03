from ._utils import (
    log_info,
)
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
    until_empty,
)
import logging
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from typing import (
    FrozenSet,
)

LOG = logging.getLogger(__name__)


def _exist(client: SchemaClient, schema: SchemaId) -> Cmd[Maybe[SchemaId]]:
    return client.exist(schema).map(
        lambda b: Maybe.from_optional(schema if b else None)
    )


def merge_parts(
    client: SchemaClient, schema_part_prefix: str, target: SchemaId
) -> Cmd[None]:
    schemas = (
        infinite_range(0, 1)
        .map(
            lambda i: _exist(
                client, SchemaId(f"{schema_part_prefix.lower()}{i}")
            )
        )
        .transform(lambda p: until_empty(from_piter(p)))
    )
    return consume(
        schemas.map(
            lambda s: log_info(LOG, "Moving %s -> %s", str(s), str(target))
            + client.move(s, target)
        )
    )


def merge_dynamo_tables(
    client: SchemaClient, tables: FrozenSet[str], target: SchemaId
) -> Cmd[None]:
    schemas = (
        from_flist(tuple(tables))
        .map(lambda table: SchemaId(f"dynamodb_{table.lower()}"))
        .map(
            lambda s: _exist(client, s).map(
                lambda m: m.to_result().alt(lambda _: s)
            )
        )
        .transform(lambda p: from_piter(p))
    )
    return consume(
        schemas.map(
            lambda r: r.map(
                lambda s: log_info(
                    LOG, "Migrating %s -> %s", str(s), str(target)
                )
                + client.migrate(s, target)
            )
            .alt(lambda s: log_info(LOG, "Ignoring non-existent %s", str(s)))
            .to_union()
        )
    )
