"""Data Access Layer to the Forces tables."""

from typing import Any, AsyncIterator

# Standard library
from datetime import datetime
import logging

# Third party libraries
import aioboto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Local libraries
from backend.dal.helpers import dynamodb

# Constants
LOGGER = logging.getLogger(__name__)
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

    async with aioboto3.resource(**dynamodb.RESOURCE_OPTIONS) as resource:
        table = await resource.Table(TABLE_NAME)
        results = await table.query(
            KeyConditionExpression=key_condition_expresion,
            FilterExpression=filter_expression
        )

        for result in results['Items']:
            if 'accepted_exploits' not in result['vulnerabilities']:
                result['vulnerabilities']['accepted_exploits'] = []
            if 'integrates_exploits' not in result['vulnerabilities']:
                result['vulnerabilities']['integrates_exploits'] = []
            if 'exploits' not in result['vulnerabilities']:
                result['vulnerabilities']['exploits'] = []
            yield result

        while results.get('LastEvaluatedKey'):
            results = await table.query(
                KeyConditionExpression=key_condition_expresion,
                FilterExpression=filter_expression,
                ExclusiveStartKey=results['LastEvaluatedKey'])
            for result in results['Items']:
                yield result


async def create_execution(project_name: str,
                           **execution_attributes: Any) -> bool:
    """Create an execution of forces."""
    success = False
    try:
        execution_attributes['date'] = datetime.strftime(
            execution_attributes['date'], '%Y-%m-%dT%H:%M:%S.%f%z')

        execution_attributes['subscription'] = project_name
        success = await dynamodb.async_put_item(TABLE_NAME,
                                                execution_attributes)
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return success
