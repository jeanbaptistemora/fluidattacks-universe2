from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from custom_types import (
    Comment as CommentType,
    DynamoDelete as DynamoDeleteType,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from itertools import (
    chain,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    List,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "FI_comments"
TABLE_NAME_NEW: str = "fi_finding_comments"


async def create(comment_id: int, comment_attributes: CommentType) -> bool:
    success = False
    try:
        comment_attributes.update({"user_id": comment_id})
        success = await dynamodb_ops.put_item(TABLE_NAME, comment_attributes)
        comment_attributes.update(
            {
                "finding_id": str(comment_attributes.pop("finding_id")),
                "comment_id": str(comment_attributes.pop("user_id")),
                "parent": str(comment_attributes.pop("parent")),
            }
        )
        success = success and await dynamodb_ops.put_item(
            TABLE_NAME_NEW, comment_attributes
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def delete(finding_id: int, user_id: int) -> bool:
    success = False
    try:
        delete_attrs = DynamoDeleteType(
            Key={"finding_id": finding_id, "user_id": user_id}
        )
        success = await dynamodb_ops.delete_item(TABLE_NAME, delete_attrs)
        delete_attrs = DynamoDeleteType(
            Key={"finding_id": str(finding_id), "comment_id": str(user_id)}
        )
        success = success and await dynamodb_ops.delete_item(
            TABLE_NAME_NEW, delete_attrs
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def get_comments(
    comment_type: str, finding_id: int
) -> List[CommentType]:
    """Get comments of the given finding"""
    key_exp = Key("finding_id").eq(finding_id)
    comment_type = comment_type.lower()
    if comment_type == "comment":
        filter_exp: object = Attr("comment_type").eq("comment") | Attr(
            "comment_type"
        ).eq("verification")
    elif comment_type == "observation":
        filter_exp = Attr("comment_type").eq("observation")
    elif comment_type == "event":
        filter_exp = Attr("comment_type").eq("event")
    elif comment_type == "zero_risk":
        filter_exp = Attr("comment_type").eq("zero_risk")
    query_attrs = {
        "KeyConditionExpression": key_exp,
        "FilterExpression": filter_exp,
    }
    return await dynamodb_ops.query(TABLE_NAME, query_attrs)


async def get_comments_for_ids(
    comment_type: str,
    identifiers: List[str],
) -> List[CommentType]:
    """Retrieve comments for several ids"""
    comments = await collect(
        get_comments(
            comment_type,
            int(identifier),
        )
        for identifier in identifiers
    )
    return list(chain.from_iterable(comments))
