import aioboto3
from aioboto3.dynamodb.table import (
    CustomTableResource,
)
import aioextensions
from boto3.dynamodb.conditions import (
    ConditionBase,
)
import botocore
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    FI_AWS_SESSION_TOKEN,
    FI_DYNAMODB_HOST,
    FI_DYNAMODB_PORT,
    FI_ENVIRONMENT,
)
from dynamodb.exceptions import (
    handle_error,
)
from dynamodb.types import (
    Facet,
    Index,
    Item,
    PrimaryKey,
    Table,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def _get_resource_options() -> Dict[str, Optional[str]]:
    basic_options = {
        "service_name": "dynamodb",
        "aws_access_key_id": FI_AWS_DYNAMODB_ACCESS_KEY,
        "aws_secret_access_key": FI_AWS_DYNAMODB_SECRET_KEY,
        "aws_session_token": FI_AWS_SESSION_TOKEN,
        "region_name": "us-east-1",
        "config": botocore.config.Config(
            max_pool_connections=50,
        ),
    }
    if FI_ENVIRONMENT == "development" and FI_DYNAMODB_HOST:
        return {
            **basic_options,
            "endpoint_url": f"http://{FI_DYNAMODB_HOST}:{FI_DYNAMODB_PORT}",
        }
    return basic_options


RESOURCE_OPTIONS = _get_resource_options()


def _build_facet_item(*, facet: Facet, item: Item, table: Table) -> Item:
    key_structure = table.primary_key
    attrs = (key_structure.partition_key, key_structure.sort_key, *facet.attrs)
    return {attr: item[attr] for attr in attrs}


def _build_query_args(
    *,
    condition_expression: ConditionBase,
    facets: Tuple[Facet, ...],
    filter_expression: Optional[ConditionBase],
    index: Optional[Index],
    table: Table,
) -> Dict[str, Any]:
    facet_attrs = tuple({attr for facet in facets for attr in facet.attrs})
    key_source: Union[Index, Table] = index if index else table
    key_structure = key_source.primary_key
    attrs = (key_structure.partition_key, key_structure.sort_key, *facet_attrs)
    args = {
        "ExpressionAttributeNames": {f"#{attr}": attr for attr in attrs},
        "FilterExpression": filter_expression,
        "IndexName": index.name if index else None,
        "KeyConditionExpression": condition_expression,
        "ProjectionExpression": ",".join([f"#{attr}" for attr in attrs]),
    }
    return _exclude_none(args=args)


def _exclude_none(*, args: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in args.items() if value is not None}


async def batch_write_item(*, items: Tuple[Item, ...], table: Table) -> None:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)

        async with table_resource.batch_writer() as batch_writer:
            try:
                await aioextensions.collect(
                    tuple(batch_writer.put_item(Item=item) for item in items)
                )
            except ClientError as error:
                handle_error(error=error)


async def delete_item(
    *,
    condition_expression: Optional[ConditionBase] = None,
    primary_key: PrimaryKey,
    table: Table,
) -> None:
    key_structure = table.primary_key

    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)
        args = {
            "ConditionExpression": condition_expression,
            "Key": {
                key_structure.partition_key: primary_key.partition_key,
                key_structure.sort_key: primary_key.sort_key,
            },
        }

        try:
            await table_resource.delete_item(**_exclude_none(args=args))
        except ClientError as error:
            handle_error(error=error)


async def put_item(
    *,
    condition_expression: Optional[ConditionBase] = None,
    facet: Facet,
    item: Item,
    table: Table,
) -> None:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)
        facet_item = _build_facet_item(facet=facet, item=item, table=table)
        args = {
            "ConditionExpression": condition_expression,
            "Item": {
                attr: value
                for attr, value in facet_item.items()
                if value is not None
            },
        }

        try:
            await table_resource.put_item(**_exclude_none(args=args))
        except ClientError as error:
            handle_error(error=error)


async def query(
    *,
    condition_expression: ConditionBase,
    facets: Tuple[Facet, ...],
    filter_expression: Optional[ConditionBase] = None,
    index: Optional[Index] = None,
    table: Table,
) -> Tuple[Item, ...]:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)
        query_args = _build_query_args(
            condition_expression=condition_expression,
            facets=facets,
            filter_expression=filter_expression,
            index=index,
            table=table,
        )

        try:
            response = await table_resource.query(**query_args)
            items: List[Item] = response.get("Items", list())
            while response.get("LastEvaluatedKey"):
                response = await table_resource.query(
                    **query_args,
                    ExclusiveStartKey=response.get("LastEvaluatedKey"),
                )
                items += response.get("Items", list())
        except ClientError as error:
            handle_error(error=error)
    return tuple(items)


async def update_item(
    *,
    condition_expression: Optional[ConditionBase] = None,
    item: Item,
    key: PrimaryKey,
    table: Table,
) -> None:
    key_structure = table.primary_key
    attr_names = {f"#{attr}": attr for attr in item}
    attr_values = {
        f":{attr}": value for attr, value in item.items() if value is not None
    }
    attrs_to_update = ",".join(
        f"#{attr} = :{attr}"
        for attr, value in item.items()
        if value is not None
    )
    attrs_to_remove = ",".join(
        f"#{attr}" for attr, value in item.items() if value is None
    )
    update_expressions = []
    if attrs_to_update:
        update_expressions.append(f"SET {attrs_to_update}")
    if attrs_to_remove:
        update_expressions.append(f"REMOVE {attrs_to_remove}")

    async with aioboto3.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)
        args = {
            "ConditionExpression": condition_expression,
            "ExpressionAttributeNames": attr_names,
            "ExpressionAttributeValues": attr_values,
            "Key": {
                key_structure.partition_key: key.partition_key,
                key_structure.sort_key: key.sort_key,
            },
            "UpdateExpression": " ".join(update_expressions),
        }

        try:
            await table_resource.update_item(**_exclude_none(args=args))
        except ClientError as error:
            handle_error(error=error)
