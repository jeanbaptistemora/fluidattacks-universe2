# pylint: disable=invalid-name
"""
Update the credential owner gsi with the new owner

Execution Time:    2022-06-21 at 16:45:59 UTC
Finalization Time: 2022-06-21 at 16:48:52 UTC
"""
from aioextensions import (
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
from db_model.credentials.constants import (
    OWNER_INDEX_FACET,
)
from db_model.credentials.types import (
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
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

Secret = HttpsSecret | HttpsPatSecret | SshSecret


async def check_and_update_owner_pk(item: Item) -> None:
    key_structure = TABLE.primary_key
    credential_key = keys.build_key(
        facet=TABLE.facets["credentials_new_metadata"],
        values={
            "organization_id": item["organization_id"],
            "id": item["id"],
        },
    )
    gsi_2_index = TABLE.indexes["gsi_2"]
    gsi_2_key = keys.build_key(
        facet=OWNER_INDEX_FACET,
        values={
            "owner": item["owner"],
            "id": item["id"],
        },
    )
    if item[gsi_2_index.primary_key.partition_key] != gsi_2_key.partition_key:
        credential_item = {
            gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key
        }
        await operations.update_item(
            condition_expression=(Attr(key_structure.partition_key).exists()),
            item=credential_item,
            key=credential_key,
            table=TABLE,
        )


async def process_organization_credentials(
    organization_id: str,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_new_metadata"],
        values={"organization_id": organization_id},
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
        facets=(TABLE.facets["credentials_new_metadata"],),
        index=index,
        table=TABLE,
    )
    for item in response.items:
        await check_and_update_owner_pk(item)


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    count = 0
    async for org_id, org_name, _ in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        count += 1
        print(count, org_name)
        await process_organization_credentials(org_id)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
