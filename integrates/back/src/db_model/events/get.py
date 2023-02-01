from .types import (
    Event,
    EventState,
    GroupEventsRequest,
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
from db_model import (
    TABLE,
)
from db_model.events.constants import (
    GSI_2_FACET,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
    Optional,
)


async def _get_event(*, event_id: str) -> Optional[Event]:
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
        return None

    return format_event(response.items[0])


async def _get_group_events(
    *,
    event_dataloader: DataLoader,
    request: GroupEventsRequest,
) -> list[Event]:
    if request.is_solved is None:
        facet = TABLE.facets["event_metadata"]
        primary_key = keys.build_key(
            facet=facet,
            values={"name": request.group_name},
        )
        index = TABLE.indexes["inverted_index"]
        key_structure = index.primary_key
        condition_expression = Key(key_structure.partition_key).eq(
            primary_key.sort_key
        ) & Key(key_structure.sort_key).begins_with(primary_key.partition_key)
    else:
        facet = GSI_2_FACET
        primary_key = keys.build_key(
            facet=facet,
            values={
                "group_name": request.group_name,
                "is_solved": str(request.is_solved).lower(),
            },
        )
        index = TABLE.indexes["gsi_2"]
        key_structure = index.primary_key
        condition_expression = Key(key_structure.partition_key).eq(
            primary_key.partition_key
        ) & Key(key_structure.sort_key).begins_with(primary_key.sort_key)

    response = await operations.query(
        condition_expression=condition_expression,
        facets=(TABLE.facets["event_metadata"],),
        table=TABLE,
        index=index,
    )

    events: list[Event] = []
    for item in response.items:
        event = format_event(item)
        events.append(event)
        event_dataloader.prime(event.id, event)

    return events


async def _get_historic_state(
    *,
    event_id: str,
) -> list[EventState]:
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
    return list(map(format_state, response.items))


class EventsHistoricStateLoader(DataLoader[str, list[EventState]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, event_ids: Iterable[str]
    ) -> list[list[EventState]]:
        return list(
            await collect(
                tuple(
                    _get_historic_state(event_id=event_id)
                    for event_id in event_ids
                )
            )
        )


class EventLoader(DataLoader[str, Optional[Event]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        event_keys: Iterable[str],
    ) -> list[Optional[Event]]:
        return list(
            await collect(
                tuple(_get_event(event_id=event_id) for event_id in event_keys)
            )
        )


class GroupEventsLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[GroupEventsRequest]
    ) -> list[list[Event]]:
        return list(
            await collect(
                _get_group_events(
                    event_dataloader=self.dataloader,
                    request=request,
                )
                for request in requests
            )
        )
