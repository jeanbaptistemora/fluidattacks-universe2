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
from db_model.organization_access.types import (
    OrganizationAccess,
    OrganizationAccessMetadataToUpdate,
)
from dynamodb.operations_legacy import (
    delete_item as dynamodb_delete_item,
    put_item as dynamodb_put_item,
    query as dynamodb_query,
    update_item as dynamodb_update_item,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils.organization_access import (
    format_metadata_item,
)
from newutils.organizations import (
    remove_org_id_prefix,
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
TABLE_NAME = "fi_organizations"


async def add(*, organization_access: OrganizationAccess) -> None:
    organization_id = remove_org_id_prefix(organization_access.organization_id)
    email = organization_access.email.lower().strip()
    item = {
        "pk": f"ORG#{organization_id}",
        "sk": f"USER#{email}",
    }
    try:
        if not await dynamodb_put_item(TABLE_NAME, item):
            raise UnavailabilityError()
    except ClientError as ex:
        raise UnavailabilityError() from ex


async def get_ids_for_user(email: str) -> list[str]:
    """
    Return the IDs of all the organizations a user belongs to.
    """
    organization_ids: list[str] = []
    query_attrs = {
        "KeyConditionExpression": (
            Key("sk").eq(f"USER#{email.lower().strip()}")
        ),
        "IndexName": "gsi-1",
        "ProjectionExpression": "pk",
    }
    try:
        response_items = await dynamodb_query(TABLE_NAME, query_attrs)
        if response_items:
            organization_ids = [item["pk"] for item in response_items]
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return organization_ids


async def get_users(organization_id: str) -> list[str]:
    """
    Return a list of the emails of all the users that belong to an
    organization.
    """
    organization_id = remove_org_id_prefix(organization_id)
    users: list[str] = []
    query_attrs = {
        "KeyConditionExpression": (
            Key("pk").eq(f"ORG#{organization_id}")
            & Key("sk").begins_with("USER#")
        )
    }
    try:
        response_items = await dynamodb_query(TABLE_NAME, query_attrs)
        if response_items:
            users = [item["sk"].split("#")[1] for item in response_items]
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return users


async def has_user_access(organization_id: str, email: str) -> bool:
    organization_id = remove_org_id_prefix(organization_id)
    has_access: bool = False
    query_attrs: dict[str, Any] = {
        "KeyConditionExpression": (
            Key("pk").eq(f"ORG#{organization_id}")
            & Key("sk").eq(f"USER#{email.lower().strip()}")
        )
    }
    response_items = await dynamodb_query(TABLE_NAME, query_attrs)
    if response_items:
        has_access = True
    return has_access


async def remove(*, email: str, organization_id: str) -> None:
    """Remove a stakeholder org access."""
    organization_id = remove_org_id_prefix(organization_id)
    item = DynamoDeleteType(
        Key={
            "pk": f"ORG#{organization_id}",
            "sk": f"USER#{email.lower().strip()}",
        }
    )
    try:
        if not await dynamodb_delete_item(TABLE_NAME, item):
            raise UnavailabilityError()
    except ClientError as ex:
        raise UnavailabilityError() from ex


async def _update_stakeholder(
    organization_id: str, user_email: str, data: dict[str, Any]
) -> bool:
    """Update org access attributes."""
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

    organization_id = remove_org_id_prefix(organization_id)
    update_attrs = {
        "Key": {
            "pk": f"ORG#{organization_id}",
            "sk": f"USER#{user_email.lower()}",
        },
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    try:
        success = await dynamodb_update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def update_metadata(
    *,
    email: str,
    metadata: OrganizationAccessMetadataToUpdate,
    organization_id: str,
) -> None:
    data: Item = format_metadata_item(metadata)
    if not await _update_stakeholder(organization_id, email, data):
        raise UnavailabilityError()
