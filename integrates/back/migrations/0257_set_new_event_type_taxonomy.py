# pylint: disable=invalid-name
"""
Set the new event taxonomy for the old events

Execution Time:    2022-08-10 at 20:02:20 UTC
Finalization Time: 2022-08-10 at 20:02:32 UTC
"""
from aioextensions import (
    collect,
    run,
)
import csv
from custom_exceptions import (
    EventNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    events as events_model,
)
from db_model.events.enums import (
    EventType,
)
from db_model.events.types import (
    Event,
    EventMetadataToUpdate,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_event(
    loaders: Dataloaders, event_data: dict[str, str]
) -> None:
    try:
        event: Optional[Event] = await loaders.event.load(
            event_data["event_id"]
        )
    except EventNotFound:
        event = None
    if event:
        print(event)
        await events_model.update_metadata(
            event_id=event.id,
            group_name=event.group_name,
            metadata=EventMetadataToUpdate(
                type=EventType[event_data["new_event_type"]],
                clean_affected_components=True,
            ),
        )


async def main() -> None:  # noqa: MC0001
    loader = get_new_context()
    with open(
        "Historico Eventualidades - -Report1-2022-07-05-01 53-final.csv",
        mode="r",
        encoding="utf8",
    ) as in_file:
        reader = csv.reader(in_file)
        new_data = [
            {
                "event_id": str(rows[0]).strip(),
                "group_name": rows[1],
                "current_event_type": rows[3],
                "new_event_type": str(rows[4]).strip(),
            }
            for rows in reader
            if rows[0] != "event_id_str"  # Skip header
        ]

    print(f"   === events to update: {len(new_data)}")
    print(f"   === sample: {new_data[:3]}")

    await collect(
        tuple(process_event(loader, event_data) for event_data in new_data),
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
