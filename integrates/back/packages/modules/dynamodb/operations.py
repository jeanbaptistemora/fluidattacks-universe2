# Standard
from typing import Any, Dict, Optional, Tuple, Union

# Third party
import aioboto3
import aioextensions
import botocore
from boto3.dynamodb.conditions import ConditionBase

# Local
from dynamodb.types import Facet, Index, Item, PrimaryKey, Table
from newutils.context import (
    AWS_DYNAMODB_ACCESS_KEY,
    AWS_DYNAMODB_SECRET_KEY,
    AWS_SESSION_TOKEN,
    DYNAMODB_HOST,
    DYNAMODB_PORT,
    ENVIRONMENT
)


def _get_resource_options() -> Dict[str, Optional[str]]:
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


RESOURCE_OPTIONS = _get_resource_options()


def _build_query_attrs(
    *,
    condition_expression: ConditionBase,
    facets: Tuple[Facet, ...],
    index: Optional[Index],
    table: Table,
) -> Dict[str, Any]:
    facet_attrs = tuple({
        attr
        for facet in facets
        for attr in facet.attrs
    })
    key_source: Union[Index, Table] = index if index else table
    key_structure = key_source.primary_key
    attrs = (
        key_structure.partition_key,
        key_structure.sort_key,
        *facet_attrs
    )
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
        query_attrs = _build_query_attrs(
            condition_expression=condition_expression,
            facets=facets,
            index=index,
            table=table
        )
        response = await table_resource.query(**query_attrs)
        items = response.get('Items', list())

        while response.get('LastEvaluatedKey'):
            response = await table_resource.query(
                **query_attrs,
                ExclusiveStartKey=response.get('LastEvaluatedKey')
            )
            items += response.get('Items', list())

    return tuple(items)


def _build_facet_item(
    *,
    facet: Facet,
    item: Item,
    table: Table,
) -> Item:
    key_structure = table.primary_key
    attrs = (
        key_structure.partition_key,
        key_structure.sort_key,
        *facet.attrs
    )
    return {
        attr: item[attr]
        for attr in attrs
    }


async def put_item(
    *,
    facet: Facet,
    item: Item,
    table: Table
) -> None:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource = await resource.Table(table.name)
        facet_item = _build_facet_item(
            facet=facet,
            item=item,
            table=table
        )
        await table_resource.put_item(Item=facet_item)


async def batch_write_item(
    *,
    items: Tuple[Item, ...],
    table: Table,
) -> None:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource = await resource.Table(table.name)
        async with table_resource.batch_writer() as batch_writer:
            await aioextensions.collect(tuple(
                batch_writer.put_item(Item=item)
                for item in items
            ))


async def update_item(
    *,
    item: Item,
    key: PrimaryKey,
    table: Table
) -> None:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource = await resource.Table(table.name)
        update_attrs = ','.join(f'#{attr} = :{attr}' for attr in item)
        table_resource.update_item(
            ExpressionAttributeNames={f'#{attr}': attr for attr in item},
            ExpressionAttributeValues={
                f':{attr}': value
                for (attr, value) in item.items()
            },
            Key=dict(key._asdict()),
            UpdateExpression=f'SET {update_attrs}'
        )


def _build_delete_attrs(
    *,
    primary_key: PrimaryKey,
    table: Table
) -> Dict[str, Any]:
    key_structure = table.primary_key
    return {
        'Key': {
            key_structure.partition_key: primary_key.partition_key,
            key_structure.sort_key: primary_key.sort_key,
        }
    }


async def delete_item(
    *,
    primary_key: PrimaryKey,
    table: Table
) -> None:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource = await resource.Table(table.name)
        delete_attrs = _build_delete_attrs(
            primary_key=primary_key,
            table=table
        )
        await table_resource.delete_item(**delete_attrs)
