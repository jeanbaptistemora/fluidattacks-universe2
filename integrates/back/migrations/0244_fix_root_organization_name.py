# pylint: disable=invalid-name
"""
Fix root organization name since some roots has the organization id
as organization name

Execution Time:    2022-07-21 at 18:55:47 UTC
Finalization Time: 2022-07-21 at 18:57:27 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.roots.constants import (
    ORG_INDEX_METADATA,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_root(organization_name: str, root: Item) -> None:
    root_id = root["pk"].split("#")[1]
    root_key = PrimaryKey(
        partition_key=root["pk"],
        sort_key=root["sk"],
    )
    gsi_2_key = keys.build_key(
        facet=ORG_INDEX_METADATA,
        values={"name": organization_name, "uuid": root_id},
    )
    if (
        gsi_2_key.partition_key != root["pk_2"]
        or gsi_2_key.sort_key != root["sk_2"]
    ):
        condition_expression = Attr(TABLE.primary_key.partition_key).exists()
        await operations.update_item(
            condition_expression=condition_expression,
            key=root_key,
            item={
                "pk_2": gsi_2_key.partition_key,
                "sk_2": gsi_2_key.sort_key,
                "organization_name": organization_name,
            },
            table=TABLE,
        )


async def _get_group_roots(*, group_name: str) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["git_root_metadata"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["url_root_metadata"],
        ),
        index=index,
        table=TABLE,
    )
    return response.items


async def process_group(
    organization_name: str,
    group_name: str,
) -> None:
    roots = await _get_group_roots(group_name=group_name)
    await collect(
        tuple(process_root(organization_name, root) for root in roots),
        workers=10,
    )


async def process_organization(
    organization_name: str,
    group_names: tuple[str, ...],
) -> None:
    await collect(
        process_group(organization_name, group_name)
        for group_name in group_names
    )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    count = 0
    async for _, org_name, org_groups_names in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        count += 1
        print(count, org_name)
        await process_organization(org_name, org_groups_names)  # type: ignore


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
