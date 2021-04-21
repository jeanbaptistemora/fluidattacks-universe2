# Standard libraries
import logging
import logging.config
from typing import (
    Any,
    cast,
    Dict,
    List,
    NamedTuple,
    Optional,
    Union,
)

# Third-party lbraries
import aioboto3
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import ClientError

# Local libraries
from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.typing import Project as GroupType


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = 'FI_projects'

ServicePolicy = NamedTuple('ServicePolicy', [('group', str), ('service', str)])


async def can_user_access(
    group_name: str,
    role: str,
    table: aioboto3.session.Session.client = None
) -> bool:
    group_data = await get_attributes(
        group_name.lower(),
        [
            'deletion_date',
            'historic_deletion',
            'project_name',
            'project_status',
        ],
        table
    )
    is_user_allowed = False
    if await is_alive(group_name, group_data):
        is_user_allowed = bool(role)
    return is_user_allowed


async def create(group: GroupType) -> bool:
    """Add group to dynamo."""
    resp = False
    try:
        resp = await dynamodb.async_put_item(TABLE_NAME, group)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return resp


async def exists(
    group_name: str,
    pre_computed_group_data: Optional[GroupType] = None
) -> bool:
    group = group_name.lower()
    group_data = (
        pre_computed_group_data or
        await get_attributes(group, ['project_name'])
    )
    return bool(group_data)


async def get_active_groups() -> List[str]:
    """Get active group in DynamoDB"""
    filtering_exp = (
        Attr('project_status').eq('ACTIVE') &
        Attr('project_status').exists()
    )
    groups = await get_all(filtering_exp, 'project_name')
    return cast(
        List[str],
        [group['project_name'] for group in groups]
    )


async def get_alive_groups(data_attr: str = '') -> List[GroupType]:
    """Get active and suspended groups in DynamoDB"""
    filtering_exp = (
        Attr('project_status').eq('ACTIVE') |
        Attr('project_status').eq('SUSPENDED')
    )
    groups: List[GroupType] = await get_all(filtering_exp, data_attr)
    return groups


async def get_all(
    filtering_exp: object = '',
    data_attr: str = ''
) -> List[GroupType]:
    """Get all groups"""
    scan_attrs = {}
    if filtering_exp:
        scan_attrs['FilterExpression'] = filtering_exp
    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr
    items = await dynamodb.async_scan(TABLE_NAME, scan_attrs)
    return cast(List[GroupType], items)


async def get_attributes(
    group_name: str,
    attributes: Optional[List[str]] = None,
    table: aioboto3.session.Session.client = None
) -> Dict[str, Union[str, List[str]]]:
    response = {}
    query_attrs = {
        'KeyConditionExpression': Key('project_name').eq(group_name),
        'Limit': 1
    }
    if attributes:
        projection = ','.join(attributes)
        query_attrs.update({'ProjectionExpression': projection})

    if not table:
        response_items = await dynamodb.async_query(TABLE_NAME, query_attrs)
    else:
        response_item = await table.query(**query_attrs)
        response_items = response_item.get('Items', [])

    if response_items:
        response = response_items[0]
    return response


async def get_description(group_name: str) -> str:
    """ Get the description of a project. """
    description = await get_attributes(group_name, ['description'])
    group_description = (
        str(description.get('description', ''))
        if description
        else ''
    )
    return group_description


async def get_group(
    group_name: str,
    table: aioboto3.session.Session.client
) -> GroupType:
    response = await table.get_item(Key={'project_name': group_name})
    return response.get('Item', {})


async def get_groups_with_forces() -> List[str]:
    filtering_exp = Attr('project_status').eq('ACTIVE')
    query_attrs = {
        "ProjectionExpression": "#name,#h_config",
        "FilterExpression": filtering_exp,
        "ExpressionAttributeNames": {
            "#name": "project_name",
            "#h_config": "historic_configuration",
        }
    }
    response = await dynamodb.async_scan(TABLE_NAME, query_attrs)
    groups: List[str] = [
        group['project_name']
        for group in response
        if (
            group.get('historic_configuration') is not None and
            group['historic_configuration'][-1]['has_forces']
        )
    ]
    return groups


async def get_service_policies(group: str) -> List[ServicePolicy]:
    """Return a list of policies for the given group."""
    policies: List[ServicePolicy] = []
    query_attrs = {
        'KeyConditionExpression': Key('project_name').eq(group.lower()),
        'ConsistentRead': True,
        'ProjectionExpression': 'historic_configuration, project_status'
    }
    response_items = await dynamodb.async_query(TABLE_NAME, query_attrs)

    # There is no such group, let's make an early return
    if not response_items:
        return policies

    group_attributes = response_items[0]
    historic_config: List[Dict[str, Any]] = group_attributes[
        'historic_configuration'
    ]
    has_drills: bool = historic_config[-1]['has_drills']
    has_forces: bool = historic_config[-1]['has_forces']
    has_integrates: bool = group_attributes['project_status'] == 'ACTIVE'
    type_: str = historic_config[-1]['type']
    if type_ == 'continuous':
        policies.append(ServicePolicy(group=group, service='continuous'))
        if has_integrates:
            policies.append(ServicePolicy(group=group, service='integrates'))
            if has_drills:
                policies.append(
                    ServicePolicy(group=group, service='drills_white')
                )
                if has_forces:
                    policies.append(
                        ServicePolicy(group=group, service='forces')
                    )
    elif type_ == 'oneshot':
        if has_integrates:
            policies.append(ServicePolicy(group=group, service='integrates'))
            policies.append(ServicePolicy(group=group, service='drills_black'))
    else:
        LOGGER.critical(
            'Group has invalid type attribute',
            extra={'extra': dict(group=group)})
    return policies


async def is_alive(
    group_name: str,
    pre_computed_group_data: Optional[GroupType] = None
) -> bool:
    """Validate if a group exist and is not deleted."""
    group_name = group_name.lower()
    is_valid_group: bool = True
    if await exists(group_name, pre_computed_group_data):
        group_data = (
            pre_computed_group_data or
            await get_attributes(
                group_name,
                ['deletion_date', 'project_status']
            )
        )
        if (
            group_data.get('project_status') != 'ACTIVE' or
            group_data.get('deletion_date')
        ):
            is_valid_group = False
    else:
        is_valid_group = False
    return is_valid_group


async def update(group_name: str, data: GroupType) -> bool:
    success = False
    set_expression = ''
    remove_expression = ''
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f'{attr}, '
        else:
            set_expression += f'{attr} = :{attr}, '
            expression_values.update({f':{attr}': value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        'Key': {'project_name': group_name.lower()},
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
        # By default updates on non-existent items create a new item
        # This condition disables that effect
        'ConditionExpression': Attr('project_name').exists(),
    }
    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    try:
        success = await dynamodb.async_update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success
