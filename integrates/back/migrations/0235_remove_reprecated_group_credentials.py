# pylint: disable=invalid-name
"""
Remove deprecated group credentials

Execution Time:    2022-06-29 at 21:50:42 UTC
Finalization Time: 2022-06-29 at 22:23:03 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from collections import (
    defaultdict,
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
from more_itertools import (
    chunked,
)
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


async def remove_historic(credentials_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_historic_state"],
        values={"uuid": credentials_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["credentials_historic_state"],),
        table=TABLE,
    )
    await collect(
        tuple(
            operations.batch_delete_item(
                keys=tuple(
                    PrimaryKey(
                        partition_key=item[TABLE.primary_key.partition_key],
                        sort_key=item[TABLE.primary_key.sort_key],
                    )
                    for item in chunked_items
                ),
                table=TABLE,
            )
            for chunked_items in chunked(response.items, 20)
        ),
        workers=100,
    )


async def get_credentials_items(
    *, group_name: str
) -> defaultdict[str, list[Item]]:
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
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
            TABLE.facets["credentials_historic_state"],
            TABLE.facets["credentials_metadata"],
            TABLE.facets["credentials_state"],
        ),
        index=index,
        table=TABLE,
    )
    credential_items = defaultdict(list)
    for item in response.items:
        credential_id = item[key_structure.sort_key].split("#")[1]
        credential_items[credential_id].append(item)

    return credential_items


async def get_removed_credentials_items(
    *, group_name: str
) -> defaultdict[str, list[Item]]:
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
        values={"name": group_name},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                f"REMOVED#{primary_key.partition_key}"
            )
        ),
        facets=(
            TABLE.facets["credentials_historic_state"],
            TABLE.facets["credentials_metadata"],
            TABLE.facets["credentials_state"],
        ),
        index=index,
        table=TABLE,
    )
    credential_items = defaultdict(list)
    for item in response.items:
        credential_id = item[key_structure.sort_key].split("#")[2]
        credential_items[credential_id].append(item)

    return credential_items


async def process_organization(
    group_names: tuple[str, ...],
) -> None:
    for group_name in group_names:
        credentials_items = await get_credentials_items(group_name=group_name)
        removed_credentials_items = await get_removed_credentials_items(
            group_name=group_name
        )
        for credentials_id, items in tuple(
            list(credentials_items.items())
            + list(removed_credentials_items.items())
        ):
            await remove_historic(credentials_id)
            await collect(
                tuple(
                    operations.batch_delete_item(
                        keys=tuple(
                            PrimaryKey(
                                partition_key=item[
                                    TABLE.primary_key.partition_key
                                ],
                                sort_key=item[TABLE.primary_key.sort_key],
                            )
                            for item in chunked_items
                        ),
                        table=TABLE,
                    )
                    for chunked_items in chunked(items, 20)
                ),
                workers=100,
            )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    count = 0
    async for _, org_name, org_groups_names in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        count += 1
        print(count, org_name)
        await process_organization(org_groups_names)  # type: ignore


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
