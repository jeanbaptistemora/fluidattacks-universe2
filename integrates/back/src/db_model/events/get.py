from .types import (
    Event,
    EventState,
)
from .utils import (
    format_event,
    format_state,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
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


async def _get_event(*, event_id: str) -> Event:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={"id": event_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["event_metadata"],),
        limit=1,
        table=TABLE,
    )

    if not response.items:
        raise EventNotFound()

    return format_event(response.items[0])


async def _get_group_events(
    group_name: str,
) -> tuple[Event, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={"name": group_name},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["event_metadata"],),
        table=TABLE,
        index=index,
    )

    return tuple(format_event(item) for item in response.items)


async def _get_historic_state(
    *,
    event_id: str,
) -> tuple[EventState, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_historic_state"],
        values={"id": event_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["event_historic_state"],),
        table=TABLE,
    )
    return tuple(map(format_state, response.items))


class EventsHistoricStateLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, event_ids: Iterable[str]
    ) -> tuple[tuple[Event, ...], ...]:
        return await collect(
            tuple(
                _get_historic_state(event_id=event_id)
                for event_id in event_ids
            )
        )


class EventLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self,
        event_keys: Iterable[str],
    ) -> tuple[Event, ...]:
        return await collect(
            tuple(_get_event(event_id=event_id) for event_id in event_keys)
        )


class GroupEventsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[tuple[Event, ...], ...]:
        return await collect(tuple(map(_get_group_events, group_names)))
