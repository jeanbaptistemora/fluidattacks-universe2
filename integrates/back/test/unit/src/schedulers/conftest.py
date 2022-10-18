# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import boto3
from moto.dynamodb2 import (
    mock_dynamodb2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import os
import pytest
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
            treatment=dict(
                modified_by="integratesuser@gmail.com",
                assigned="integratesuser2@gmail.com",
                justification="test justification",
                modified_date="2020-01-03T17:46:10+00:00",
                status="IN_PROGRESS",
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            pk_5="FIN#422286126",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=0,
                unreliable_source="ASM",
                unreliable_efficacy=0,
                unreliable_treatment_changes=1,
            ),
            specific="12",
            type="LINES",
            created_by="unittest@fluidattacks.com",
            sk="FIN#422286126",
            sk_3="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            pk_2="ROOT",
            where="test/data/lib_path/f060/csharp.cs",
            created_date="2020-01-03T17:46:10+00:00",
            pk="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            pk_3="USER#integratesuser@gmail.com",
            sk_5="VULN#DELETED#false#ZR#false#STATE#open#VERIF#none",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source="ASM",
                modified_date="2020-01-03T17:46:10+00:00",
                tool=dict(
                    name="tool-2",
                    impact="INDIRECT",
                ),
                status="OPEN",
            ),
            sk_2="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
        ),
        dict(
            treatment=dict(
                modified_by="integratesuser2@gmail.com",
                assigned="integratesuser@gmail.com",
                justification="This is a treatment justification",
                modified_date="2020-11-23T17:46:10+00:00",
                status="IN_PROGRESS",
            ),
            hacker_email="test@unittesting.com",
            group_name="unittesting",
            pk_5="FIN#422286126",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=0,
                unreliable_source="ASM",
                unreliable_efficacy=0,
                unreliable_treatment_changes=1,
            ),
            specific="phone",
            type="INPUTS",
            created_by="test@unittesting.com",
            zero_risk=dict(
                modified_by="test@gmail.com",
                modified_date="2020-09-09T21:01:26+00:00",
                comment_id="123456",
                status="CONFIRMED",
            ),
            sk="FIN#422286126",
            sk_3="VULN#80d6a69f-a376-46be-98cd-2fdedcffdcc0",
            pk_2="ROOT",
            where="https://example.com",
            created_date="2020-09-09T21:01:26+00:00",
            pk="VULN#80d6a69f-a376-46be-98cd-2fdedcffdcc0",
            pk_3="USER#integratesuser@gmail.com",
            sk_5="VULN#DELETED#false#ZR#true#STATE#open#VERIF#none",
            state=dict(
                modified_by="test@unittesting.com",
                source="ASM",
                modified_date="2020-09-09T21:01:26+00:00",
                tool=dict(
                    name="tool-2",
                    impact="INDIRECT",
                ),
                status="OPEN",
            ),
            sk_2="VULN#80d6a69f-a376-46be-98cd-2fdedcffdcc0",
        ),
    ],
)


@pytest.fixture(scope="function", autouse=False)
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(name="dynamo_resource", scope="module")
async def dynamodb() -> AsyncGenerator[ServiceResource, None]:
    """Mocked DynamoDB Fixture."""
    with mock_dynamodb2():
        yield boto3.resource("dynamodb")


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
