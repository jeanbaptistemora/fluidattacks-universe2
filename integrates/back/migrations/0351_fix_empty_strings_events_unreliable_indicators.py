# pylint: disable=invalid-name
"""
Refresh events unreliable_indicators when an empty string is in an
attribute that would hold a date. These empty strings are causing an
indexation error in opensearch. The attribute will be removed instead.

Execution Time:    2023-01-13 at 16:46:06 UTC
Finalization Time: 2023-01-13 at 16:54:40 UTC
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
    events as events_model,
    TABLE,
)
from db_model.events.types import (
    EventUnreliableIndicatorsToUpdate,
)
from db_model.events.utils import (
    format_event,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def get_group_event_items(group_name: str) -> tuple[Item, ...]:
    facet = TABLE.facets["event_metadata"]
    primary_key = keys.build_key(
        facet=facet,
        values={"name": group_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.sort_key
    ) & Key(key_structure.sort_key).begins_with(primary_key.partition_key)

    response = await operations.query(
        condition_expression=condition_expression,
        facets=(TABLE.facets["event_metadata"],),
        table=TABLE,
        index=index,
    )

    return response.items


async def process_event(event: Item) -> None:
    indicators: Item = event["unreliable_indicators"]
    if not indicators:
        return
    if indicators.get("unreliable_solving_date") == "":
        await events_model.update_unreliable_indicators(
            current_value=format_event(event),
            indicators=EventUnreliableIndicatorsToUpdate(
                clean_unreliable_solving_date=True,
            ),
        )
        print(f"Event updated {event.get('id')=}")


async def process_group(
    group_name: str,
    progress: float,
) -> None:
    group_events: tuple[Item, ...] = await get_group_event_items(group_name)
    await collect(
        tuple(process_event(event) for event in group_events),
        workers=1,
    )
    print(
        f"Processed {group_name=}, {len(group_events)=}, "
        f"progress: {round(progress, 2)}"
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    print(f"{len(group_names)=}")
    await collect(
        tuple(
            process_group(
                group_name=group_name,
                progress=count / len(group_names),
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=1,
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
