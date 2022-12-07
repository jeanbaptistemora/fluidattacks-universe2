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
from db_model.utils import (
    serialize,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json


async def add(*, group_comment: GroupComment) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["group_comment"],
        values={"id": group_comment.id, "name": group_comment.group_name},
    )
    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        **json.loads(json.dumps(group_comment, default=serialize)),
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["group_comment"],
            item=item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedComment() from ex
