# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.group_comments.types import (
    GroupComment,
)
from dynamodb.types import (
    Item,
)


def format_group_comments(item: Item) -> GroupComment:
    return GroupComment(
        group_name=item["group_name"],
        id=item["id"],
        parent_id=item["parent_id"],
        creation_date=item["creation_date"],
        full_name=item.get("full_name"),
        content=item["content"],
        email=item["email"],
    )
