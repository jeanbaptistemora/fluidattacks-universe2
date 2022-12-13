import boto3
from decimal import (
    Decimal,
)
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

data: Dict[str, List[Any]] = dict(
    integrates_vms=[
        dict(
            role="hacker",
            group_name="unittesting",
            responsability="Test",
            sk="GROUP#unittesting",
            has_access=True,
            pk="USER#integrateshacker@fluidattacks.com",
            email="integrateshacker@fluidattacks.com",
        ),
        dict(
            role="user_manager",
            group_name="unittesting",
            responsability="Test",
            sk="GROUP#unittesting",
            has_access=True,
            pk="USER#integratesuser@gmail.com",
            email="integratesuser@gmail.com",
        ),
        dict(
            role="user_manager",
            group_name="unittesting",
            responsability="Test",
            sk="GROUP#unittesting",
            has_access=True,
            pk="USER#continuoushacking@gmail.com",
            email="continuoushacking@gmail.com",
        ),
        dict(
            role="user_manager",
            group_name="oneshottest",
            responsability="Test",
            sk="GROUP#oneshottest",
            has_access=True,
            pk="USER#continuoushacking@gmail.com",
            email="continuoushacking@gmail.com",
        ),
        dict(
            role="reattacker",
            group_name="oneshottest",
            responsability="Test",
            sk="GROUP#oneshottest",
            has_access=True,
            pk="USER#integrateshacker@fluidattacks.com",
            email="integrateshacker@fluidattacks.com",
        ),
        dict(
            role="user",
            group_name="oneshottest",
            responsability="Test",
            sk="GROUP#oneshottest",
            has_access=True,
            pk="USER#integratesuser@gmail.com",
            email="integratesuser@gmail.com",
        ),
        dict(
            role="user_manager",
            group_name="unittesting",
            responsability="Test",
            sk="GROUP#unittesting",
            has_access=True,
            pk="USER#integratesuser@gmail.com",
            email="integratesuser@gmail.com",
        ),
        dict(
            role="customer_manager",
            sk="ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            pk="USER#org_testgroupmanager1@gmail.com",
            email="org_testgroupmanager1@gmail.com",
            organization_id="f2e2777d-a168-4bea-93cd-d79142b294d2",
        ),
        dict(
            role="customer_manager",
            sk="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            pk="USER#unittest2@fluidattacks.com",
            email="unittest2@fluidattacks.com",
            organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        ),
        dict(
            is_concurrent_session=False,
            is_registered=True,
            role="hacker",
            last_name="Hacking",
            last_login_date="2020-03-23T15:45:37+00:00",
            legal_remember=True,
            registration_date="2018-02-28T16:54:12+00:00",
            sk="USER#continuoushacking@gmail.com",
            pk_2="USER#all",
            pk="USER#continuoushacking@gmail.com",
            first_name="Continuous",
            email="continuoushacking@gmail.com",
            sk_2="USER#continuoushacking@gmail.com",
        ),
        dict(
            is_concurrent_session=False,
            is_registered=True,
            role="user",
            last_name="Buendia",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember=True,
            registration_date="2018-02-28T16:54:12+00:00",
            sk="USER#integratesuser2@gmail.com",
            pk_2="USER#all",
            pk="USER#integratesuser2@gmail.com",
            first_name="Aureliano",
            email="integratesuser2@gmail.com",
            sk_2="USER#integratesuser2@gmail.com",
        ),
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="hacker",
            last_name="Hacker",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember="False",
            registration_date="2018-02-28T16:54:12+00:00",
            sk="USER#integrateshacker@fluidattacks.com",
            pk_2="USER#all",
            pk="USER#integrateshacker@fluidattacks.com",
            first_name="Integrates",
            email="integrateshacker@fluidattacks.com",
            sk_2="USER#integrateshacker@fluidattacks.com",
        ),
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="user",
            last_name="User",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember="True",
            registration_date="2018-02-28T16:54:12+00:00",
            sk="USER#integratesuser@gmail.com",
            pk_2="USER#all",
            pk="USER#integratesuser@gmail.com",
            first_name="Integrates",
            email="integratesuser@gmail.com",
            sk_2="USER#integratesuser@gmail.com",
        ),
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="admin",
            last_name="de Orellana",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember="True",
            registration_date="2019-02-28T16:54:12+00:00",
            sk="USER#unittest@fluidattacks.com",
            pk_2="USER#all",
            pk="USER#unittest@fluidattacks.com",
            first_name="Miguel",
            email="unittest@fluidattacks.com",
            sk_2="USER#unittest@fluidattacks.com",
        ),
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="admin",
            last_name="Lavoe",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember="True",
            registration_date="2019-02-28T16:54:12+00:00",
            sk="USER#integrates@fluidattacks.com",
            pk_2="USER#all",
            pk="USER#integrates@fluidattacks.com",
            first_name="Hector",
            email="integrates@fluidattacks.com",
            sk_2="USER#integrates@fluidattacks.com",
        ),
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="user",
            last_name="Lebron",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember="True",
            registration_date="2018-02-28T16:54:12+00:00",
            sk="USER#unittesting@fluidattacks.com",
            pk_2="USER#all",
            pk="USER#unittesting@fluidattacks.com",
            first_name="Pablo",
            email="unittesting@fluidattacks.com",
            sk_2="USER#unittesting@fluidattacks.com",
        ),
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="admin",
            last_name="Mirabal",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember="False",
            registration_date="2018-02-28T16:54:12+00:00",
            sk="USER#unittesting@gmail.com",
            pk_2="USER#all",
            pk="USER#unittesting@gmail.com",
            first_name="Manuel",
            email="unittesting@gmail.com",
            sk_2="USER#unittesting@gmail.com",
        ),
        dict(
            pk="USER#integratesuser@gmail.com",
            sk="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            email="integratesuser@gmail.com",
            organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            role="user_manager",
        ),
        dict(
            pk="USER#unittesting@fluidattacks.com",
            sk="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            email="unittesting@fluidattacks.com",
            organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            role="user",
        ),
        dict(
            pk="USER#integrates@fluidattacks.com",
            sk="ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            email="integrates@fluidattacks.com",
            organization_id="f2e2777d-a168-4bea-93cd-d79142b294d2",
            role="admin",
        ),
        dict(
            pk="USER#unittesting@gmail.com",
            sk="ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            email="unittesting@gmail.com",
            organization_id="f2e2777d-a168-4bea-93cd-d79142b294d2",
            role="admin",
        ),
        dict(
            business_name="Testing Company and Sons",
            policies=dict(
                max_number_acceptances=3,
                min_acceptance_severity=0,
                vulnerability_grace_period=10,
                modified_by="integratesmanager@gmail.com",
                min_breaking_severity=Decimal("3.9"),
                max_acceptance_days=90,
                modified_date="2021-11-22T20:07:57+00:00",
                max_acceptance_severity=Decimal("3.9"),
            ),
            description="oneshot testing",
            language="EN",
            created_by="unknown",
            organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            sk="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            name="oneshottest",
            pk="GROUP#oneshottest",
            created_date="2019-01-20T22:00:00+00:00",
            state=dict(
                has_squad=False,
                tier="ONESHOT",
                managed="NOT_MANAGED",
                service="BLACK",
                modified_by="unknown",
                has_machine=True,
                modified_date="2019-01-20T22:00:00+00:00",
                tags=["test_tags"],
                type="ONESHOT",
                status="ACTIVE",
            ),
            business_id="14441323",
            sprint_duration=2,
        ),
        dict(
            business_name="Testing Company and Sons",
            policies=dict(
                max_number_acceptances=3,
                min_acceptance_severity=0,
                vulnerability_grace_period=10,
                modified_by="integratesmanager@gmail.com",
                min_breaking_severity=Decimal("3.9"),
                max_acceptance_days=90,
                modified_date="2021-11-22T20:07:57+00:00",
                max_acceptance_severity=Decimal("3.9"),
            ),
            context="Group context test",
            disambiguation="Disambiguation test",
            description="Integrates unit test group",
            language="EN",
            created_by="unknown",
            organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            sk="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            name="unittesting",
            pk="GROUP#unittesting",
            created_date="2018-03-08T00:43:18+00:00",
            files=[
                dict(
                    modified_by="unittest@fluidattacks.com",
                    description="Test",
                    modified_date="2019-03-01T20:21:00+00:00",
                    file_name="test.zip",
                ),
                dict(
                    modified_by="unittest@fluidattacks.com",
                    description="shell",
                    modified_date="2019-04-24T19:56:00+00:00",
                    file_name="shell.exe",
                ),
                dict(
                    modified_by="unittest@fluidattacks.com",
                    description="shell2",
                    modified_date="2019-04-24T19:59:00+00:00",
                    file_name="shell2.exe",
                ),
                dict(
                    modified_by="unittest@fluidattacks.com",
                    description="test_description",
                    modified_date="2019-08-06T19:28:00+00:00",
                    file_name="test.py",
                ),
            ],
            state=dict(
                has_squad=True,
                tier="MACHINE",
                managed="NOT_MANAGED",
                service="WHITE",
                modified_by="unknown",
                has_machine=True,
                modified_date="2018-03-08T00:43:18+00:00",
                type="CONTINUOUS",
                tags=["test-groups", "test-updates", "test-tag"],
                status="ACTIVE",
            ),
            sprint_start_date="2022-05-31T00:00:00+00:00",
            business_id="14441323",
            sprint_duration=2,
        ),
    ],
)


@pytest.fixture(scope="function", autouse=True)
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
