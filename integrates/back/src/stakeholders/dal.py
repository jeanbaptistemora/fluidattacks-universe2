from boto3.dynamodb.conditions import (
    Key,
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
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderMetadataToUpdate,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils import (
    stakeholders as stakeholders_utils,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
USERS_TABLE_NAME = "FI_users"


async def add(stakeholder: Stakeholder) -> None:
    try:
        data = stakeholders_utils.format_stakeholder_item(
            stakeholder=stakeholder
        )
        await dynamodb_ops.put_item(USERS_TABLE_NAME, data)
    except ClientError as ex:
        raise UnavailabilityError() from ex


async def remove(email: str) -> None:
    try:
        delete_attrs = DynamoDeleteType(Key={"email": email.lower()})
        await dynamodb_ops.delete_item(USERS_TABLE_NAME, delete_attrs)
    except ClientError as ex:
        raise UnavailabilityError() from ex


async def get(email: str) -> dict[str, Any]:
    response = {}
    query_attrs = {
        "KeyConditionExpression": Key("email").eq(email.lower()),
        "Limit": 1,
    }
    response_items = await dynamodb_ops.query(USERS_TABLE_NAME, query_attrs)
    if response_items:
        response = response_items[0]
    return response


async def get_all(
    filter_exp: object, data_attr: str = ""
) -> list[dict[str, dict[str, Any]]]:
    scan_attrs = {}
    scan_attrs["FilterExpression"] = filter_exp
    if data_attr:
        scan_attrs["ProjectionExpression"] = data_attr
    items = await dynamodb_ops.scan(USERS_TABLE_NAME, scan_attrs)
    return items


async def update(email: str, data: dict[str, Any]) -> bool:
    success = False
    set_expression = ""
    remove_expression = ""
    expression_names = {}
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f"#{attr}, "
            expression_names.update({f"#{attr}": attr})
        else:
            set_expression += f"#{attr} = :{attr}, "
            expression_names.update({f"#{attr}": attr})
            expression_values.update({f":{attr}": value})
    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'
    update_attrs = {
        "Key": {"email": email.lower()},
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    if expression_names:
        update_attrs.update({"ExpressionAttributeNames": expression_names})
    try:
        success = await dynamodb_ops.update_item(
            USERS_TABLE_NAME, update_attrs
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def update_metadata(
    *,
    metadata: StakeholderMetadataToUpdate,
    stakeholder_email: str,
) -> None:
    if metadata.notifications_preferences:
        await stakeholders_model.update_metadata(
            metadata=StakeholderMetadataToUpdate(
                notifications_preferences=metadata.notifications_preferences
            ),
            stakeholder_email=stakeholder_email,
        )
    item = stakeholders_utils.format_metadata_item(metadata=metadata)
    if item and not await update(
        email=stakeholder_email,
        data=item,
    ):
        raise UnavailabilityError()
