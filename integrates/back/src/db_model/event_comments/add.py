# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    EventComment,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    RepeatedComment,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore


async def add(*, event_comment: EventComment) -> None:
    key_structure = TABLE.primary_key

    event_comment_key = keys.build_key(
        facet=TABLE.facets["event_comment"],
        values={"id": event_comment.id, "event_id": event_comment.event_id},
    )

    event_comment_item = {
        key_structure.partition_key: event_comment_key.partition_key,
        key_structure.sort_key: event_comment_key.sort_key,
        **json.loads(json.dumps(event_comment)),
    }

    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["event_comment"],
            item=event_comment_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedComment() from ex
