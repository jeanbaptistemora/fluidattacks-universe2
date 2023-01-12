import boto3
from moto.dynamodb import (
    mock_dynamodb,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    List,
)

pytestmark = [
    pytest.mark.asyncio,
]

tables_names = ["integrates_vms"]
key_schemas = {
    "integrates_vms": [
        {"AttributeName": "pk", "KeyType": "HASH"},
        {"AttributeName": "sk", "KeyType": "RANGE"},
    ],
}
attribute_definitions = {
    "integrates_vms": [
        {"AttributeName": "sk", "AttributeType": "S"},
        {"AttributeName": "pk", "AttributeType": "S"},
    ],
}
global_secondary_indexes: Dict[str, List[Any]] = {
    "integrates_vms": [
        {
            "IndexName": "inverted_index",
            "KeySchema": [
                {"AttributeName": "sk", "KeyType": "HASH"},
                {"AttributeName": "pk", "KeyType": "RANGE"},
            ],
            "Projection": {
                "ProjectionType": "ALL",
            },
        }
    ],
}
data: Dict[str, List[Any]] = dict(
    integrates_vms=[
        dict(
            group_name="unittesting",
            description="Integrates unit test",
            unreliable_indicators=dict(
                unreliable_where="test",
            ),
            type="OTHER",
            created_by="unittest@fluidattacks.com",
            hacker="unittest@fluidattacks.com",
            event_date="2018-06-27T12:00:00+00:00",
            sk="GROUP#unittesting",
            client="Fluid",
            pk_2="GROUP#unittesting",
            created_date="2018-06-27T19:40:05+00:00",
            id="418900971",
            pk="EVENT#418900971",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                modified_date="2018-06-27T19:40:05+00:00",
                status="CREATED",
            ),
            evidences=dict(
                evidence1=dict(
                    modified_date="2019-04-08T05:00:00+00:00",
                    description="Comm1",
                    url="test_url",
                ),
            ),
            sk_2="EVENT#SOLVED#false",
        ),
    ],
)


@pytest_asyncio.fixture(name="dynamo_resource", scope="module")
async def dynamodb() -> AsyncGenerator[ServiceResource, None]:
    """Mocked DynamoDB Fixture."""
    with mock_dynamodb():
        yield boto3.resource("dynamodb")


@pytest.fixture(scope="module", autouse=True)
def create_tables(
    dynamodb_tables_args: dict, dynamo_resource: ServiceResource
) -> None:
    for table in tables_names:
        dynamo_resource.create_table(
            TableName=table,
            KeySchema=key_schemas[table],  # type: ignore
            AttributeDefinitions=attribute_definitions[table],  # type: ignore
            GlobalSecondaryIndexes=global_secondary_indexes[table],
            ProvisionedThroughput=dynamodb_tables_args[table][
                "provisioned_throughput"
            ],
        )
        for item in data[table]:
            dynamo_resource.Table(table).put_item(Item=item)
