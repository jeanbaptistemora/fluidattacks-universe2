# pylint: disable=invalid-name
"""
Get the events that needs to change their taxonomy

Execution Time:    2022-08-10 at 21:45:53 UTC
Finalization Time: 2022-08-10 at 21:46:02 UTC
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


async def process_group(loaders: Dataloaders, group_name: str) -> list[Event]:
    return await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )


async def main() -> None:  # noqa: MC0001
    loaders = get_new_context()
    with open(
        "Historico Eventualidades - -Report1-2022-07-05-01 53-final.csv",
        mode="r",
        encoding="utf8",
    ) as in_file:
        reader = csv.reader(in_file)
        migrated_event_ids = {
            str(rows[0]).strip()
            for rows in reader
            if rows[0] != "event_id_str"  # Skip header
        }

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
        "description",
        "event_type",
        "new_event_type",
    ]
    csv_file = "0258_get_events_to_change_taxonomy.csv"
    try:
        with open(csv_file, "w", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for event in all_events:
                if event.id not in migrated_event_ids:
                    writer.writerow(
                        {
                            "event_id": event.id,
                            "group_name": event.group_name,
                            "description": event.description,
                            "event_type": event.type,
                            "new_event_type": None,
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
