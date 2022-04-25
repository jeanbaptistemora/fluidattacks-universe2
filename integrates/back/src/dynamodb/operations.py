from .utils import (
    get_cursor,
    get_key_from_cursor,
)
from aioboto3.dynamodb.table import (
    BatchWriter,
    CustomTableResource,
)
import aioextensions
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    ConditionBase,
)
from botocore.exceptions import (
    ClientError,
)
from decimal import (
    Decimal,
)
from dynamodb.exceptions import (
    handle_error,
)
from dynamodb.resource import (
    RESOURCE_OPTIONS,
    SESSION,
)
from dynamodb.types import (
    Facet,
    Index,
    Item,
    PageInfo,
    PrimaryKey,
    QueryResponse,
    Table,
)
from itertools import (
    chain,
)
from more_itertools import (
    chunked,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)


# Fix for https://github.com/boto/boto3/pull/2867
class PatchedBatchWriter(BatchWriter):
    async def _flush(self) -> None:
        items_to_send = self._items_buffer[
            : self._flush_amount
        ]  # type: List[Item]
        self._items_buffer = self._items_buffer[
            self._flush_amount :
        ]  # type: List[Item]
        response = await self._client.batch_write_item(
            RequestItems={self._table_name: items_to_send}
        )
        unprocessed_items = response["UnprocessedItems"].get(
            self._table_name, []
        )

        if unprocessed_items:
            self._items_buffer.extend(unprocessed_items)


def _build_facet_item(*, facet: Facet, item: Item, table: Table) -> Item:
    key_structure = table.primary_key
    attrs = (key_structure.partition_key, key_structure.sort_key, *facet.attrs)
    return {attr: item[attr] for attr in attrs if item.get(attr) is not None}


def _build_query_args(
    *,
    condition_expression: ConditionBase,
    facets: Tuple[Facet, ...],
    filter_expression: Optional[ConditionBase],
    index: Optional[Index],
    limit: Optional[int],
    start_key: Optional[Dict[str, str]],
    table: Table,
) -> Dict[str, Any]:
    facet_attrs = tuple({attr for facet in facets for attr in facet.attrs})
    attrs = {
        table.primary_key.partition_key,
        table.primary_key.sort_key,
        *facet_attrs,
    }
    if index:
        attrs.add(index.primary_key.partition_key)
        attrs.add(index.primary_key.sort_key)
    args = {
        "ExpressionAttributeNames": {f"#{attr}": attr for attr in attrs},
        "FilterExpression": filter_expression,
        "IndexName": index.name if index else None,
        "KeyConditionExpression": condition_expression,
        "ProjectionExpression": ",".join([f"#{attr}" for attr in attrs]),
    }
    if limit:
        args["Limit"] = limit
    if start_key:
        args["ExclusiveStartKey"] = start_key
    return _exclude_none(args=args)


