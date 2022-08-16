from db_model.event_comments.types import (
    EventComment,
)
from dynamodb.types import (
    Item,
)
from newutils.datetime import (
    convert_from_iso_str,
    convert_to_iso_str,
    format_comment_date,
)


def _get_fullname(objective_data: EventComment) -> str:
    objective_email = objective_data.email
    objective_possible_fullname = (
        objective_data.full_name if objective_data.full_name else None
    )
    real_name = objective_possible_fullname or objective_email

    if "@fluidattacks.com" in objective_email:
        return f"{real_name} at Fluid Attacks"

    return real_name


def format_event_comments(item: Item) -> EventComment:
    return EventComment(
        event_id=item["finding_id"],
        id=str(item["comment_id"]),
        parent_id=str(item["parent"]),
        creation_date=convert_to_iso_str(item["created"]),
        full_name=item.get("fullname", None),
        content=item["content"],
        email=item["email"],
    )


def format_event_consulting_resolve(event_comment: EventComment) -> Item:
    fullname = _get_fullname(objective_data=event_comment)
    return {
        "content": event_comment.content,
        "created": format_comment_date(
            convert_from_iso_str(event_comment.creation_date)
        ),
        "email": event_comment.email,
        "fullname": fullname if fullname else event_comment.email,
        "id": event_comment.id,
        "modified": format_comment_date(
            convert_from_iso_str(event_comment.creation_date)
        ),
        "parent": event_comment.parent_id,
    }


def format_event_comment_item(event_comment: EventComment) -> Item:
    item = {
        "finding_id": event_comment.event_id,
        "comment_id": int(event_comment.id),
        "parent": event_comment.parent_id,
        "comment_type": "event",
        "created": convert_from_iso_str(event_comment.creation_date),
        "fullname": event_comment.full_name,
        "content": event_comment.content,
        "email": event_comment.email,
        "modified": convert_from_iso_str(event_comment.creation_date),
    }
    return {
        key: None if not value else value
        for key, value in item.items()
        if value is not None
    }
