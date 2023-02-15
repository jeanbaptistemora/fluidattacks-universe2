from db_model.event_comments.types import (
    EventComment,
)
from dynamodb.types import (
    Item,
)
from newutils.datetime import (
    format_comment_datetime,
)
from newutils.validations import (
    is_fluid_staff,
)


def _get_email(objective_data: EventComment) -> str:
    objective_email = objective_data.email
    if is_fluid_staff(objective_email):
        return "help@fluidattacks.com"

    return objective_email


def _get_fullname(objective_data: EventComment) -> str:
    objective_email = objective_data.email
    objective_possible_fullname = (
        objective_data.full_name if objective_data.full_name else None
    )
    real_name = objective_possible_fullname or objective_email

    if is_fluid_staff(objective_email):
        return "Fluid Attacks"

    return real_name


def format_event_consulting_resolve(event_comment: EventComment) -> Item:
    email = _get_email(objective_data=event_comment)
    fullname = _get_fullname(objective_data=event_comment)
    comment_date: str = format_comment_datetime(event_comment.creation_date)
    return {
        "content": event_comment.content,
        "created": comment_date,
        "email": email,
        "fullname": fullname if fullname else email,
        "id": event_comment.id,
        "modified": comment_date,
        "parent": event_comment.parent_id,
    }
