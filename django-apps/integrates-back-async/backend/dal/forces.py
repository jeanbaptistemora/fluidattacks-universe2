"""Data Access Layer to the Forces tables."""

from typing import AsyncIterator

# Standard library
from datetime import datetime
import logging

# Third party libraries
from asgiref.sync import sync_to_async
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Local libraries
from backend.dal.helpers import dynamodb

# Constants
LOGGER = logging.getLogger(__name__)
TABLE = dynamodb.DYNAMODB_RESOURCE.Table('bb_executions')  # type: ignore
TABLE_NAME = 'bb_executions'


async def yield_executions(
        project_name: str,
        from_date: datetime,
        to_date: datetime) -> AsyncIterator:
    """ Lazy iterator over the executions of a project """
    key_condition_expresion = \
        Key('subscription').eq(project_name)

    filter_expression = \
        Attr('date').gte(from_date.isoformat()) \
        & Attr('date').lte(to_date.isoformat())

    results = await sync_to_async(TABLE.query)(
        KeyConditionExpression=key_condition_expresion,
        FilterExpression=filter_expression)

    for result in results['Items']:
        yield result

    while results.get('LastEvaluatedKey'):
        results = await sync_to_async(TABLE.query)(
            KeyConditionExpression=key_condition_expresion,
            FilterExpression=filter_expression,
            ExclusiveStartKey=results['LastEvaluatedKey'])
        for result in results['Items']:
            yield result


async def create_execution(project_name: str,
                           **execution_attributes: str) -> bool:
    """Create an execution of forces."""
    success = False
    try:
        execution_attributes['subscription'] = project_name
        success = await dynamodb.async_put_item(TABLE_NAME,
                                                execution_attributes)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success
