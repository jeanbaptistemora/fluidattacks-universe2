from db_model.finding_comments.types import (
    FindingComment,
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


def _get_email(objective_data: FindingComment, is_draft: bool = False) -> str:
    objective_email = objective_data.email
    if is_fluid_staff(objective_email) and not is_draft:
        return "help@fluidattacks.com"

    return objective_email


def _get_fullname(
    objective_data: FindingComment, is_draft: bool = False
) -> str:
    objective_email = objective_data.email
    objective_possible_fullname = (
        objective_data.full_name if objective_data.full_name else None
    )
    real_name = objective_possible_fullname or objective_email

    if is_fluid_staff(objective_email) and not is_draft:
        return "Fluid Attacks"

    return real_name


def format_finding_consulting_resolve(
    finding_comment: FindingComment, is_draft: bool = False
) -> Item:
    email = _get_email(objective_data=finding_comment, is_draft=is_draft)
    fullname = _get_fullname(objective_data=finding_comment, is_draft=is_draft)
    comment_date: str = format_comment_datetime(finding_comment.creation_date)
    return {
        "content": finding_comment.content,
        "created": comment_date,
        "email": email,
        "fullname": fullname if fullname else email,
        "id": finding_comment.id,
        "modified": comment_date,
        "parent": finding_comment.parent_id,
    }