def _parse_floats(*, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts floats into Decimal.
    Needed as floats are currently unsupported by DynamoDB
    """
    return {
        key: _parse_floats(args=value)
        if isinstance(value, dict)
        else Decimal(str(value))
        if isinstance(value, float)
        else value
        for key, value in args.items()
    }


def _exclude_none(*, args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        key: _exclude_none(args=value) if isinstance(value, dict) else value
        for key, value in args.items()
        if value is not None
    }


async def batch_delete_item(
    *, keys: Tuple[PrimaryKey, ...], table: Table
) -> None:
    key_structure = table.primary_key

    async with SESSION.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)

        async with PatchedBatchWriter(
            table_resource.name,
            table_resource.meta.client,
            flush_amount=25,
            overwrite_by_pkeys=None,
            on_exit_loop_sleep=0,
        ) as batch_writer:
            try:
                await aioextensions.collect(
                    tuple(
                        batch_writer.delete_item(
                            Key={
                                key_structure.partition_key: (
                                    primary_key.partition_key
                                ),
                                key_structure.sort_key: primary_key.sort_key,
                            }
                        )
                        for primary_key in keys
                    )
                )
            except ClientError as error:
                handle_error(error=error)


async def batch_get_item(
    *, keys: Tuple[PrimaryKey, ...], table: Table
) -> Tuple[Item, ...]:
    key_structure = table.primary_key
    items: List[Item] = []

    async with SESSION.resource(**RESOURCE_OPTIONS) as resource:

        async def _get_chunk(chunk_keys: List[PrimaryKey]) -> Tuple[Item, ...]:
            response = await resource.batch_get_item(
                RequestItems={
                    table.name: {
                        "Keys": [
                            {
                                key_structure.partition_key: (
                                    primary_key.partition_key
                                ),
                                key_structure.sort_key: primary_key.sort_key,
                            }
                            for primary_key in chunk_keys
                        ]
                    }
                },
            )
            return response["Responses"][table.name]

        try:
            items = [
                item
                for items_chunk in await collect(
                    tuple(
                        _get_chunk(keys_chunk)
                        for keys_chunk in chunked(keys, 100)
                    ),
                )
                for item in items_chunk
            ]
        except ClientError as error:
            handle_error(error=error)

    return tuple(items)


async def batch_put_item(*, items: Tuple[Item, ...], table: Table) -> None:
    async with SESSION.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)

        async with PatchedBatchWriter(
            table_resource.name,
            table_resource.meta.client,
            flush_amount=25,
            overwrite_by_pkeys=None,
            on_exit_loop_sleep=0,
        ) as batch_writer:
            try:
                await aioextensions.collect(
                    tuple(
                        batch_writer.put_item(
                            Item=_exclude_none(args=_parse_floats(args=item))
                        )
                        for item in items
                    )
                )
            except ClientError as error:
                handle_error(error=error)


async def delete_item(
    *,
    condition_expression: Optional[ConditionBase] = None,
    key: PrimaryKey,
    table: Table,
) -> None:
    key_structure = table.primary_key

    async with SESSION.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)
        args = {
            "ConditionExpression": condition_expression,
            "Key": {
                key_structure.partition_key: key.partition_key,
                key_structure.sort_key: key.sort_key,
            },
        }

        try:
            await table_resource.delete_item(**_exclude_none(args=args))
        except ClientError as error:
            handle_error(error=error)


def _build_get_item_args(
    *, facets: Tuple[Facet, ...], key: PrimaryKey, table: Table
) -> Dict[str, Any]:
    facet_attrs = tuple({attr for facet in facets for attr in facet.attrs})
    attrs = {
        table.primary_key.partition_key,
        table.primary_key.sort_key,
        *facet_attrs,
    }
    key_structure = table.primary_key

    return {
        "ExpressionAttributeNames": {f"#{attr}": attr for attr in attrs},
        "Key": {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
        },
        "ProjectionExpression": ",".join([f"#{attr}" for attr in attrs]),
    }


async def get_item(
    *, facets: Tuple[Facet, ...], key: PrimaryKey, table: Table
) -> Optional[Item]:
    item: Optional[Item] = None

    async with SESSION.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)
        get_item_args = _build_get_item_args(
            key=key, facets=facets, table=table
        )

        try:
            response = await table_resource.get_item(**get_item_args)
            item = response.get("Item")
        except ClientError as error:
            handle_error(error=error)

    return item


async def put_item(
    *,
    condition_expression: Optional[ConditionBase] = None,
    facet: Facet,
    item: Item,
    table: Table,
) -> None:
    async with SESSION.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)
        facet_item = _build_facet_item(facet=facet, item=item, table=table)
        args = {
            "ConditionExpression": condition_expression,
            "Item": _parse_floats(args=facet_item),
        }

        try:
            await table_resource.put_item(**_exclude_none(args=args))
        except ClientError as error:
            handle_error(error=error)


async def query(  # pylint: disable=too-many-locals
    *,
    after: Optional[str] = None,
    condition_expression: ConditionBase,
    facets: Tuple[Facet, ...],
    filter_expression: Optional[ConditionBase] = None,
    index: Optional[Index] = None,
    limit: Optional[int] = None,
    paginate: bool = False,
    table: Table,
) -> QueryResponse:
    async with SESSION.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)
        start_key = None
        if after:
            start_key = get_key_from_cursor(after, index, table)

        query_args = _build_query_args(
            condition_expression=condition_expression,
            facets=facets,
            filter_expression=filter_expression,
            index=index,
            limit=limit,
            start_key=start_key,
            table=table,
        )

        try:
            response = await table_resource.query(**query_args)
            items: List[Item] = response.get("Items", [])
            if paginate:
                cursor = get_cursor(
                    index, items[-1] if items else start_key, table
                )
                has_next_page = bool(response.get("LastEvaluatedKey"))
            else:
                while response.get("LastEvaluatedKey"):
                    response = await table_resource.query(
                        **query_args,
                        ExclusiveStartKey=response.get("LastEvaluatedKey"),
                    )
                    items += response.get("Items", [])
                cursor = get_cursor(index, None, table)
                has_next_page = False
        except ClientError as error:
            handle_error(error=error)

    return QueryResponse(
        items=tuple(items),
        page_info=PageInfo(has_next_page=has_next_page, end_cursor=cursor),
    )


def _format_map_attrs(attr: str) -> str:
    return ".".join([f"#{map_attr}" for map_attr in attr.split(".")])


async def update_item(
    *,
    condition_expression: Optional[ConditionBase] = None,
    item: Item,
    key: PrimaryKey,
    table: Table,
) -> None:
    key_structure = table.primary_key
    item_attrs = chain(
        *[attr.split(".") if "." in attr else [attr] for attr in item]
    )
    attr_names = {f"#{attr}": attr for attr in item_attrs}
    attr_values = {
        f":{attr.replace('.', '')}": value
        for attr, value in item.items()
        if value is not None
    }
    attrs_to_update = ",".join(
        f"{_format_map_attrs(attr)} = :{attr.replace('.', '')}"
        if "." in attr
        else f"#{attr} = :{attr}"
        for attr, value in item.items()
        if value is not None
    )
    attrs_to_remove = ",".join(
        f"{_format_map_attrs(attr)}"
        for attr, value in item.items()
        if value is None
    )

    async with SESSION.resource(**RESOURCE_OPTIONS) as resource:
        table_resource: CustomTableResource = await resource.Table(table.name)
        base_args: Dict[str, Any] = {
            "ConditionExpression": condition_expression,
            "ExpressionAttributeNames": attr_names,
            "Key": {
                key_structure.partition_key: key.partition_key,
                key_structure.sort_key: key.sort_key,
            },
            "UpdateExpression": " ".join(
                (
                    f"SET {attrs_to_update}" if attrs_to_update else "",
                    f"REMOVE {attrs_to_remove}" if attrs_to_remove else "",
                )
            ),
        }
        args = (
            {**base_args, "ExpressionAttributeValues": attr_values}
            if attrs_to_update
            else base_args
        )

        try:
            await table_resource.update_item(**_exclude_none(args=args))
        except ClientError as error:
            handle_error(error=error)
