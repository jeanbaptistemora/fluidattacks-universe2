# Standard
from typing import Any, Dict, Optional, Tuple

# Third party
import aioboto3
import botocore
from boto3.dynamodb.conditions import ConditionBase

# Local
from dynamodb.types import Facet, Index, Item, Table
from newutils.context import (
    AWS_DYNAMODB_ACCESS_KEY,
    AWS_DYNAMODB_SECRET_KEY,
    AWS_SESSION_TOKEN,
    DYNAMODB_HOST,
    DYNAMODB_PORT,
    ENVIRONMENT
)


def get_resource_options() -> Dict[str, Optional[str]]:
    basic_options = {
        'service_name': 'dynamodb',
        'aws_access_key_id': AWS_DYNAMODB_ACCESS_KEY,
        'aws_secret_access_key': AWS_DYNAMODB_SECRET_KEY,
        'aws_session_token': AWS_SESSION_TOKEN,
        'region_name': 'us-east-1',
        'config': botocore.config.Config(
            max_pool_connections=50,
        )
    }

    if ENVIRONMENT == 'development' and DYNAMODB_HOST:
        return {
            **basic_options,
            'endpoint_url': f'http://{DYNAMODB_HOST}:{DYNAMODB_PORT}'
        }

    return basic_options


RESOURCE_OPTIONS = get_resource_options()


def build_query_attrs(
    *,
    condition_expression: ConditionBase,
    facets: Tuple[Facet, ...],
    index: Optional[Index],
) -> Dict[str, Any]:
    attrs = tuple({
        attr
        for facet in facets
        for attr in facet.attrs
    })
    basic_attrs = {
        'ExpressionAttributeNames': {f'#{attr}': attr for attr in attrs},
        'KeyConditionExpression': condition_expression,
        'ProjectionExpression': ','.join([f'#{attr}' for attr in attrs])
    }

    if index:
        return {**basic_attrs, 'IndexName': index.name}

    return basic_attrs


async def query(
    *,
    condition_expression: ConditionBase,
    facets: Tuple[Facet, ...],
    index: Optional[Index],
    table: Table
) -> Tuple[Item, ...]:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource = await resource.Table(table.name)
        query_attrs = build_query_attrs(
            condition_expression=condition_expression,
            facets=facets,
            index=index,
        )
        response = await table_resource.query(**query_attrs)
        items = response.get('Items', [])

        while response.get('LastEvaluatedKey'):
            response = await table_resource.query(
                **query_attrs,
                ExclusiveStartKey=response.get('LastEvaluatedKey')
            )
            items += response.get('Items', [])

    return tuple(items)
