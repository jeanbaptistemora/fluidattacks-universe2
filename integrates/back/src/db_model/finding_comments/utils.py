from db_model.finding_comments.types import (
    FindingComment,
)
from dynamodb.types import (
    Item,
)


def format_finding_comment_item(finding_comment: FindingComment) -> Item:
    return {
        "finding_id": finding_comment.finding_id,
        "id": finding_comment.id,
        "parent_id": finding_comment.parent_id,
        "comment_type": finding_comment.comment_type.value,
        "creation_date": finding_comment.creation_date,
        "content": finding_comment.content,
        "email": finding_comment.email,
        "full_name": finding_comment.full_name,
    }
