# type: ignore

# pylint: disable=invalid-name
"""
Remove the states with closed status for all the events

Execution Time:    2022-07-08 at 14:30:24 UTC
Finalization Time: 2022-07-08 at 14:43:57 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
    EventState,
)
from dynamodb import (
    keys,
    operations,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
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


async def remove_state(
    event_id: str,
    state: EventState,
) -> None:
    historic_state_key = keys.build_key(
        facet=TABLE.facets["event_historic_state"],
        values={
            "id": event_id,
            "iso8601utc": datetime_utils.get_as_utc_iso_format(
                state.modified_date
            ),
        },
    )
    await operations.delete_item(key=historic_state_key, table=TABLE)


async def process_event(loaders: Dataloaders, event: Event) -> None:
    historic_states = await loaders.event_historic_state.load(event.id)
    for state in historic_states:
        if state.status == EventStateStatus.CLOSED:
            await remove_state(event.id, state)


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    events = await loaders.group_events.load(group_name)
    await collect(
        tuple(process_event(loaders, event) for event in events), workers=30
    )


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
        await process_organization(loaders, group_names)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
