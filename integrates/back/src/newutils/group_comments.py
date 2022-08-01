from db_model.group_comments.types import (
    GroupComment,
)
from dynamodb.types import (
    Item,
)


def format_group_comments(item: Item) -> GroupComment:
    return GroupComment(
        group_name=item["project_name"],
        id=str(item["user_id"]),
        parent_id=str(item["parent"]),
        creation_date=item["created"],
        full_name=item["fullname"],
        content=item["content"],
        email=item["email"],
    )
