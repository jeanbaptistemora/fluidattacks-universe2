import aioboto3
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    ErrorAddingGroup,
    ErrorUpdatingGroup,
)
from custom_types import (
    Group as GroupType,
)
from db_model.groups.types import (
    Group,
    GroupMetadataToUpdate,
    GroupState,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils import (
    groups as groups_utils,
)
from newutils.utils import (
    duplicate_dict_keys,
    get_key_or_fallback,
)
from settings import (
    LOGGING,
)
from typing import (
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "FI_projects"


async def can_user_access(
    group_name: str, role: str, table: aioboto3.session.Session.client = None
) -> bool:
    group_data = await get_attributes(
        group_name.lower(),
        [
            "deletion_date",
            "historic_deletion",
            "project_name",
            "project_status",
        ],
        table,
    )
    is_user_allowed = False
    if await is_valid(group_name, group_data):
        is_user_allowed = bool(role)
    return is_user_allowed


async def add(group: GroupType) -> bool:
    """Add group to dynamo."""
    resp = False
    try:
        resp = await dynamodb_ops.put_item(TABLE_NAME, group)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return resp


async def add_typed(
    *,
    group: Group,
) -> None:
    group_item = groups_utils.format_group_to_add_item(group)
    if not await add(group=group_item):
        raise ErrorAddingGroup.new()


async def exists(
    group_name: str, pre_computed_group_data: Optional[GroupType] = None
) -> bool:
    group = group_name.lower()
    group_data = pre_computed_group_data or await get_attributes(
        group, ["project_name"]
    )
    return bool(group_data)


async def get_active_groups() -> List[str]:
    """Get active groups names in DynamoDB."""
    filtering_exp = (
        Attr("project_status").eq("ACTIVE") & Attr("project_status").exists()
    )
    groups = await get_all(filtering_exp, "project_name")
    return cast(List[str], [get_key_or_fallback(group) for group in groups])


async def get_active_groups_attributes(data_attr: str = "") -> List[GroupType]:
    """Get active groups attributes in DynamoDB."""
    filtering_exp = Attr("project_status").eq("ACTIVE")
    groups: List[GroupType] = await get_all(filtering_exp, data_attr)
    # Compatibility with old API
    if "project_name" in groups[0]:
        groups_with_gn: List[GroupType] = [
            duplicate_dict_keys(group, "group_name", "project_name")
            for group in groups
        ]
        return groups_with_gn
    return groups


async def get_all(
    filtering_exp: object = "", data_attr: str = ""
) -> List[GroupType]:
    """Get all groups."""
    scan_attrs = {}
    if filtering_exp:
        scan_attrs["FilterExpression"] = filtering_exp
    if data_attr:
        scan_attrs["ProjectionExpression"] = data_attr
    items = await dynamodb_ops.scan(TABLE_NAME, scan_attrs)
    return cast(List[GroupType], items)


async def get_attributes(
    group_name: str,
    attributes: Optional[List[str]] = None,
    table: aioboto3.session.Session.client = None,
) -> Dict[str, Union[str, List[str]]]:
    response = {}
    query_attrs = {
        "KeyConditionExpression": Key("project_name").eq(group_name),
        "Limit": 1,
    }
    if attributes:
        projection = ",".join(attributes)
        query_attrs.update({"ProjectionExpression": projection})

    if not table:
        response_items = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    else:
        response_item = await table.query(**query_attrs)
        response_items = response_item.get("Items", [])

    if response_items:
        response = response_items[0]
    return response


async def get_description(group_name: str) -> str:
    """Get the description of a group."""
    description = await get_attributes(group_name, ["description"])
    group_description = (
        str(description.get("description", "")) if description else ""
    )
    return group_description


async def get_group_info(group_name: str) -> Tuple[str, str, str]:
    """Get the information section of a group."""
    info = await get_attributes(
        group_name, ["description", "business_id", "business_name"]
    )
    business_id = str(info.get("business_id", "")) if info else ""
    business_name = str(info.get("business_name", "")) if info else ""
    group_description = str(info.get("description", "")) if info else ""
    return (business_id, business_name, group_description)


async def get_group(
    group_name: str, table: aioboto3.session.Session.client
) -> GroupType:
    response = await table.get_item(Key={"project_name": group_name})
    return response.get("Item", {})


async def get_groups_with_forces() -> List[str]:
    filtering_exp = Attr("project_status").eq("ACTIVE")
    query_attrs = {
        "ProjectionExpression": "#name,#h_config",
        "FilterExpression": filtering_exp,
        "ExpressionAttributeNames": {
            "#name": "project_name",
            "#h_config": "historic_configuration",
        },
    }
    response = await dynamodb_ops.scan(TABLE_NAME, query_attrs)
    groups: List[str] = [
        get_key_or_fallback(group)
        for group in response
        if (
            group.get("historic_configuration") is not None
            and group["historic_configuration"][-1]["has_forces"]
        )
    ]
    return groups


async def is_valid(
    group_name: str, pre_computed_group_data: Optional[GroupType] = None
) -> bool:
    """Validate if a group exist and is not deleted."""
    group_name = group_name.lower()
    is_valid_group: bool = True
    if await exists(group_name, pre_computed_group_data):
        group_data = pre_computed_group_data or await get_attributes(
            group_name, ["deletion_date", "project_status"]
        )
        if get_key_or_fallback(
            group_data, "group_status", "project_status"
        ) != "ACTIVE" or group_data.get("deletion_date"):
            is_valid_group = False
    else:
        is_valid_group = False
    return is_valid_group


async def update(group_name: str, data: GroupType) -> bool:
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
        "Key": {"project_name": group_name.lower()},
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
        # By default updates on non-existent items create a new item
        # This condition disables that effect
        "ConditionExpression": Attr("project_name").exists(),
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


async def update_metadata_typed(
    *,
    group_name: str,
    metadata: GroupMetadataToUpdate,
) -> None:
    group_item = groups_utils.format_group_metadata_item(metadata)
    if group_item and not await update(group_name=group_name, data=group_item):
        raise ErrorUpdatingGroup.new()


async def update_state_typed(
    *,
    group_name: str,
    state: GroupState,
) -> None:
    new_state_item = groups_utils.format_group_state_item(state)
    group_item = await get_attributes(
        group_name=group_name,
        attributes=["historic_configuration"],
    )
    if new_state_item and not await update(
        group_name=group_name,
        data={
            "historic_configuration": [
                *group_item["historic_configuration"],
                new_state_item,
            ],
        },
    ):
        raise ErrorUpdatingGroup.new()
