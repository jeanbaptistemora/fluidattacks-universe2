from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.types import (
    Event,
)
from moto.dynamodb2 import (
    dynamodb_backend2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import pytest
from typing import (
    Any,
)
from unittest import (
    mock,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["table", "length"],
    [
        ["integrates_vms", 1],
    ],
)
def test_create_tables(
    dynamo_resource: ServiceResource, table: str, length: int
) -> None:
    assert table in dynamodb_backend2.tables
    assert len(dynamo_resource.Table(table).scan()["Items"]) == length


async def test_get_event(
    dynamo_resource: ServiceResource,
) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders: Dataloaders = get_new_context()
    event_id = "418900971"
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        test_data: Event = await loaders.event.load(event_id)
    expected_output = "unittesting"
    assert test_data.group_name == expected_output
