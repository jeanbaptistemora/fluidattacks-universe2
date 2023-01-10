from ._utils import (
    log_info,
)
from dynamo_etl_conf import (
    _utils,
    jobs_sdk,
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


def main(
    client: SchemaClient,
    tables: FrozenSet[str],
    parts_schema_prefix: str,
    loading_schema: SchemaId,
    pre_merge_schema: SchemaId,
    schema: SchemaId,
) -> Cmd[None]:
    return (
        _utils.log_info(LOG, "Preparing loading schema...")
        + jobs_sdk.prepare_loading(
            loading_schema, "s3://observes.cache/dynamoEtl/vms_schema"
        )
        + _utils.log_info(LOG, "Merging schema parts...")
        + merge_parts(client, parts_schema_prefix, loading_schema)
        + _utils.log_info(LOG, "Renaming...")
        + client.rename(loading_schema, pre_merge_schema)
        + _utils.log_info(LOG, "Migrating data...")
        + merge_dynamo_tables(client, tables, schema)
    )
