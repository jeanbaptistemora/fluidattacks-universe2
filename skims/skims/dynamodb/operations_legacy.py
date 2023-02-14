from dynamodb.resource import (
    get_resource,
)
from typing import (
    Any,
)


async def scan(table: str, scan_attrs: dict[str, Any]) -> list[Any]:
    response_items: list[Any]
    dynamodb_resource = await get_resource()
    dynamo_table = await dynamodb_resource.Table(table)
    response = await dynamo_table.scan(**scan_attrs)
    response_items = response.get("Items", [])
    while response.get("LastEvaluatedKey"):
        scan_attrs.update(
            {"ExclusiveStartKey": response.get("LastEvaluatedKey")}
        )
        response = await dynamo_table.scan(**scan_attrs)
        response_items += response.get("Items", [])
    return response_items
