from db_model.group_comments.types import (
    GroupComment,
)
from dynamodb.types import (
    Item,
)
from newutils.datetime import (
    convert_from_iso_str,
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
