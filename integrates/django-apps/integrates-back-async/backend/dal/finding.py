"""DAL functions for findings."""
import logging
from typing import Any, cast, Dict, List

import aioboto3
from boto3.dynamodb.conditions import And, Attr, Equals, Key
from botocore.exceptions import ClientError

from backend.dal.helpers import s3, dynamodb
from backend.typing import Finding as FindingType
from backend.utils import datetime as datetime_utils
from fluidintegrates.settings import LOGGING
from __init__ import FI_AWS_S3_BUCKET

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = 'FI_findings'


def _escape_alnum(string: str) -> str:
    """ Removes non-alphanumeric characters from a string """
    return ''.join([
        char
        for char in string
        if char.isalnum()
    ])


async def create(
        finding_id: str,
        project_name: str,
        finding_attrs: Dict[str, FindingType]) -> bool:
    success = False
    try:
        finding_attrs.update({
            'finding_id': finding_id,
            'project_name': project_name
        })
        success = await dynamodb.async_put_item(TABLE_NAME, finding_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success


async def update(finding_id: str, data: Dict[str, FindingType]) -> bool:
    success = False
    set_expression = ''
    remove_expression = ''
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f'{attr}, '
        else:
            set_expression += f'{attr} = :{_escape_alnum(attr)}, '
            expression_values.update({f':{_escape_alnum(attr)}': value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        'Key': {
            'finding_id': finding_id
        },
        'UpdateExpression': f'{set_expression} {remove_expression}'.strip(),
    }
    if expression_values:
        update_attrs.update({'ExpressionAttributeValues': expression_values})
    try:
        success = await dynamodb.async_update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return success


async def list_append(
        finding_id: str,
        attr: str,
        data: List[FindingType]) -> bool:
    """
    Adds elements to the end of a list attribute

    :param finding_id: id of the finding to update
    :param attr: attribute name
    :param data: list with the elements to append
    """
    success = False
    try:
        update_attrs = {
            'Key': {
                'finding_id': finding_id
            },
            'UpdateExpression': f'SET {attr} = list_append({attr}, :data)',
            'ExpressionAttributeValues': {':data': data}
        }
        success = await dynamodb.async_update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return success


async def get_attributes(
        finding_id: str, attributes: List[str]) -> Dict[str, FindingType]:
    """ Get a group of attributes of a finding. """
    finding_attrs: Dict[str, FindingType] = {}
    item_attrs = {
        'KeyConditionExpression': Key('finding_id').eq(finding_id)
    }
    if attributes:
        projection = ','.join(attributes)
        item_attrs.update({'ProjectionExpression': projection})
    response_item = cast(
        List[Dict[str, FindingType]],
        await dynamodb.async_query(TABLE_NAME, item_attrs)
    )
    if response_item:
        finding_attrs = response_item[0]
    return finding_attrs


async def get_finding(finding_id: str) -> Dict[str, FindingType]:
    """ Retrieve all attributes from a finding """
    response = {}
    query_attrs = {
        'KeyConditionExpression': Key('finding_id').eq(finding_id),
        'Limit': 1
    }
    response_items = await dynamodb.async_query(TABLE_NAME, query_attrs)
    if response_items:
        response = response_items[0]

    return response


async def get(
        finding_id: str,
        table: aioboto3.session.Session.client) -> Dict[str, FindingType]:
    response = await table.get_item(Key={'finding_id': finding_id})
    return response.get('Item', {})


async def save_evidence(file_object: object, file_name: str) -> bool:
    return await s3.upload_memory_file(  # type: ignore
        FI_AWS_S3_BUCKET,
        file_object,
        file_name
    )


async def search_evidence(file_name: str) -> List[str]:
    return await s3.list_files(FI_AWS_S3_BUCKET, file_name)  # type: ignore


async def remove_evidence(file_name: str) -> bool:
    return await s3.remove_file(FI_AWS_S3_BUCKET, file_name)  # type: ignore


async def download_evidence(file_name: str, file_path: str):
    await s3.download_file(  # type: ignore
        FI_AWS_S3_BUCKET,
        file_name,
        file_path
    )


async def get_findings_by_group(group_name: str) -> List[Dict[str, Any]]:
    key_exp: Equals = Key('project_name').eq(group_name)
    today: str = datetime_utils.get_as_str(datetime_utils.get_now())
    filter_exp: And = (
        Attr('releaseDate').exists() &
        Attr('releaseDate').lte(today)
    )

    return await dynamodb.async_query(
        TABLE_NAME,
        {
            'FilterExpression': filter_exp,
            'IndexName': 'project_findings',
            'KeyConditionExpression': key_exp
        }
    )
