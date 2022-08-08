from db_model.finding_comments.types import (
    FindingComment,
)
from dynamodb.types import (
    Item,
)
from newutils.datetime import (
    convert_from_iso_str,
    convert_to_iso_str,
    format_comment_date,
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


def format_finding_comments(item: Item) -> FindingComment:
    return FindingComment(
        finding_id=item["finding_id"],
        id=str(item["comment_id"]),
        comment_type=item["comment_type"],
        parent_id=str(item["parent"]),
        creation_date=convert_to_iso_str(item["created"]),
        full_name=item.get("fullname", None),
        content=item["content"],
        email=item["email"],
    )


def format_finding_consulting_resolve(finding_comment: FindingComment) -> Item:
    fullname = _get_fullname(objective_data=finding_comment)
    return {
        "content": finding_comment.content,
        "created": format_comment_date(
            convert_from_iso_str(finding_comment.creation_date)
        ),
        "email": finding_comment.email,
        "fullname": fullname if fullname else finding_comment.email,
        "id": finding_comment.id,
        "modified": format_comment_date(
            convert_from_iso_str(finding_comment.creation_date)
        ),
        "parent": finding_comment.parent_id,
    }


def format_finding_comment_item(finding_comment: FindingComment) -> Item:
    return {
        "finding_id": finding_comment.finding_id,
        "comment_id": int(finding_comment.id),
        "parent": finding_comment.parent_id,
        "comment_type": finding_comment.comment_type,
        "created": convert_from_iso_str(finding_comment.creation_date),
        "fullname": finding_comment.full_name,
        "content": finding_comment.content,
        "email": finding_comment.email,
        "modified": convert_from_iso_str(finding_comment.creation_date),
    }
