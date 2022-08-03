from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from db_model.event_comments.types import (
    EventComment,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from dynamodb.types import (
    Item,
)
from newutils.event_comments import (
    format_event_comments,
)
from typing import (
    Iterable,
)

TABLE_NAME: str = "fi_finding_comments"


async def get_comments(event_id: str) -> list[Item]:
    """Get comments of the given finding"""
    key_exp = Key("finding_id").eq(event_id)
    filter_exp = Attr("comment_type").eq("event")
    query_attrs = {
        "KeyConditionExpression": key_exp,
        "FilterExpression": filter_exp,
    }
    return await dynamodb_ops.query(TABLE_NAME, query_attrs)


class EventCommentsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[str]
    ) -> tuple[tuple[EventComment, ...], ...]:
        items = await collect(
            tuple((get_comments(event_id=event_id) for event_id in keys))
        )
        return tuple(
            tuple(format_event_comments(item=item) for item in lst)
            for lst in items
        )
