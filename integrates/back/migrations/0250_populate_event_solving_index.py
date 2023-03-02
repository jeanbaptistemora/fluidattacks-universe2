# pylint: disable=invalid-name
"""
Populate the solving index in the events

Execution Time:    2022-08-02 at 15:12:48 UTC
Finalization Time: 2022-08-02 at 15:14:28 UTC
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
from db_model.events.constants import (
    GSI_2_FACET,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from dynamodb import (
    keys,
    operations,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def process_event(event: Event) -> None:
    gsi_2_index = TABLE.indexes["gsi_2"]
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={
            "id": event.id,
            "name": event.group_name,
        },
    )
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "is_solved": str(
                event.state.status is EventStateStatus.SOLVED
            ).lower(),
            "group_name": event.group_name,
        },
    )
    item = {
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
    }
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=primary_key,
        table=TABLE,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    await collect(tuple(process_event(event) for event in events), workers=30)


async def process_organization(
    loaders: Dataloaders, group_names: tuple[str, ...]
) -> None:
    await collect(
        tuple(
            process_group(loaders, group_name) for group_name in group_names
        ),
        workers=3,
    )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    count = 0
    async for _, org_name, group_names in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        count += 1
        print(count, org_name)
        await process_organization(loaders, group_names)  # type: ignore


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
