# pylint: disable=invalid-name
"""
Populate the unreliable solving date indicator for all the events

Execution Time:    2022-07-08 at 20:19:40 UTC
Finalization Time: 2022-07-08 at 20:22:34 UTC

Execution Time:    2022-07-13 at 14:37:19 UTC
Finalization Time: 2022-07-13 at 14:39:49 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.types import (
    Event,
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
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_event(event: Event) -> None:
    # solve event is dependency of solving date
    await update_unreliable_indicators_by_deps(
        EntityDependency.solve_event,
        event_ids=[event.id],
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    events = await loaders.group_events.load(group_name)  # type: ignore
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
