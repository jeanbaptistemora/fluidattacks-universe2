from boto3.dynamodb.conditions import (
    Attr,
)
from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    UnavailabilityError,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils import (
    group_access as group_access_utils,
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
TABLE_NAME: str = "FI_project_access"


async def add(*, group_access: GroupAccess) -> None:
    item = group_access_utils.format_group_access_item(group_access)
    try:
        if not await dynamodb_ops.put_item(TABLE_NAME, item):
            raise UnavailabilityError()
    except ClientError as ex:
        raise UnavailabilityError() from ex


async def get_access_by_url_token(
    url_token: str,
    attr: str = "invitation",
) -> list[dict[str, Any]]:
    """Get user access of a group by the url token"""
    filter_exp = Attr(attr).exists() & Attr(f"{attr}.url_token").eq(url_token)
    scan_attrs = {"FilterExpression": filter_exp}
    items = await dynamodb_ops.scan(TABLE_NAME, scan_attrs)
    return items


async def remove(*, email: str, group_name: str) -> None:
    """Remove group access in dynamo."""
    delete_attrs = DynamoDeleteType(
        Key={
            "user_email": email.lower(),
            "project_name": group_name.lower(),
        }
    )
    try:
        if not await dynamodb_ops.delete_item(TABLE_NAME, delete_attrs):
            raise UnavailabilityError()
    except ClientError as ex:
        raise UnavailabilityError() from ex


async def _update(email: str, group_name: str, data: dict[str, Any]) -> bool:
    """Update group access attributes."""
    success = False
    set_expression = ""
    remove_expression = ""
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f"{attr}, "
        else:
            set_expression += f"{attr} = :{attr}, "
            expression_values.update({f":{attr}": value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        "Key": {
            "user_email": email.lower(),
            "project_name": group_name.lower(),
        },
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    try:
        success = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def update_metadata(
    *,
    email: str,
    group_name: str,
    metadata: GroupAccessMetadataToUpdate,
) -> None:
    item = group_access_utils.format_metadata_item(metadata)
    if not await _update(email=email, group_name=group_name, data=item):
        raise UnavailabilityError()
