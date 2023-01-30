# pylint: disable=invalid-name
"""
Retrieve all solved events
Execution Time:    2022-08-09 at 20∶58∶27 UTC
Finalization Time: 2022-08-09 at 20∶58∶27 UTC
"""
from aioextensions import (
    collect,
    run,
)
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
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


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> list[Event]:
    return await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name, is_solved=True)
    )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    all_group_names = set()
    async for _, _, org_groups_names in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        all_group_names.update(set(org_groups_names))

    all_events = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    process_group(loaders, group_name)
                    for group_name in all_group_names
                ),
                workers=100,
            )
        )
    )

    csv_columns = [
        "event_id",
        "group_name",
        "status",
        "description",
        "solving_reason",
        "other_solving_reason",
    ]
    csv_file = "0256_get_solved_events.csv"
    try:
        with open(csv_file, "w", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for event in all_events:
                writer.writerow(
                    {
                        "event_id": event.id,
                        "group_name": event.group_name,
                        "status": event.state.status.value,
                        "description": event.description,
                        "solving_reason": event.state.reason.value
                        if event.state.reason
                        else None,
                        "other_solving_reason": event.state.other,
                    }
                )
    except IOError:
        print("   === I/O error")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
