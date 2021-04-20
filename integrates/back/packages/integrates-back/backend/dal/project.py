"""DAL functions for projects."""

import logging
from typing import (
    Any,
    Dict,
    Optional,
)

import aioboto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.typing import Project as ProjectType
from groups import dal as groups_dal


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = 'FI_projects'


async def exists(
    project_name: str,
    pre_computed_project_data: Optional[Dict[str, str]] = None
) -> bool:
    project = project_name.lower()
    project_data = (
        pre_computed_project_data or
        await groups_dal.get_attributes(project, ['project_name'])
    )

    return bool(project_data)


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
            await groups_dal.get_attributes(
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
    project_data = await groups_dal.get_attributes(
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
