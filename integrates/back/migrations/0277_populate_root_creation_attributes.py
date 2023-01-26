# pylint: disable=invalid-name
"""
Populate the creation attributes for the roots

Execution Time:    2022-09-13 at 20:08:27 UTC
Finalization Time: 2022-09-13 at 20:09:04 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.roots.types import (
    Root,
    RootState,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
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


async def process_root(loaders: Dataloaders, root: Root) -> None:
    historic: tuple[RootState, ...] = await loaders.root_historic_states.load(
        root.id
    )
    creation_state: RootState = historic[0]
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": root.group_name, "uuid": root.id},
    )
    key_structure = TABLE.primary_key
    item = {
        "created_by": creation_state.modified_by,
        "created_date": creation_state.modified_date,
    }
    print("item", item)
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=primary_key,
        table=TABLE,
    )


async def get_group_roots(
    loaders: Dataloaders,
    group_name: str,
) -> list[Root]:
    return await loaders.group_roots.load(group_name)


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    all_organization_ids = {"ORG#unknown"}
    async for organization in orgs_domain.iterate_organizations():
        all_organization_ids.add(organization.id)

    all_group_names = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    orgs_domain.get_group_names(loaders, organization_id)
                    for organization_id in all_organization_ids
                ),
                workers=100,
            )
        )
    )
    all_roots = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    get_group_roots(loaders, group_name)
                    for group_name in all_group_names
                ),
                workers=100,
            )
        )
    )
    await collect(
        tuple(process_root(loaders, root) for root in all_roots),
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
