from boto3.dynamodb.conditions import (
    ConditionBase,
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    InvalidOrganization,
    OrganizationNotFound,
    UnavailabilityError,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationPoliciesToUpdate,
    OrganizationState,
)
from dynamodb.operations_legacy import (
    client as dynamodb_client,
    delete_item as dynamodb_delete_item,
    get_item as dynamodb_get_item,
    put_item as dynamodb_put_item,
    query as dynamodb_query,
    update_item as dynamodb_update_item,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from newutils.organizations import (
    format_org_policies_item,
    format_organization,
    format_organization_item,
    format_organization_state_item,
    remove_org_id_prefix,
)
from newutils.utils import (
    get_key_or_fallback,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    AsyncIterator,
    cast,
    Optional,
)
import uuid

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = "fi_organizations"


def _map_attributes_to_dal(attrs: list[str]) -> list[str]:
    """
    Map domain attributes to its DynamoDB representation.
    """
    mapping = {"id": "pk", "name": "sk"}
    mapped_attrs = [attr for attr in attrs if attr not in mapping]
    mapped_attrs.extend([mapping[attr] for attr in attrs if attr in mapping])
    return mapped_attrs


def _map_keys_to_domain(org: dict[str, Any]) -> dict[str, Any]:
    """
    Map DynamoDB keys to a human-readable form.
    """
    mapping = {"pk": "id", "sk": "name"}
    mapped_org = {key: org[key] for key in org if key not in mapping}
    mapped_org.update(
        {mapping[key]: org[key] for key in org if key in mapping}
    )
    return mapped_org


async def add_user(organization_id: str, email: str) -> bool:
    organization_id = remove_org_id_prefix(organization_id)
    success: bool = False
    new_item = {
        "pk": f"ORG#{organization_id}",
        "sk": f"USER#{email.lower().strip()}",
    }
    try:
        success = await dynamodb_put_item(TABLE_NAME, new_item)
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return success


async def add_typed(
    organization: Organization,
) -> None:
    org_item = format_organization_item(organization)
    try:
        await dynamodb_put_item(TABLE_NAME, org_item)
    except ClientError as ex:
        raise UnavailabilityError() from ex


async def add(
    *,
    modified_by: str,
    organization_name: str,
    organization_id: str = "",
) -> dict[str, Any]:
    """
    Add an organization and returns its key.
    """
    if await exists(organization_name):
        raise InvalidOrganization()

    organization_id = (
        str(uuid.uuid4()) if organization_id == "" else organization_id
    )
    organization_name = organization_name.lower().strip()
    new_state = {
        "modified_by": modified_by,
        "modified_date": datetime_utils.get_now_as_str(),
        "status": OrganizationStateStatus.ACTIVE.value,
    }
    item_to_add: dict[str, Any] = {
        "pk": f"ORG#{organization_id}",
        "sk": f"INFO#{organization_name}",
        "historic_state": [new_state],
    }
    try:
        await dynamodb_put_item(TABLE_NAME, item_to_add)
    except ClientError as ex:
        raise UnavailabilityError() from ex

    return {
        "id": organization_id,
        "name": organization_name,
        "historic_state": [new_state],
    }


async def update_state(
    *,
    organization_id: str,
    organization_name: str,
    state: OrganizationState,
) -> bool:
    organization: Item = await get_by_id(organization_id, ["historic_state"])
    historic_state: list[dict[str, str]] = organization.get(
        "historic_state", []
    )
    new_state: Item = format_organization_state_item(
        state,
    )
    item_to_update: Item = {
        "historic_state": [
            *historic_state,
            new_state,
        ]
    }
    return await update(
        organization_id=organization_id,
        organization_name=organization_name,
        values=item_to_update,
    )


async def exists(org_name: str) -> bool:
    """
    Returns True if the organization key exists.
    """
    try:
        await get_by_name(org_name.lower().strip())
        return True
    except OrganizationNotFound:
        return False


async def get_access_by_url_token(
    organization_id: str,
    user_email: str,
) -> dict[str, Any]:
    """Get user access of a organization by the url token."""
    organization_id = remove_org_id_prefix(organization_id)
    key = {
        "pk": f"ORG#{organization_id}",
        "sk": f"USER#{user_email}",
    }
    get_attrs = {"Key": cast(ConditionBase, key)}
    item = await dynamodb_get_item(TABLE_NAME, get_attrs)
    return item


async def get_by_id(
    organization_id: str, attributes: Optional[list[str]] = None
) -> dict[str, Any]:
    """
    Use the organization ID to fetch general information about it.
    """
    organization_id = remove_org_id_prefix(organization_id)
    organization: dict[str, Any] = {}
    query_attrs = {
        "KeyConditionExpression": (
            Key("pk").eq(f"ORG#{organization_id}")
            & Key("sk").begins_with("INFO#")
        )
    }

    if attributes:
        projection = ",".join(_map_attributes_to_dal(attributes))
        query_attrs.update({"ProjectionExpression": projection})
    try:
        response_item = await dynamodb_query(TABLE_NAME, query_attrs)
        if not response_item:
            raise OrganizationNotFound()
        organization = response_item[0]
        if "sk" in organization:
            organization.update(
                {"sk": cast(str, organization["sk"]).split("#")[1]}
            )
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return _map_keys_to_domain(organization)


async def get_by_name(
    org_name: str, attributes: Optional[list[str]] = None
) -> dict[str, Any]:
    """
    Get an organization info given its name
    Return specified attributes or all if not setted.
    """
    organization: dict[str, Any] = {}
    query_attrs = {
        "KeyConditionExpression": (
            Key("sk").eq(f"INFO#{org_name.lower().strip()}")
            & Key("pk").begins_with("ORG#")
        ),
        "IndexName": "gsi-1",
        "Limit": 1,
    }
    if attributes:
        projection = ",".join(_map_attributes_to_dal(attributes))
        query_attrs["ProjectionExpression"] = projection
    try:
        response_items = await dynamodb_query(TABLE_NAME, query_attrs)
        if not response_items:
            raise OrganizationNotFound()
        organization = response_items[0]
        if "sk" in organization:
            organization.update(
                {"sk": cast(str, organization["sk"]).split("#")[1]}
            )
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return _map_keys_to_domain(organization)


async def get_id_for_group(group_name: str) -> str:
    """
    Return the ID of the organization a group belongs to.
    """
    organization_id: str = ""
    query_attrs: dict[str, Any] = {
        "KeyConditionExpression": (
            Key("sk").eq(f"GROUP#{group_name.lower().strip()}")
        ),
        "IndexName": "gsi-1",
        "ProjectionExpression": "pk",
    }
    try:
        response_item = await dynamodb_query(TABLE_NAME, query_attrs)
        if response_item:
            organization_id = response_item[0]["pk"]
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return organization_id


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


async def iterate_organizations() -> AsyncIterator[Organization]:
    """Yield typed organizations non-concurrently generated."""
    async with dynamodb_client() as client:
        async for response in client.get_paginator("scan").paginate(
            ExpressionAttributeNames={
                "#pk": "pk",
                "#sk": "sk",
            },
            ExpressionAttributeValues={
                ":pk": {"S": "ORG#"},
                ":sk": {"S": "INFO#"},
            },
            FilterExpression=(
                "begins_with(#pk, :pk) and begins_with(#sk, :sk)"
            ),
            TableName=TABLE_NAME,
        ):
            for item in response["Items"]:
                yield format_organization(await get_by_id(item["pk"]["S"]))


async def remove_user(organization_id: str, email: str) -> bool:
    """
    Remove a user from an organization.
    """
    success: bool = False
    organization_id = remove_org_id_prefix(organization_id)
    user_item = DynamoDeleteType(
        Key={
            "pk": f"ORG#{organization_id}",
            "sk": f"USER#{email.lower().strip()}",
        }
    )
    try:
        success = await dynamodb_delete_item(TABLE_NAME, user_item)
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return success


async def update(
    organization_id: str, organization_name: str, values: dict[str, Any]
) -> bool:
    """
    Updates the attributes of an organization.
    """
    success: bool = False
    set_expression: str = ""
    remove_expression: str = ""
    expression_values: dict[str, Any] = {}
    for attr, value in values.items():
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
    try:
        update_attrs: dict[str, Any] = {
            "Key": {
                "pk": f"ORG#{organization_id}",
                "sk": f"INFO#{organization_name.lower().strip()}",
            },
            "UpdateExpression": (
                f"{set_expression} {remove_expression}".strip()
            ),
        }
        if expression_values:
            update_attrs.update(
                {"ExpressionAttributeValues": expression_values}
            )
        success = await dynamodb_update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return success


async def update_policies_typed(
    organization_id: str,
    organization_name: str,
    policies_to_update: OrganizationPoliciesToUpdate,
    user_email: str,
) -> bool:
    historic_policies: list[Item] = []
    if policies_to_update.max_number_acceptances is not None:
        organization_data = await get_by_id(
            organization_id=organization_id,
            attributes=[
                "historic_max_number_acceptances",
                "historic_max_number_acceptations",
            ],
        )
        historic_policies = get_key_or_fallback(
            organization_data,
            "historic_max_number_acceptances",
            "historic_max_number_acceptations",
            fallback=[],
        )
    organization_item = format_org_policies_item(
        historic=historic_policies,
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        policies=policies_to_update,
    )
    success = await update(
        organization_id=organization_id,
        organization_name=organization_name,
        values=organization_item,
    )
    return success


async def update_user(
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
