"""DAL functions for projects."""

import logging
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Union,
)

import aioboto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr, Key

from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.typing import Project as ProjectType
from groups import dal as groups_dal


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = 'FI_projects'


async def get_groups_with_forces() -> List[str]:
    """Get active project in DynamoDB"""
    filtering_exp = (
        Attr('project_status').eq('ACTIVE')
    )
    query_attrs = {
        "ProjectionExpression": "#name,#h_config",
        "FilterExpression": filtering_exp,
        "ExpressionAttributeNames": {
            "#name": "project_name",
            "#h_config": "historic_configuration",
        },
    }
    response = await dynamodb.async_scan(TABLE_NAME, query_attrs)
    projects = [
        project['project_name'] for project in response
        if project.get('historic_configuration') is not None
        and project['historic_configuration'][-1]['has_forces']
    ]

    return cast(List[str], projects)


async def get_alive_groups(
    data_attr: str = ''
) -> List[ProjectType]:
    """Get active and suspended projects in DynamoDB"""
    filtering_exp = (
        Attr('project_status').eq('ACTIVE') |
        Attr('project_status').eq('SUSPENDED')
    )
    groups = await groups_dal.get_all(filtering_exp, data_attr)
    return cast(List[ProjectType], groups)


async def get_group(
        group_name: str,
        table: aioboto3.session.Session.client) -> ProjectType:
    response = await table.get_item(Key={'project_name': group_name})
    return response.get('Item', {})


async def get_description(project: str) -> str:
    """ Get the description of a project. """
    description = await get_attributes(project, ['description'])
    project_description = ''
    if description:
        project_description = str(description.get('description', ''))
    else:
        # project without description
        pass
    return project_description


async def exists(
    project_name: str,
    pre_computed_project_data: Optional[Dict[str, str]] = None
) -> bool:
    project = project_name.lower()
    project_data = (
        pre_computed_project_data or
        await get_attributes(project, ['project_name'])
    )

    return bool(project_data)


async def get_attributes(
    project_name: str,
    attributes: Optional[List[str]] = None,
    table: aioboto3.session.Session.client = None
) -> Dict[str, Union[str, List[str]]]:
    response = {}
    query_attrs = {
        'KeyConditionExpression': Key('project_name').eq(project_name),
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


async def is_alive(
    project: str,
    pre_computed_project_data: Optional[Dict[str, Any]] = None
) -> bool:
    """Validate if a project exist and is not deleted."""
    project_name = project.lower()
    is_valid_project = True
    if await exists(project_name, pre_computed_project_data):
        project_data = (
            pre_computed_project_data or
            await get_attributes(
                project_name.lower(),
                ['deletion_date', 'project_status']
            )
        )
        if project_data.get('project_status') != 'ACTIVE' or \
           project_data.get('deletion_date'):
            is_valid_project = False
    else:
        is_valid_project = False
    return is_valid_project


async def can_user_access(
        project: str,
        role: str,
        table: aioboto3.session.Session.client = None) -> bool:
    project_data = await get_attributes(
        project.lower(),
        [
            'deletion_date',
            'historic_deletion',
            'project_name',
            'project_status',
        ],
        table
    )

    is_user_allowed = False
    if await is_alive(project, project_data):
        is_user_allowed = bool(role)
    return is_user_allowed


async def update(project_name: str, data: ProjectType) -> bool:
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
        'Key': {'project_name': project_name.lower()},
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


async def create(project: ProjectType) -> bool:
    """Add project to dynamo."""
    resp = False
    try:
        resp = await dynamodb.async_put_item(TABLE_NAME, project)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return resp
