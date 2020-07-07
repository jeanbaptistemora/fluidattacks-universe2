"""DAL functions for findings."""

from typing import cast, Dict, List

import aioboto3
from asgiref.sync import async_to_sync
from boto3.dynamodb.conditions import Key
import rollbar
from botocore.exceptions import ClientError

from backend.typing import Finding as FindingType
from backend.dal.helpers import s3, dynamodb
from backend.dal.vulnerability import get_vulnerabilities
from backend.utils import aio
from __init__ import FI_AWS_S3_BUCKET

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('FI_findings')
TABLE_NAME: str = 'FI_findings'


def _escape_alnum(string: str) -> str:
    """ Removes non-alphanumeric characters from a string """
    return ''.join([
        char
        for char in string
        if char.isalnum()
    ])


def create(finding_id: str, project_name: str,
           finding_attrs: Dict[str, FindingType]) -> bool:
    success = False
    try:
        finding_attrs.update({
            'finding_id': finding_id,
            'project_name': project_name
        })
        response = TABLE.put_item(Item=finding_attrs)
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message(
            'Error: Couldn\'nt create draft',
            'error',
            extra_data=ex,
            payload_data=locals()
        )
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
        await aio.ensure_io_bound(
            rollbar.report_message,
            'Error: Couldn\'nt update finding',
            'error',
            extra_data=ex,
            payload_data=locals()
        )

    return success


def list_append(finding_id: str, attr: str, data: List[FindingType]) -> bool:
    """
    Adds elements to the end of a list attribute

    :param finding_id: id of the finding to update
    :param attr: attribute name
    :param data: list with the elements to append
    """
    success = False
    primary_keys = {'finding_id': finding_id}
    try:
        response = TABLE.update_item(
            Key=primary_keys,
            UpdateExpression=f'SET {attr} = list_append({attr}, :data)',
            ExpressionAttributeValues={':data': data}
        )
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message(
            'Error: Couldn\'nt update finding',
            'error',
            extra_data=ex,
            payload_data=locals()
        )

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


@async_to_sync
async def save_evidence(file_object: object, file_name: str) -> bool:
    return await s3.upload_memory_file(  # type: ignore
        FI_AWS_S3_BUCKET,
        file_object,
        file_name
    )


@async_to_sync
async def search_evidence(file_name: str) -> List[str]:
    return await s3.list_files(FI_AWS_S3_BUCKET, file_name)  # type: ignore


@async_to_sync
async def remove_evidence(file_name: str) -> bool:
    return await s3.remove_file(FI_AWS_S3_BUCKET, file_name)  # type: ignore


@async_to_sync
async def download_evidence(file_name: str, file_path: str):
    await s3.download_file(  # type: ignore
        FI_AWS_S3_BUCKET,
        file_name,
        file_path
    )


async def is_pending_verification(finding_id: str) -> bool:
    finding = await get_attributes(
        finding_id,
        [
            'finding_id',
            'historic_state',
            'historic_verification'
        ]
    )
    last_verification = cast(
        List[Dict[str, str]],
        finding.get('historic_verification', [{}])
    )[-1]
    last_state = cast(
        List[Dict[str, str]],
        finding.get('historic_state', [{}])
    )[-1]
    resp = (
        last_verification.get('status') == 'REQUESTED' and
        not last_verification.get('vulns')
    )
    if not resp:
        vulns = await aio.ensure_io_bound(get_vulnerabilities, finding_id)
        open_vulns = [
            vuln
            for vuln in vulns
            if cast(
                List[Dict[str, str]],
                vuln.get('historic_state', [{}])
            )[-1].get('state') == 'open'
        ]
        remediated_vulns = [
            vuln
            for vuln in open_vulns
            if cast(
                List[Dict[str, str]],
                vuln.get('historic_verification', [{}])
            )[-1].get('status') == 'REQUESTED'
        ]
        resp = len(remediated_vulns) != 0
    return resp and last_state.get('state') != 'DELETED'
