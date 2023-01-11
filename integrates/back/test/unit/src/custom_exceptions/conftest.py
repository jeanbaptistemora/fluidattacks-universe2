import boto3
from decimal import (
    Decimal,
)
from moto import (
    mock_s3,
)
from moto.dynamodb2 import (
    mock_dynamodb2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
from mypy_boto3_s3 import (
    S3Client,
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

BUCKET_NAME = "unit_test_bucket"
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
            pk="USER#unittest@fluidattacks.com",
            sk="GROUP#unittesting",
            role="reattacker",
            has_access=True,
            responsibility="Testes",
            group_name="unittesting",
            email="unittest@fluidattacks.com",
        ),
        dict(
            business_name="Testing Company and Sons",
            policies=dict(
                max_number_acceptances=1,
                min_acceptance_severity=0,
                vulnerability_grace_period=10,
                modified_by="integratesmanager@gmail.com",
                min_breaking_severity=Decimal("3.9"),
                max_acceptance_days=60,
                modified_date="2021-11-22T20:07:57+00:00",
                max_acceptance_severity=Decimal("3.9"),
            ),
            description="Integrates group",
            language="EN",
            created_by="unittest@fluidattacks.com",
            organization_id="f2e2777d-a168-4bea-93cd-d79142b294d2",
            sk="ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            name="kurome",
            pk="GROUP#kurome",
            created_date="2020-05-20T22:00:00+00:00",
            state=dict(
                has_squad=False,
                tier="OTHER",
                managed="NOT_MANAGED",
                service="WHITE",
                modified_by="unittest@fluidattacks.com",
                has_machine=False,
                modified_date="2020-05-20T22:00:00+00:00",
                type="CONTINUOUS",
                status="ACTIVE",
            ),
            sprint_start_date="2022-06-06T00:00:00+00:00",
            business_id="14441323",
            sprint_duration=2,
        ),
        dict(
            business_name="Testing Company and Sons",
            description="Integrates unit test group",
            language="EN",
            created_by="unittest@fluidattacks.com",
            organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            sk="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            name="unittesting",
            pk="GROUP#unittesting",
            created_date="2018-03-08T00:43:18+00:00",
            state=dict(
                has_squad=True,
                tier="MACHINE",
                managed="NOT_MANAGED",
                service="WHITE",
                modified_by="unittest@fluidattacks.com",
                has_machine=True,
                modified_date="2018-03-08T00:43:18+00:00",
                type="CONTINUOUS",
                status="ACTIVE",
                tags=["test-groups", "test-updates", "test-tag"],
            ),
            sprint_start_date="2022-05-31T00:00:00+00:00",
            business_id="14441323",
            sprint_duration=2,
        ),
    ]
)


@pytest_asyncio.fixture(name="dynamo_resource", scope="module")
async def dynamodb() -> AsyncGenerator[ServiceResource, None]:
    """Mocked DynamoDB Fixture."""
    with mock_dynamodb2():
        yield boto3.resource("dynamodb")


@pytest_asyncio.fixture(name="s3_client", scope="module")
async def s_3() -> AsyncGenerator[S3Client, None]:
    """Mocked S3 Fixture."""
    with mock_s3():
        yield boto3.client("s3")


@pytest.fixture(scope="module", autouse=True)
def create_tables(dynamo_resource: ServiceResource) -> None:
    for table in tables_names:
        dynamo_resource.create_table(
            TableName=table,
            KeySchema=key_schemas[table],  # type: ignore
            AttributeDefinitions=attribute_definitions[table],  # type: ignore
            GlobalSecondaryIndexes=global_secondary_indexes[table],
        )
        for item in data[table]:
            dynamo_resource.Table(table).put_item(Item=item)


@pytest.fixture(scope="module", autouse=True)
def create_bucket(s3_client: S3Client) -> None:
    s3_client.create_bucket(Bucket=BUCKET_NAME)
