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
from decimal import (
    Decimal,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = "fi_portfolios"


async def delete(organization_name: str, tag: str) -> bool:
    success: bool = False
    item = DynamoDeleteType(
        Key={"organization": organization_name.lower(), "tag": tag.lower()}
    )
    try:
        success = await dynamodb_ops.delete_item(TABLE_NAME, item)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def get_attributes(
    organization_name: str, tag: str, attributes: Optional[list[str]] = None
) -> dict[str, Union[list[str], str]]:
    response = {}
    item_attrs: dict[str, Any] = {
        "KeyConditionExpression": (
            Key("organization").eq(organization_name.lower())
            & Key("tag").eq(tag.lower())
        ),
    }
    if attributes:
        item_attrs["ProjectionExpression"] = ",".join(attributes)
    response_items = await dynamodb_ops.query(TABLE_NAME, item_attrs)
    if response_items:
        response = response_items[0]
    return response


async def get_tags(
    organization_name: str, attributes: Optional[list[str]]
) -> list[Dict[str, Any]]:
    tags: list[Dict[str, Any]] = []
    query_attrs = {
        "KeyConditionExpression": Key("organization").eq(organization_name)
    }
    if attributes:
        projection = ",".join(attributes)
        query_attrs.update({"ProjectionExpression": projection})
    try:
        tags = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return tags


async def update(
    organization_name: str,
    tag: str,
    data: dict[str, Union[list[str], Decimal]],
) -> bool:
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
        "Key": {"organization": organization_name, "tag": tag},
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }

    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    if expression_names:
        update_attrs.update({"ExpressionAttributeNames": expression_names})
    try:
        success = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success
