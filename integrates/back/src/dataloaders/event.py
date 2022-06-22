from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from db_model.events.types import (
    Event,
    EventState,
)
from dynamodb.types import (
    Item,
)
from events import (
    dal as events_dal,
)
from newutils.events import (
    adjust_historic_dates,
    format_event,
    format_historic_state,
)
from typing import (
    Iterable,
)


async def _get_group_events(group_name: str) -> tuple[Event, ...]:
    event_ids = await events_dal.list_group_events(group_name)
    event_items = await collect(events_dal.get_event(id) for id in event_ids)
    return tuple(format_event(item) for item in event_items)


class EventsHistoricStateTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, event_ids: Iterable[str]
    ) -> tuple[tuple[EventState, ...], ...]:
        event_items: list[Item] = [
            await events_dal.get_event(id) for id in event_ids
        ]
        return tuple(
            adjust_historic_dates(format_historic_state(item))
            for item in event_items
        )


class EventTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, event_ids: Iterable[str]
    ) -> tuple[Event, ...]:
        event_items: list[Item] = [
            await events_dal.get_event(id) for id in event_ids
        ]
        return tuple(format_event(item) for item in event_items)


class GroupEventsTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[Event, ...]:
        return await collect(
            _get_group_events(group_name) for group_name in group_names
        )
