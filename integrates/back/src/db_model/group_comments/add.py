from .types import (
    GroupComment,
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


async def add(*, group_comment: GroupComment) -> None:
    key_structure = TABLE.primary_key

    group_comments_key = keys.build_key(
        facet=TABLE.facets["group_comment"],
        values={"id": group_comment.id, "name": group_comment.group_name},
    )

    group_comments_item = {
        key_structure.partition_key: group_comments_key.partition_key,
        key_structure.sort_key: group_comments_key.sort_key,
        **json.loads(json.dumps(group_comment)),
    }

    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["group_comment"],
            item=group_comments_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedComment() from ex
