from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    UnavailabilityError,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils.finding_comments import (
    format_finding_comment_item,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Dict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "fi_finding_comments"


async def _create(
    comment_id: str, comment_attributes: Dict[str, Any], finding_id: str
) -> bool:
    success = False
    try:
        success = await dynamodb_ops.put_item(
            TABLE_NAME,
            {
                **comment_attributes,
                "comment_id": comment_id,
                "finding_id": finding_id,
                "parent": str(comment_attributes["parent"]),
            },
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def add(*, finding_comment: FindingComment) -> None:
    finding_comment_item = format_finding_comment_item(finding_comment)
    if not await _create(
        finding_comment.id,
        finding_comment_item,
        finding_comment.finding_id,
    ):
        raise UnavailabilityError()


async def remove(*, comment_id: str, finding_id: str) -> None:
    delete_attrs = DynamoDeleteType(
        Key={"finding_id": finding_id, "comment_id": comment_id}
    )
    if not await dynamodb_ops.delete_item(TABLE_NAME, delete_attrs):
        raise UnavailabilityError()
