# pylint: disable=invalid-name
"""
Migrate events metadata to "integrates_vms" table.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model import (
    events as events_model,
    TABLE,
)
from db_model.events.types import (
    Event,
    EventState,
)
from dynamodb import (
    keys,
    operations,
    operations_legacy as ops_legacy,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils import (
    events as events_utils,
)
from settings import (
    LOGGING,
)
import simplejson as json  # type: ignore
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
EVENTS_TABLE = "fi_events"


def adjust_historic_dates(
    historic: tuple[EventState, ...],
) -> tuple[EventState, ...]:
    """Ensure dates are not the same and in ascending order."""
    new_historic = []
    comparison_date = ""
    for entry in historic:
        if entry.modified_date > comparison_date:
            comparison_date = entry.modified_date
        else:
            fixed_date = datetime.fromisoformat(comparison_date) + timedelta(
                seconds=1
            )
            comparison_date = fixed_date.astimezone(
                tz=timezone.utc
            ).isoformat()
        new_historic.append(entry._replace(modified_date=comparison_date))
    return tuple(new_historic)


async def update_historic_state(
    event_id: str, historic: tuple[EventState, ...]
) -> None:
    key_structure = TABLE.primary_key
    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["event_historic_state"],
            values={
                "id": event_id,
                "iso8601utc": entry.modified_date,
            },
        )
        for entry in historic
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(entry)),
        }
        for key, entry in zip(new_keys, historic)
    )
    await operations.batch_put_item(items=new_items, table=TABLE)


async def process_event(item: Item) -> None:
    event: Event = events_utils.format_event(item)
    historic_state = adjust_historic_dates(
        events_utils.format_historic_state(item)
    )
    await update_historic_state(event.id, historic_state)
    await events_model.add(event=event)


async def main() -> None:
    events_scanned: list[Item] = await ops_legacy.scan(
        table=EVENTS_TABLE, scan_attrs={}
    )
    LOGGER_CONSOLE.info(
        "All events", extra={"extra": {"scanned": len(events_scanned)}}
    )

    await collect(process_event(item) for item in events_scanned)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
