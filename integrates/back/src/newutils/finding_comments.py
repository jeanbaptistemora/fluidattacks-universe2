from db_model.finding_comments.types import (
    FindingComment,
)
from dynamodb.types import (
    Item,
)
from newutils.datetime import (
    format_comment_datetime,
)


def _get_fullname(objective_data: FindingComment) -> str:
    objective_email = objective_data.email
    objective_possible_fullname = (
        objective_data.full_name if objective_data.full_name else None
    )
    real_name = objective_possible_fullname or objective_email

    if "@fluidattacks.com" in objective_email:
        return f"{real_name} at Fluid Attacks"

    return real_name


def format_finding_consulting_resolve(finding_comment: FindingComment) -> Item:
    fullname = _get_fullname(objective_data=finding_comment)
    comment_date: str = format_comment_datetime(finding_comment.creation_date)
    return {
        "content": finding_comment.content,
        "created": comment_date,
        "email": finding_comment.email,
        "fullname": fullname if fullname else finding_comment.email,
        "id": finding_comment.id,
        "modified": comment_date,
        "parent": finding_comment.parent_id,
    }
