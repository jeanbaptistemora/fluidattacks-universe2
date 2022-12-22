import boto3
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (  # type: ignore
    VulnerabilityTreatmentStatus,
)
from decimal import (
    Decimal,
)
from moto.dynamodb2 import (
    mock_dynamodb2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
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

data: Dict[str, List[Any]] = dict(
    integrates_vms=[
        dict(
            finding_id="988493279",
            id="47ce0fb0-4108-49b0-93cc-160dce8168a6",
            treatment=dict(
                modified_by="integratesuser@gmail.com",
                assigned="integratesuser@gmail.com",
                justification="Observations about permanently accepted",
                modified_date="2020-10-08T00:59:06+00:00",
                acceptance_status=VulnerabilityAcceptanceStatus.APPROVED,
                status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=0,
                unreliable_source="ASM",
                unreliable_efficacy=0,
                unreliable_treatment_changes=Decimal("2"),
            ),
            type=VulnerabilityType.PORTS,
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            created_by="unittest@fluidattacks.com",
            created_date="2019-04-08T00:45:15+00:00",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source=Source.ASM,
                modified_date="2019-04-08T00:45:15+00:00",
                specific="8888",
                status=VulnerabilityStateStatus.VULNERABLE,
                tool=dict(
                    name="tool-1",
                    impact=VulnerabilityToolImpact.INDIRECT,
                ),
                where="192.168.1.19",
            ),
            pk="VULN#47ce0fb0-4108-49b0-93cc-160dce8168a6",
            sk="FIN#988493279",
            pk_2="ROOT",
            sk_2="VULN#47ce0fb0-4108-49b0-93cc-160dce8168a6",
            pk_3="USER#integratesuser@gmail.com",
            sk_3="VULN#47ce0fb0-4108-49b0-93cc-160dce8168a6",
            sk_5="VULN#DELETED#false#ZR#false#STATE#open#VERIF#none",
            pk_5="FIN#988493279",
        ),
        dict(
            finding_id="422286126",
            id="0a848781-b6a4-422e-95fa-692151e6a98z",
            treatment=dict(
                modified_by="integratesuser@gmail.com",
                assigned="integratesuser2@gmail.com",
                justification="test justification",
                modified_date="2020-01-03T17:46:10+00:00",
                status=VulnerabilityTreatmentStatus.IN_PROGRESS,
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=Decimal("0"),
                unreliable_source="ASM",
                unreliable_efficacy=Decimal("0"),
                unreliable_treatment_changes=Decimal("1"),
            ),
            type=VulnerabilityType.LINES,
            created_by="unittest@fluidattacks.com",
            created_date="2020-01-03T17:46:10+00:00",
            state=dict(
                commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                modified_by="unittest@fluidattacks.com",
                source=Source.ASM,
                modified_date="2020-01-03T17:46:10+00:00",
                specific="12",
                status=VulnerabilityStateStatus.VULNERABLE,
                tool=dict(
                    name="tool-2",
                    impact=VulnerabilityToolImpact.INDIRECT,
                ),
                where="test/data/lib_path/f060/csharp.cs",
            ),
            pk="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            sk="FIN#422286126",
            pk_2="ROOT",
            sk_2="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            pk_3="USER#integratesuser@gmail.com",
            sk_3="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            sk_5="VULN#DELETED#false#ZR#true#STATE#open#VERIF#none",
            pk_5="FIN#422286126",
        ),
    ]
)


@pytest.fixture(name="dynamo_resource", scope="module")
async def dynamodb() -> AsyncGenerator[ServiceResource, None]:
    """Mocked DynamoDB Fixture."""
    with mock_dynamodb2():
        yield boto3.resource("dynamodb")


@pytest.fixture(scope="module", autouse=True)
def create_tables(
    dynamodb_tables_args: dict, dynamo_resource: ServiceResource
) -> None:
    for table in tables_names:

        dynamo_resource.create_table(
            TableName=table,
            KeySchema=dynamodb_tables_args[table]["key_schema"],
            AttributeDefinitions=dynamodb_tables_args[table][
                "attribute_definitions"
            ],
            GlobalSecondaryIndexes=dynamodb_tables_args[table][
                "global_secondary_indexes"
            ],
        )
        for item in data[table]:
            dynamo_resource.Table(table).put_item(Item=item)
