# pylint: disable=invalid-name
"""
Remove credential from root if the credential does not exist

Execution Time:    2022-07-21 at 20:26:59 UTC
Finalization Time: 2022-07-21 at 20:28:29 UTC
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
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_root(root: Item, credentials_ids: set[str]) -> None:
    root_key = PrimaryKey(
        partition_key=root["pk"],
        sort_key=root["sk"],
    )
    root_credential_id: Optional[str] = root["state"].get("credential_id")
    if root_credential_id and root_credential_id not in credentials_ids:
        condition_expression = Attr(TABLE.primary_key.partition_key).exists()
        await operations.update_item(
            condition_expression=condition_expression,
            key=root_key,
            item={
                "state.credential_id": None,
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
    group_name: str,
    credentials_ids: set[str],
) -> None:
    roots = await _get_group_roots(group_name=group_name)
    await collect(
        tuple(process_root(root, credentials_ids) for root in roots),
        workers=10,
    )


async def process_organization(
    loaders: Dataloaders,
    organization_id: str,
    group_names: tuple[str, ...],
) -> None:
    org_credentials = await loaders.organization_credentials.load(
        organization_id
    )
    credentials_ids = set(credentials.id for credentials in org_credentials)
    await collect(
        process_group(group_name, credentials_ids)
        for group_name in group_names
    )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    count = 0
    async for org_id, org_name, org_groups_names in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        count += 1
        print(count, org_name)
        await process_organization(loaders, org_id, org_groups_names)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
