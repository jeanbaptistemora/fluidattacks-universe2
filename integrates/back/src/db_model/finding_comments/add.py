from .types import (
    FindingComment,
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
from db_model.finding_comments.utils import (
    format_finding_comment_item,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)


async def add(*, finding_comment: FindingComment) -> None:
    key_structure = TABLE.primary_key

    finding_comment_key = keys.build_key(
        facet=TABLE.facets["finding_comment"],
        values={
            "id": finding_comment.id,
            "finding_id": finding_comment.finding_id,
        },
    )

    finding_comment_item = {
        key_structure.partition_key: finding_comment_key.partition_key,
        key_structure.sort_key: finding_comment_key.sort_key,
        **format_finding_comment_item(finding_comment),
    }

    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["finding_comment"],
            item=finding_comment_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedComment() from ex
