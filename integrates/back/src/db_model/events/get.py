from .types import (
    Event,
)
from .utils import (
    format_event,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    EventNotFound,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_event(*, event_id: str, group_name: str) -> Event:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={
            "id": event_id,
            "name": group_name,
        },
    )
    item = await operations.get_item(
        facets=(TABLE.facets["event_metadata"],),
        key=primary_key,
        table=TABLE,
    )
    if not item:
        raise EventNotFound()

    return format_event(item)


class EventLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self,
        event_keys: Iterable[tuple[str, str]],
    ) -> tuple[Event, ...]:
        # This loaders receives a tuple with (group_name, event_id)
        return await collect(
            tuple(
                _get_event(event_id=event_id, group_name=group_name)
                for group_name, event_id in event_keys
            )
        )
