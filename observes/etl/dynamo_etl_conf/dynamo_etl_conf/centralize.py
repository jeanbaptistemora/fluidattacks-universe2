# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    Cmd,
    Maybe,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    from_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    consume,
    filter_maybe,
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
    TypeVar,
)

_T = TypeVar("_T")
LOG = logging.getLogger(__name__)


def _print(item: _T, msg: str) -> _T:
    LOG.info(msg)
    return item


def _exist(client: SchemaClient, schema: SchemaId) -> Cmd[Maybe[SchemaId]]:
    return client.exist(schema).map(
        lambda b: Maybe.from_optional(schema if b else None)
    )


def merge_parts(
    client: SchemaClient, schema_part_prefix: str, target: SchemaId
) -> Cmd[None]:
    schemas = (
        from_range(range(0, 10))
        .map(
            lambda i: _exist(
                client, SchemaId(f"{schema_part_prefix.lower()}{i}")
            )
        )
        .transform(lambda p: filter_maybe(from_piter(p)))
    )
    return consume(
        schemas.map(lambda s: _print(s, f"Moving {s} -> {target}")).map(
            lambda s: client.move(s, target)
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
    nothing = Cmd.from_cmd(lambda: None)
    return consume(
        schemas.map(
            lambda r: r.map(lambda s: _print(s, f"Migrating {s} -> {target}"))
            .map(lambda s: client.migrate(s, target))
            .alt(lambda s: _print(nothing, f"Ignoring non-existent {s}"))
            .to_union()
        )
    )
