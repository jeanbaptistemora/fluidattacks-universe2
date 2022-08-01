from db_model.group_comments.types import (
    GroupComment,
)
from dynamodb.types import (
    Item,
)
from newutils.datetime import (
    convert_from_iso_str,
    convert_to_iso_str,
    format_comment_date,
)


def _get_fullname(objective_data: GroupComment) -> str:
    objective_email = objective_data.email
    objective_possible_fullname = (
        objective_data.full_name if objective_data.full_name else None
    )
    real_name = objective_possible_fullname or objective_email

    if "@fluidattacks.com" in objective_email:
        return f"{real_name} at Fluid Attacks"

    return real_name


def format_group_comments(item: Item) -> GroupComment:
    return GroupComment(
        group_name=item["project_name"],
        id=str(item["user_id"]),
        parent_id=str(item["parent"]),
        creation_date=convert_to_iso_str(item["created"]),
        full_name=item.get("fullname", None),
        content=item["content"],
        email=item["email"],
    )


def format_group_consulting_resolve(group_comment: GroupComment) -> Item:
    fullname = _get_fullname(objective_data=group_comment)
    return {
        "content": group_comment.content,
        "created": format_comment_date(
            convert_from_iso_str(group_comment.creation_date)
        ),
        "email": group_comment.email,
        "fullname": fullname if fullname else group_comment.email,
        "id": group_comment.id,
        "modified": format_comment_date(
            convert_from_iso_str(group_comment.creation_date)
        ),
        "parent": group_comment.parent_id,
    }


def format_group_comment_item(group_comment: GroupComment) -> Item:
    return {
        "project_name": group_comment.group_name,
        "user_id": group_comment.id,
        "parent": group_comment.parent_id,
        "created": convert_from_iso_str(group_comment.creation_date),
        "fullname": group_comment.full_name,
        "content": group_comment.content,
        "email": group_comment.email,
        "modified": convert_from_iso_str(group_comment.creation_date),
    }
