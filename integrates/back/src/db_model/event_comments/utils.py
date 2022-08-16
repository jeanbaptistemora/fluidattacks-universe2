from db_model.event_comments.types import (
    EventComment,
)
from dynamodb.types import (
    Item,
)


def format_event_comments(item: Item) -> EventComment:
    return EventComment(
        event_id=item["event_id"],
        id=item["id"],
        parent_id=item["parent_id"],
        creation_date=item["creation_date"],
        full_name=item.get("full_name"),
        content=item["content"],
        email=item["email"],
    )
