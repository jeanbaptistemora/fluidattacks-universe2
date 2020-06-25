# standard imports
import asyncio
import uuid
from typing import (
    cast,
    Dict,
    List,
    Optional
)

# third-party imports
import rollbar
from asgiref.sync import sync_to_async
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# local imports
from backend.dal.helpers.dynamodb import (
    async_query as dynamo_async_query,
    async_put_item as dynamo_async_put_item,
    async_update_item as dynamo_async_update_item,
    TABLE_NAME as OLD_TABLE_NAME
)
from backend.exceptions import InvalidOrganization
from backend.typing import (
    Dynamo as DynamoType,
    DynamoQuery as DynamoQueryType,
    Organization as OrganizationType
)

TABLE_NAME = 'fi_organizations'


def _map_keys_to_domain(org: OrganizationType) -> OrganizationType:
    """
    Map DynamoDB keys to a human-readable form
    """
    mapping = {
        'pk': 'id',
        'sk': 'name'
    }
    mapped_org = {
        key: org[key]
        for key in org
        if key not in mapping
    }
    mapped_org.update({
        mapping[key]: org[key]
        for key in org
        if key in mapping
    })
    return mapped_org


def _map_keys_to_dal(org: OrganizationType) -> OrganizationType:
    """
    Map domain keys to its DynamoDB representation
    """
    mapping = {
        'id': 'pk',
        'name': 'sk'
    }
    mapped_org = {
        key: org[key]
        for key in org
        if key not in mapping
    }
    mapped_org.update({
        mapping[key]: org[key]
        for key in org
        if key in mapping
    })
    return mapped_org


def _map_attributes_to_dal(attrs: List[str]) -> List[str]:
    """
    Map domain attributes to its DynamoDB representation
    """
    mapping = {
        'id': 'pk',
        'name': 'sk'
    }
    mapped_attrs = [
        attr
        for attr in attrs
        if attr not in mapping
    ]
    mapped_attrs.extend([
        mapping[attr]
        for attr in attrs
        if attr in mapping
    ])
    return mapped_attrs


async def add_group(organization_id: str, group: str) -> None:
    new_item = {
        'pk': organization_id,
        'sk': f'GROUP#{group}'
    }
    try:
        await dynamo_async_put_item(TABLE_NAME, new_item)
    except ClientError as ex:
        await sync_to_async(rollbar.report_message)(
            'Error adding group to organization',
            'error',
            extra_data=ex,
            payload_data=locals()
        )


async def add_user(organization_id: str, email: str) -> None:
    new_item = {
        'pk': organization_id,
        'sk': f'USER#{email}'
    }
    try:
        await dynamo_async_put_item(TABLE_NAME, new_item)
    except ClientError as ex:
        await sync_to_async(rollbar.report_message)(
            'Error adding user to organization',
            'error',
            extra_data=ex,
            payload_data=locals()
        )


async def create(organization_name: str) -> OrganizationType:
    """
    Create an organization and returns its key
    """
    org_exists = await exists(organization_name)
    if org_exists:
        raise InvalidOrganization()

    new_item: OrganizationType = {
        'pk': 'ORG#{}'.format(str(uuid.uuid4())),
        'sk': organization_name.lower()
    }

    try:
        await asyncio.gather(*[
            asyncio.create_task(
                dynamo_async_put_item(table, new_item)
            )
            for table in [OLD_TABLE_NAME, TABLE_NAME]
        ])
    except ClientError as ex:
        await sync_to_async(rollbar.report_message)(
            'Error creating organization',
            'error',
            extra_data=ex,
            payload_data=locals()
        )
    return _map_keys_to_domain(new_item)


async def exists(org_name: str) -> bool:
    """
    Returns True if the organization key exists
    """
    org = await get(org_name)
    resp = False
    if org:
        resp = True
    return resp


async def get(org_name: str,
              attributes: List[str] = None) -> Optional[OrganizationType]:
    """
    Get an organization info given its name
    Return specified attributes or all if not setted
    """
    query_attrs = {
        'KeyConditionExpression': Key('sk').eq(org_name) &
        Key('pk').begins_with('ORG#'),
        'IndexName': 'gsi-1',
        'Limit': 1
    }
    if attributes:
        projection = ','.join(_map_attributes_to_dal(attributes))
        query_attrs['ProjectionExpression'] = projection
    org = None
    try:
        response_items = cast(
            List[OrganizationType],
            await dynamo_async_query(OLD_TABLE_NAME, query_attrs)
        )
        if response_items:
            org = _map_keys_to_domain(response_items[0])
    except ClientError as ex:
        await sync_to_async(rollbar.report_message)(
            'Error fetching organization attributes',
            'error',
            extra_data=ex,
            payload_data=locals()
        )
    return org


