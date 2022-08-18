from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    UnavailabilityError,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
)
from db_model.event_comments.types import (
    EventComment,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils.event_comments import (
    format_event_comment_item,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "fi_finding_comments"


async def _create(
    comment_id: str, comment_attributes: dict[str, Any], event_id: str
) -> bool:
    success = False
    try:
        success = await dynamodb_ops.put_item(
            TABLE_NAME,
            {
                **comment_attributes,
                "comment_id": comment_id,
                "finding_id": event_id,
                "parent": str(comment_attributes["parent"]),
            },
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def add(
    *,
    event_comment: EventComment,
) -> None:
    event_comment_item = format_event_comment_item(event_comment)
    if not await _create(
        event_comment.id, event_comment_item, event_comment.event_id
    ):
        raise UnavailabilityError()


async def remove(
    *,
    comment_id: str,
    event_id: str,
) -> None:
    delete_attrs = DynamoDeleteType(
        Key={"finding_id": event_id, "comment_id": comment_id}
    )
    if not await dynamodb_ops.delete_item(TABLE_NAME, delete_attrs):
        raise UnavailabilityError()
