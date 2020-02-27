"""Data Access Layer to the Break Build tables."""

from typing import Generator

# Standard library
from datetime import datetime

# Third party libraries
from boto3.dynamodb.conditions import Key, Attr

# Local libraries
from backend.dal.helpers import dynamodb

# Constants
TABLE = dynamodb.DYNAMODB_RESOURCE.Table('bb_executions')  # type: ignore


def yield_executions(
        project_name: str,
        from_date: datetime,
        to_date: datetime) -> Generator:
    """ Lazy iterator over the executions of a project """
    key_condition_expresion = \
        Key('subscription').eq(project_name)

    filter_expression = \
        Attr('date').gte(from_date.isoformat()) \
        & Attr('date').lte(to_date.isoformat())

    results = TABLE.query(
        KeyConditionExpression=key_condition_expresion,
        FilterExpression=filter_expression)

    yield from results['Items']

    while results.get('LastEvaluatedKey'):
        results = TABLE.query(
            KeyConditionExpression=key_condition_expresion,
            FilterExpression=filter_expression,
            ExclusiveStartKey=results['LastEvaluatedKey'])

        yield from results['Items']