async def get_by_id(
    organization_id: str,
    attributes: List[str] = None
) -> OrganizationType:
    """
    Use the organization ID to fetch general information about it
    """
    organization: OrganizationType = {}
    query_attrs = {
        'KeyConditionExpression': (
            Key('pk').eq(organization_id) &
            Key('sk').begins_with('INFO')
        )
    }

    if attributes:
        projection = ','.join(_map_attributes_to_dal(attributes))
        query_attrs.update({'ProjectionExpression': projection})

    try:
        response_item = cast(
            List[OrganizationType],
            await dynamo_async_query(TABLE_NAME, query_attrs)
        )
        if response_item:
            organization = response_item[0]
            if 'sk' in organization:
                organization.update({
                    'sk': cast(str, organization['sk']).split('#')[1]
                })
    except ClientError as ex:
        await sync_to_async(rollbar.report_message)(
            'Error fetching organization info by their ID',
            'error',
            extra_data=ex,
            payload_data=locals()
        )
    return _map_keys_to_domain(organization)


async def get_many_by_id(
    organization_ids: List[str],
    attributes: List[str] = None
) -> List[OrganizationType]:
    """
    Use the organization ID to fetch general information about it
    """
    return await asyncio.gather(*[
        asyncio.create_task(
            get_by_id(org_id, attributes)
        )
        for org_id in organization_ids
    ])


async def get_id_for_group(group_name: str) -> str:
    """
    Return the ID of the organization a group belongs to
    """
    organization_id: str = ''
    query_attrs: DynamoQueryType = {
        'KeyConditionExpression': Key('sk').eq(f'GROUP#{group_name}'),
        'IndexName': 'gsi-1',
        'ProjectionExpression': 'pk'
    }
    try:
        response_item = cast(
            List[OrganizationType],
            await dynamo_async_query(TABLE_NAME, query_attrs)
        )
        if response_item:
            organization_id = cast(str, response_item[0]['pk'])
    except ClientError as ex:
        await sync_to_async(rollbar.report_message)(
            'Error fetching the organization a group belongs to',
            'error',
            extra_data=ex,
            payload_data=locals()
        )
    return organization_id


async def get_ids_for_user(email: str) -> List[str]:
    """
    Return the IDs of all the organizations a user belongs to
    """
    organization_ids: List[str] = []
    query_attrs = {
        'KeyConditionExpression': Key('sk').eq(f'USER#{email}'),
        'IndexName': 'gsi-1',
        'ProjectionExpression': 'pk'
    }
    try:
        response_items = cast(
            List[OrganizationType],
            await dynamo_async_query(TABLE_NAME, query_attrs)
        )
        if response_items:
            organization_ids = [
                cast(str, item['pk'])
                for item in response_items
            ]
    except ClientError as ex:
        await sync_to_async(rollbar.report_message)(
            'Error fetching user organizations',
            'error',
            extra_data=ex,
            payload_data=locals()
        )
    return organization_ids


async def get_or_create(organization_name: str) -> OrganizationType:
    """
    Return an organization, even if it does not exists,
    in which case it will be created
    """
    org_name = organization_name.lower()
    org = await get(org_name, ['id', 'name'])
    if not org:
        org = await create(org_name)
    return org


async def get_groups(organization_id: str) -> List[str]:
    """
    Return a list of the names of all the groups that belong to an
    organization
    """
    groups: List[str] = []
    query_attrs = {
        'KeyConditionExpression': Key('pk').eq(organization_id) &
        Key('sk').begins_with('GROUP#')
    }
    try:
        response_items = cast(
            List[OrganizationType],
            await dynamo_async_query(TABLE_NAME, query_attrs)
        )
        if response_items:
            groups = [
                cast(str, item['sk']).split('#')[1]
                for item in response_items
            ]
    except ClientError as ex:
        await sync_to_async(rollbar.report_message)(
            'Error fetching groups from an organiation',
            'error',
            extra_data=ex,
            payload_data=locals()
        )
    return groups


async def get_users(organization_id: str) -> List[str]:
    """
    Return a list of the emails of all the users that belong to an
    organization
    """
    users: List[str] = []
    query_attrs = {
        'KeyConditionExpression': Key('pk').eq(organization_id) &
        Key('sk').begins_with('USER#')
    }
    try:
        response_items = cast(
            List[OrganizationType],
            await dynamo_async_query(TABLE_NAME, query_attrs)
        )
        if response_items:
            users = [
                cast(str, item['sk']).split('#')[1]
                for item in response_items
            ]
    except ClientError as ex:
        await sync_to_async(rollbar.report_message)(
            'Error fetching users from an organiation',
            'error',
            extra_data=ex,
            payload_data=locals()
        )
    return users


async def update(
    organization_id: str,
    organization_name: str,
    values: OrganizationType
) -> bool:
    """
    Updates the attributes of an organization
    """
    success: bool = False
    set_expression: str = ''
    remove_expression: str = ''
    expression_values: OrganizationType = {}
    for attr, value in values.items():
        if value is None:
            remove_expression += f'{attr}, '
        else:
            set_expression += f'{attr} = :{attr}, '
            expression_values.update({f':{attr}': value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'

    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    try:
        update_attrs: Dict[str, DynamoType] = {
            'Key': {
                'pk': organization_id,
                'sk': f'INFO#{organization_name}'
            },
            'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
            'ExpressionAttributeValues': expression_values
        }
        success = await dynamo_async_update_item(TABLE_NAME, update_attrs)
    except ClientError as exe:
        await sync_to_async(rollbar.report_message)(
            'There was an error updating the settings of an organization',
            'error',
            extra_data=exe,
            payload_data=locals()
        )
    return success
