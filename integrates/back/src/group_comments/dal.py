from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    UnavailabilityError,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
)
from db_model.group_comments.types import (
    GroupComment,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils.group_comments import (
    format_group_comment_item,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    cast,
    Dict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "fi_project_comments"


async def _add_comment(
    group_name: str, email: str, comment_data: Dict[str, Any]
) -> bool:
    """Add a comment in a group."""
    resp = False
    try:
        payload = {"project_name": group_name, "email": email}
        payload.update(cast(Dict[str, str], comment_data))
        resp = await dynamodb_ops.put_item(TABLE_NAME, payload)
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    return resp


async def add(*, group_comment: GroupComment) -> None:
    """Add a comment in a group."""
    comment_item = format_group_comment_item(group_comment)
    if not await _add_comment(
        group_name=group_comment.group_name,
        email=group_comment.email,
        comment_data=comment_item,
    ):
        raise UnavailabilityError()


async def remove(*, group_name: str, comment_id: str) -> None:
    try:
        delete_attrs = DynamoDeleteType(
            Key={"project_name": group_name, "user_id": comment_id}
        )
        if not await dynamodb_ops.delete_item(TABLE_NAME, delete_attrs):
            raise UnavailabilityError()
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        raise UnavailabilityError() from ex
