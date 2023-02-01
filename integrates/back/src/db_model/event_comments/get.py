from .types import (
    EventComment,
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
from db_model.event_comments.utils import (
    format_event_comments,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_comments(*, event_id: str) -> list[EventComment]:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_comment"],
        values={"event_id": event_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.sort_key).eq(primary_key.sort_key)
            & Key(key_structure.partition_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["event_comment"],),
        index=TABLE.indexes["inverted_index"],
        table=TABLE,
    )

    return [format_event_comments(item) for item in response.items]


class EventCommentsLoader(DataLoader[str, list[EventComment]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, events_ids: Iterable[str]
    ) -> list[list[EventComment]]:
        return list(
            await collect(
                tuple(
                    _get_comments(event_id=event_id) for event_id in events_ids
                )
            )
        )
