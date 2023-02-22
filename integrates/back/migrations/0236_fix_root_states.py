# type: ignore

# pylint: disable=invalid-name
"""
Properly serialize state as dict

Execution Time:    2022-06-30 at 22:26:55 UTC
Finalization Time: 2022-06-30 at 22:28:33 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
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
from db_model.roots.types import (
    GitRootState,
    Root,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
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
import simplejson as json
import time
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _get_organization_roots(organization_name: str) -> tuple[Root, ...]:
    primary_key = keys.build_key(
        facet=ORG_INDEX_METADATA,
        values={"name": organization_name},
    )

    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
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


async def process_root(item: dict[str, Any]) -> None:
    pk = item["pk"]
    sk = item["sk"]
    del item["pk"]
    del item["sk"]
    print("Updating", pk, sk)
    state = GitRootState(*item["state"])
    print(state)
    await operations.update_item(
        item={**item, "state": json.loads(json.dumps(state))},
        key=PrimaryKey(pk, sk),
        table=TABLE,
    )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()

    async for _, org_name, _ in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        print("Working on", org_name)
        roots = await _get_organization_roots(org_name)

        await collect(
            (
                process_root(root)
                for root in roots
                if isinstance(root["state"], list)
            ),
            workers=100,
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
